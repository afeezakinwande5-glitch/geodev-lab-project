import geopandas as gpd

gdf = gpd.read_file("Abeokuta_bdry.gpkg")

print("CRS:")
print(gdf.crs)

print("\nGeometry:")
print(gdf.geometry.head())

print("\nGeometry types:")
print(gdf.geom_type.value_counts())

print("\nTotal bounds:")
print(gdf.total_bounds)

print("\nArea:")
print(gdf.geometry.area.head())