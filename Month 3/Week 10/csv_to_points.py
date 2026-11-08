import pandas as pd
import geopandas as gpd

from shapely.geometry import Point

df = pd.read_csv("locations.csv")

geometry = [
    Point(xy)
    for xy in zip(df["longitude"], df["latitude"])
]

gdf = gpd.GeoDataFrame(
    df,
    geometry=geometry,
    crs="EPSG:4326"
)

print(gdf)

print("\nCRS:")
print(gdf.crs)