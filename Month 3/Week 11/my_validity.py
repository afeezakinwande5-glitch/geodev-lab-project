
from pathlib import Path
import geopandas as gpd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed"

ADMIN_FILE = DATA / "NGA_adm2.shp"
OUTPUT_FILE = DATA / "ogbomoso_lgas_valid.gpkg"

# Read administrative data
admin = gpd.read_file(ADMIN_FILE)

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

# Count invalid geometries before repair
invalid_before = (~polygons.geometry.is_valid).sum()

print("Invalid geometries before repair:", invalid_before)

# Repair geometries
polygons.geometry = polygons.geometry.make_valid()

# Count invalid geometries after repair
invalid_after = (~polygons.geometry.is_valid).sum()

print("Invalid geometries after repair:", invalid_after)

if invalid_before == 0:
    print("All geometries were already valid. No repair was necessary.")
elif invalid_after == 0:
    print("Geometry repair completed successfully.")
else:
    print("Some geometries remain invalid. Further inspection is required.")

# Save repaired layer
if OUTPUT_FILE.exists():
    OUTPUT_FILE.unlink()

polygons.to_file(OUTPUT_FILE, driver="GPKG")

print("\nSaved:", OUTPUT_FILE)
