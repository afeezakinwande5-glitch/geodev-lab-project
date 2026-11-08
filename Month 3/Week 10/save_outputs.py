import geopandas as gpd

gdf = gpd.read_file("Abeokuta_bdry.gpkg")

# Save as GeoPackage
gdf.to_file(
    "Abeokuta_bdry_processed.gpkg",
    driver="GPKG"
)

# Save attributes as CSV
gdf.drop(columns="geometry").to_csv(
    "Abeokuta_bdry_attributes.csv",
    index=False
)

print("Outputs saved successfully!")