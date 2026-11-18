
from pathlib import Path
import geopandas as gpd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed"

ADMIN_FILE = DATA / "NGA_adm2.shp"
FACILITY_FILE = DATA / "GRID3_NGA_health_facility.gpkg"
OUTPUT_FILE = DATA / "ogbomoso_facility_count.gpkg"

# Read datasets
admin = gpd.read_file(ADMIN_FILE)
facilities = gpd.read_file(FACILITY_FILE)

print("Admin CRS:", admin.crs)
print("Facilities CRS:", facilities.crs)

# Select Ogbomosho North and South
polygons = admin[
    (admin["NAME_1"].str.strip().str.lower() == "oyo") &
    (admin["NAME_2"].str.strip().str.lower().isin([
        "ogbomosho north",
        "ogbomosho south"
    ]))
].copy()

if polygons.empty:
    raise ValueError("Ogbomosho polygons not found.")

# Reproject both datasets
polygons = polygons.to_crs("EPSG:32631")
facilities = facilities.to_crs("EPSG:32631")

# Repair geometries before spatial operations
polygons.geometry = polygons.geometry.make_valid()

# Reset indexes for reliable counting
polygons = polygons.reset_index(drop=True)
facilities = facilities.reset_index(drop=True)

# Spatial join: facilities within each LGA
joined = gpd.sjoin(
    facilities,
    polygons[["geometry"]],
    how="inner",
    predicate="within"
)

# Count facilities per polygon
counts = joined.groupby("index_right").size()

# Add counts back to every polygon, including zeros
polygons["facility_count"] = (
    polygons.index.map(counts)
    .fillna(0)
    .astype(int)
)

# Total-counted check
total_counted = polygons["facility_count"].sum()
total_matched = len(joined)

print("\nHealth Facility Count by LGA:")
print(polygons[["NAME_2", "facility_count"]])

print("\nTotal counted from polygons:", total_counted)
print("Total spatial join matches:", total_matched)
print("Count check passed:", total_counted == total_matched)

# Save result
if OUTPUT_FILE.exists():
    OUTPUT_FILE.unlink()

polygons.to_file(OUTPUT_FILE, driver="GPKG")

print("\nSaved:", OUTPUT_FILE)
