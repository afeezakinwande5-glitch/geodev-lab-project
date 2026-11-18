import geopandas as gpd
# Load NGA_Adm2 layer
Adm2 = gpd.read_file("NGA_adm2.shp")

# Get the first coordinate
first = Adm2.geometry.iloc[0].exterior.coords[0]

print("Original first corner:", first)

# Reproject the layer
projected = Adm2.to_crs(epsg=32631)

print("After to_crs:",projected.geometry.iloc[0].exterior.coords[0])

# Change only the crs label 
wrongly_labelled = Adm2.set_crs(epsg=32631, allow_override=True)

print("After set_crs:",wrongly_labelled.geometry.iloc[0].exterior.coords[0])

print("Label now says:", wrongly_labelled.crs)
