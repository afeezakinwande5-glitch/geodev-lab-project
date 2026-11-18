from pyproj import Transformer

# Create coordinate transformer
to_utm = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:32631",
    always_xy=True
)

# Transform longitude and latitude
x, y = to_utm.transform(3.9064, 7.4443)

# Display UTM coordinates
print("UTM easting:", round(x, 1))
print("UTM northing:", round(y, 1))