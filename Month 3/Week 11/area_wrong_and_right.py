import geopandas as gpd

# Load Administration_2 Layer
Adm_2 = gpd.read_file("NGA_adm2.shp") 

# Display original crs
print("CRS:", Adm_2.crs)

# Calculate area using geographic CRS
Adm_2["area_wrong"]=Adm_2.area

print(Adm_2[["NAME_2","area_wrong"]].head(5))

# Estimate suitable UTM CRS
print("Suggested UTM:",Adm_2.estimate_utm_crs())

# Reproject Adm_2 to UTM ZONE 31
Adm_2_utm = Adm_2.to_crs(epsg=32631)

# Calculate area in square kilometers
Adm_2_utm["area_km2"] = Adm_2_utm.area/1_000_000

print(Adm_2_utm[["NAME_2","area_km2"]].head(3))

# calculate total area
print(round(Adm_2_utm["area_km2"].sum(),1),"km2")