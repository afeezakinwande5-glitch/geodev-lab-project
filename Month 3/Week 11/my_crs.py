
from pathlib import Path
import geopandas as gpd

# Project paths
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed"

ADMIN_FILE = DATA / "NGA_adm2.shp"
OUTPUT_FILE = DATA / "ogbomoso_lgas_utm.gpkg"

# Read administrative boundaries
admin = gpd.read_file(ADMIN_FILE)

print("Original CRS:", admin.crs)

# Select Ogbomosho North and South in Oyo State
ogb = admin[
    (admin["NAME_1"].str.strip().str.lower() == "oyo") &
    (admin["NAME_2"].str.strip().str.lower().isin([
        "ogbomosho north",
        "ogbomosho south"
    ]))
].copy()

if ogb.empty:
    raise ValueError("Ogbomosho LGAs not found. Check NAME_1 and NAME_2 fields.")

# Estimate the suitable UTM CRS
estimated_crs = ogb.estimate_utm_crs()

print("Estimated UTM CRS:", estimated_crs)

# Use the selected CRS for Ogbomosho
target_crs = "EPSG:32631"
ogb_utm = ogb.to_crs(target_crs)

print("Selected CRS:", ogb_utm.crs)

# Calculate area in square kilometres
ogb_utm["area_km2"] = ogb_utm.geometry.area / 1_000_000

print("\nLGA Areas:")
print(ogb_utm[["NAME_2", "area_km2"]])

# Save result
if OUTPUT_FILE.exists():
    OUTPUT_FILE.unlink()

ogb_utm.to_file(OUTPUT_FILE, driver="GPKG")

print("\nSaved:", OUTPUT_FILE)
