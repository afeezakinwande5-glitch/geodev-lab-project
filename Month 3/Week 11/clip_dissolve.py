
import geopandas as gpd

# ==========================================
# 1. LOAD DATASETS
# ==========================================

admin = gpd.read_file("NGA_adm2.shp")

# ==========================================
# 2. FILTER OGOMOSHO LGAs
# ==========================================

target_lgas = ["Ogbomosho North", "Ogbomosho South"]

ogbomosho = admin[
    admin["NAME_2"].isin(target_lgas)
].copy()

if ogbomosho.empty:
    raise ValueError("Ogbomosho boundaries were not found.")

# ==========================================
# 3. LOAD ROAD DATA
# ==========================================

# Replace this filename with your actual road dataset.
roads = gpd.read_file("roads.gpkg")

if roads.empty:
    raise ValueError("Road dataset is empty.")

# ==========================================
# 4. REPROJECT DATASETS
# ==========================================

ogbomosho = ogbomosho.to_crs(epsg=32631)
roads = roads.to_crs(ogbomosho.crs)

# ==========================================
# 5. CLIP ROADS TO OGOMOSHO
# ==========================================

roads_clipped = gpd.clip(
    roads,
    ogbomosho
)

# ==========================================
# 6. DISSOLVE THE TWO LGA BOUNDARIES
# ==========================================

ogbomosho_dissolved = ogbomosho.dissolve()

# ==========================================
# 7. CALCULATE ROAD LENGTH
# ==========================================

roads_clipped["length_km"] = (
    roads_clipped.geometry.length / 1000
)

total_road_length = roads_clipped["length_km"].sum()

# ==========================================
# 8. EXPORT RESULTS
# ==========================================

roads_clipped.to_file(
    "ogbomosho_clipped_roads.gpkg",
    driver="GPKG"
)

ogbomosho_dissolved.to_file(
    "ogbomosho_dissolved_boundary.gpkg",
    driver="GPKG"
)

# ==========================================
# 9. DISPLAY RESULTS
# ==========================================

print("\n========== CLIPPING AND DISSOLVING ==========")

print("Number of clipped road features:", len(roads_clipped))

print("Total road length (km):", round(total_road_length, 2))

print("Dissolved boundary count:", len(ogbomosho_dissolved))

print("\nOUTPUT FILES:")
print("1. ogbomosho_clipped_roads.gpkg")
print("2. ogbomosho_dissolved_boundary.gpkg")

print("\nCLIPPING AND DISSOLVING COMPLETED!")
