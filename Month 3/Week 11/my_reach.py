
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed"
WEEK_DIR = Path(__file__).resolve().parent

ADMIN_FILE = DATA / "NGA_adm2.shp"
FACILITY_FILE = DATA / "GRID3_NGA_health_facility.gpkg"

GAP_FILE = DATA / "ogbomoso_2km_coverage_gap.gpkg"
MAP_FILE = WEEK_DIR / "my_reach_map.png"

BUFFER_DISTANCE = 2000  # 2 kilometres in metres

# Read datasets
admin = gpd.read_file(ADMIN_FILE)
facilities = gpd.read_file(FACILITY_FILE)

# Select Ogbomosho LGAs
polygons = admin[
    (admin["NAME_1"].str.strip().str.lower() == "oyo") &
    (admin["NAME_2"].str.strip().str.lower().isin([
        "ogbomosho north",
        "ogbomosho south"
    ]))
].copy()

if polygons.empty:
    raise ValueError("Ogbomosho polygons not found.")

# Reproject to UTM Zone 31N
polygons = polygons.to_crs("EPSG:32631")
facilities = facilities.to_crs("EPSG:32631")

# Repair polygon geometry
polygons.geometry = polygons.geometry.make_valid()

# Keep facilities located inside the selected LGAs
facilities = facilities.reset_index(drop=True)

inside = gpd.sjoin(
    facilities,
    polygons[["geometry"]],
    how="inner",
    predicate="within"
)

local_facilities = facilities.loc[
    inside.index.unique()
].copy()

if local_facilities.empty:
    raise ValueError("No health facilities found inside Ogbomosho.")

# Create 2 km buffers around facilities
buffers = local_facilities[["geometry"]].copy()
buffers["geometry"] = buffers.geometry.buffer(BUFFER_DISTANCE)

# Dissolve all buffers into one coverage area
buffer_gdf = gpd.GeoDataFrame(
    buffers,
    geometry="geometry",
    crs=polygons.crs
)

dissolved = buffer_gdf.dissolve()

# Calculate uncovered areas using overlay difference
coverage_gap = gpd.overlay(
    polygons[["geometry"]],
    dissolved[["geometry"]],
    how="difference",
    keep_geom_type=False
)

# Remove empty geometries
coverage_gap = coverage_gap[
    ~coverage_gap.geometry.is_empty
].copy()

# Calculate uncovered area
coverage_gap["gap_km2"] = (
    coverage_gap.geometry.area / 1_000_000
)

# Save coverage gap
if GAP_FILE.exists():
    GAP_FILE.unlink()

coverage_gap.to_file(GAP_FILE, driver="GPKG")

print("Number of facilities:", len(local_facilities))
print("Buffer distance:", BUFFER_DISTANCE, "metres")
print("Uncovered area (km²):")
print(coverage_gap["gap_km2"].sum())

print("\nSaved coverage gap:", GAP_FILE)

# Create the map
covered = gpd.overlay(
    polygons[["geometry"]],
    dissolved[["geometry"]],
    how="intersection",
    keep_geom_type=False
)

fig, ax = plt.subplots(figsize=(12, 10))

polygons.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.5,
    label="LGA boundary"
)

covered.plot(
    ax=ax,
    color="#9ecae1",
    edgecolor="none",
    label="Within 2 km coverage"
)

if not coverage_gap.empty:
    coverage_gap.plot(
        ax=ax,
        color="#f28e2b",
        edgecolor="none",
        label="Outside 2 km coverage"
    )

local_facilities.plot(
    ax=ax,
    color="#17365d",
    markersize=12,
    label="Health facilities"
)

polygons.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.2
)

ax.set_title(
    "HEALTH FACILITY COVERAGE GAP IN OGBOMOSHO",
    fontsize=15,
    fontweight="bold",
    pad=18
)

ax.legend(loc="lower left", frameon=True)
ax.set_axis_off()

plt.tight_layout()
plt.savefig(MAP_FILE, dpi=300, bbox_inches="tight")
plt.close()

print("\nMap saved:", MAP_FILE)
