
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
# 3. REPROJECT DATASETS
# ==========================================

ogbomosho = ogbomosho.to_crs(epsg=32631)
health_ogbomosho = health_ogbomosho.to_crs(epsg=32631)

# ==========================================
# 4. CREATE 2KM BUFFERS
# ==========================================

buffers = health_ogbomosho[["geometry"]].copy()

buffers["geometry"] = buffers.geometry.buffer(2000)

# ==========================================
# 5. DISSOLVE BUFFERS
# ==========================================

coverage = buffers.dissolve()

# ==========================================
# 6. CLIP COVERAGE TO LGA BOUNDARIES
# ==========================================

coverage_inside = gpd.overlay(
    ogbomosho[["NAME_2", "geometry"]],
    coverage,
    how="intersection"
)

# ==========================================
# 7. IDENTIFY UNCOVERED AREAS
# ==========================================

uncovered = gpd.overlay(
    ogbomosho[["NAME_2", "geometry"]],
    coverage,
    how="difference"
)

# ==========================================
# 8. CALCULATE AREA STATISTICS
# ==========================================

ogbomosho["total_area_km2"] = (
    ogbomosho.geometry.area / 1_000_000
)

covered_stats = (
    coverage_inside.assign(
        covered_km2=coverage_inside.geometry.area / 1_000_000
    )
    .groupby("NAME_2")["covered_km2"]
    .sum()
)

uncovered_stats = (
    uncovered.assign(
        uncovered_km2=uncovered.geometry.area / 1_000_000
    )
    .groupby("NAME_2")["uncovered_km2"]
    .sum()
)

ogbomosho["covered_km2"] = (
    ogbomosho["NAME_2"].map(covered_stats).fillna(0)
)

ogbomosho["uncovered_km2"] = (
    ogbomosho["NAME_2"].map(uncovered_stats).fillna(0)
)

ogbomosho["coverage_percent"] = (
    ogbomosho["covered_km2"] /
    ogbomosho["total_area_km2"]
) * 100

ogbomosho["uncovered_percent"] = (
    ogbomosho["uncovered_km2"] /
    ogbomosho["total_area_km2"]
) * 100

# ==========================================
# 9. EXPORT RESULTS
# ==========================================

uncovered.to_file(
    "ogbomosho_uncovered_areas.gpkg",
    driver="GPKG"
)

coverage_inside.to_file(
    "ogbomosho_covered_areas.gpkg",
    driver="GPKG"
)

ogbomosho.to_file(
    "ogbomosho_coverage_statistics.gpkg",
    driver="GPKG"
)

# ==========================================
# 10. DISPLAY RESULTS
# ==========================================

print("\n========== COVERAGE GAP ANALYSIS ==========")

print(
    ogbomosho[
        [
            "NAME_2",
            "total_area_km2",
            "covered_km2",
            "uncovered_km2",
            "coverage_percent",
            "uncovered_percent"
        ]
    ].round(2).to_string(index=False)
)

print("\nTotal uncovered polygons:", len(uncovered))

print("\n========== OUTPUT FILES ==========")
print("1. ogbomosho_uncovered_areas.gpkg")
print("2. ogbomosho_covered_areas.gpkg")
print("3. ogbomosho_coverage_statistics.gpkg")

print("\nCOVERAGE GAP ANALYSIS COMPLETED!")
