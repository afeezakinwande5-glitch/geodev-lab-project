
import geopandas as gpd
from shapely.geometry import Polygon
from shapely.validation import explain_validity
from shapely import make_valid

# ==========================================
# 1. CREATE AN INVALID POLYGON
# ==========================================

coordinates = [
    (0, 0),
    (2, 2),
    (2, 0),
    (0, 2),
    (0, 0)
]

invalid_polygon = Polygon(coordinates)

# ==========================================
# 2. CREATE GEODATAFRAME
# ==========================================

gdf = gpd.GeoDataFrame(
    {"feature_id": [1]},
    geometry=[invalid_polygon],
    crs="EPSG:32631"
)

# ==========================================
# 3. CHECK GEOMETRY VALIDITY
# ==========================================

print("========== BEFORE REPAIR ==========")

print("Geometry type:", gdf.geometry.iloc[0].geom_type)

print("Is valid:", gdf.geometry.is_valid.iloc[0])

print(
    "Validity explanation:",
    explain_validity(gdf.geometry.iloc[0])
)

# ==========================================
# 4. REPAIR INVALID GEOMETRY
# ==========================================

gdf["geometry"] = gdf.geometry.make_valid()

# ==========================================
# 5. CHECK GEOMETRY AFTER REPAIR
# ==========================================

print("\n========== AFTER REPAIR ==========")

print("Geometry type:", gdf.geometry.iloc[0].geom_type)

print("Is valid:", gdf.geometry.is_valid.iloc[0])

print(
    "Validity explanation:",
    explain_validity(gdf.geometry.iloc[0])
)

# ==========================================
# 6. EXPORT REPAIRED GEOMETRY
# ==========================================

gdf.to_file(
    "repaired_geometry.gpkg",
    driver="GPKG"
)

print("\nOutput saved: repaired_geometry.gpkg")

print("\nGEOMETRY REPAIR COMPLETED!")
