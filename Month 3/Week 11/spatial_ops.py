
import geopandas as gpd
import pandas as pd

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

if ogbomosho.empty:
    raise ValueError("Ogbomosho boundaries were not found.")

if health_ogbomosho.empty:
    raise ValueError("No health facilities found in the selected LGAs.")

# ==========================================
# 3. REPROJECT TO UTM ZONE 31N
# ==========================================

ogbomosho = ogbomosho.to_crs(epsg=32631)
health_ogbomosho = health_ogbomosho.to_crs(epsg=32631)

print("CRS:", ogbomosho.crs)

# ==========================================
# 4. SPATIAL JOIN
# ==========================================

joined = gpd.sjoin(
    health_ogbomosho,
    ogbomosho[["NAME_2", "geometry"]],
    how="left",
    predicate="within"
)

# ==========================================
# 5. COUNT FACILITIES PER LGA
# ==========================================

facility_counts = (
    joined.groupby("NAME_2")
    .size()
    .reset_index(name="facility_count")
)

ogbomosho = ogbomosho.merge(
    facility_counts,
    on="NAME_2",
    how="left"
)

ogbomosho["facility_count"] = (
    ogbomosho["facility_count"].fillna(0).astype(int)
)

# ==========================================
# 6. CREATE 2KM FACILITY BUFFERS
# ==========================================

buffers = health_ogbomosho.copy()

buffers["geometry"] = buffers.geometry.buffer(2000)

# ==========================================
# 7. DISSOLVE OVERLAPPING BUFFERS
# ==========================================

coverage_area = buffers[["geometry"]].dissolve()

# ==========================================
# 8. CALCULATE LGA AREA
# ==========================================

ogbomosho["area_km2"] = (
    ogbomosho.geometry.area / 1_000_000
)

# ==========================================
# 9. CALCULATE COVERED AREA
# ==========================================

ogbomosho["covered_km2"] = 0.0

for index, row in ogbomosho.iterrows():

    lga = gpd.GeoDataFrame(
        geometry=[row.geometry],
        crs=ogbomosho.crs
    )

    covered = gpd.overlay(
        lga,
        coverage_area,
        how="intersection"
    )

    covered_area = (
        covered.geometry.area.sum() / 1_000_000
    )

    ogbomosho.loc[index, "covered_km2"] = covered_area

# ==========================================
# 10. CALCULATE UNCOVERED AREA
# ==========================================

ogbomosho["uncovered_km2"] = (
    ogbomosho["area_km2"] -
    ogbomosho["covered_km2"]
)

ogbomosho["coverage_percent"] = (
    ogbomosho["covered_km2"] /
    ogbomosho["area_km2"]
) * 100

# ==========================================
# 11. EXPORT RESULTS
# ==========================================

ogbomosho.to_file(
    "ogbomosho_facility_analysis.gpkg",
    driver="GPKG"
)

health_ogbomosho.to_file(
    "ogbomosho_health_facilities.gpkg",
    driver="GPKG"
)

coverage_area.to_file(
    "ogbomosho_coverage_buffers.gpkg",
    driver="GPKG"
)

# ==========================================
# 12. FINAL RESULTS
# ==========================================

print("\n========== FACILITY DISTRIBUTION ==========")

print(
    ogbomosho[
        ["NAME_2", "facility_count"]
    ].to_string(index=False)
)

print("\n========== COVERAGE ANALYSIS ==========")

print(
    ogbomosho[
        [
            "NAME_2",
            "area_km2",
            "covered_km2",
            "uncovered_km2",
            "coverage_percent"
        ]
    ].round(2).to_string(index=False)
)

print("\nTotal facilities:", len(health_ogbomosho))

print("\n========== EXPORTED FILES ==========")

print("1. ogbomosho_facility_analysis.gpkg")
print("2. ogbomosho_health_facilities.gpkg")
print("3. ogbomosho_coverage_buffers.gpkg")

print("\nWEEK 11 SPATIAL OPERATIONS COMPLETED!")
