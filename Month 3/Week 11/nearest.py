
import geopandas as gpd

# ==========================================
# 1. LOAD DATASETS
# ==========================================

health = gpd.read_file("GRID3_NGA_health_facility.gpkg")
admin = gpd.read_file("NGA_adm2.shp")

print("Datasets loaded successfully.")

# ==========================================
# 2. FILTER OGOMOSHO LGAs
# ==========================================

target_lgas = ["Ogbomosho North", "Ogbomosho South"]

ogbomosho = admin[
    admin["NAME_2"].isin(target_lgas)
].copy()

health_ogbomosho = health[
    health["lga_standard"].isin(target_lgas)
].copy()

if ogbomosho.empty or health_ogbomosho.empty:
    raise ValueError("Required Ogbomosho data was not found.")

# ==========================================
# 3. REPROJECT TO UTM ZONE 31N
# ==========================================

ogbomosho = ogbomosho.to_crs(epsg=32631)
health_ogbomosho = health_ogbomosho.to_crs(epsg=32631)

# ==========================================
# 4. CALCULATE LGA CENTROIDS
# ==========================================

centroids = ogbomosho[["NAME_2", "geometry"]].copy()

centroids["geometry"] = centroids.geometry.centroid

# ==========================================
# 5. FIND NEAREST HEALTH FACILITY
# ==========================================

nearest = gpd.sjoin_nearest(
    centroids,
    health_ogbomosho[
        ["unique_id", "facility_name", "geometry"]
    ],
    how="left",
    distance_col="distance_m"
)

# ==========================================
# 6. CONVERT DISTANCE TO KILOMETRES
# ==========================================

nearest["distance_km"] = (
    nearest["distance_m"] / 1000
)

# ==========================================
# 7. DISPLAY RESULTS
# ==========================================

print("\n========== NEAREST HEALTH FACILITY ==========")

print(
    nearest[
        [
            "NAME_2",
            "unique_id",
            "facility_name",
            "distance_m",
            "distance_km"
        ]
    ].round(2).to_string(index=False)
)

# ==========================================
# 8. EXPORT RESULTS
# ==========================================

nearest.to_file(
    "ogbomosho_nearest_facility.gpkg",
    driver="GPKG"
)

print("\nOutput saved:")
print("ogbomosho_nearest_facility.gpkg")

print("\nNEAREST FACILITY ANALYSIS COMPLETED!")
