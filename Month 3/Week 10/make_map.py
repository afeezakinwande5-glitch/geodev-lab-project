import geopandas as gpd
import matplotlib.pyplot as plt

gdf = gpd.read_file("Abeokuta_bdry.gpkg")

fig, ax = plt.subplots(figsize=(10, 8))

gdf.plot(
    ax=ax,
    color="steelblue",
    edgecolor="black",
    linewidth=0.1
)

ax.set_title(
    "Abeokuta Administrative Boundary",
    fontsize=14
)

ax.set_xlabel("Easting")
ax.set_ylabel("Northing")

ax.set_aspect("equal")

plt.tight_layout()

plt.savefig("Abeokuta_bdry_map.png", dpi=300)

plt.show()