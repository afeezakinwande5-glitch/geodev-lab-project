import geopandas as gpd

gdf = gpd.read_file("Abeokuta_bdry.gpkg")

print("First five features:")
print(gdf.head())

print("\nDataset information:")
print(gdf.info())

print("\nCoordinate Reference System:")
print(gdf.crs)

print("\nGeometry types:")
print(gdf.geom_type.value_counts())

print("\nNumber of features:")
print(len(gdf))
