# Month 1 Summary

## Project Question

Which buildings in the study area are located within 200 m of rivers and may therefore be potentially exposed to river-related flooding?

## Spatial Operation

I performed a 200 m buffer analysis around the river layer using QGIS. I chose the buffer operation because distance from rivers is one factor that can be used to identify buildings that may be potentially exposed to river-related flooding.

## What I Expected

Before running the analysis, I expected to identify around 1,000 or more buildings within the 200 m river buffer. I expected the buildings within the buffer to be concentrated around areas where rivers and waterways pass through built-up areas.

## What I Got

The building layer contains a total of 96,169 buildings. After applying the 200 m river buffer analysis, 3,018 buildings were identified within the buffer.

This represents approximately 3.1% of the total mapped buildings.

The result was higher than my initial expectation of around 1,000 or more buildings.

## Result Checking

I checked the result using the attribute table and confirmed that the output contained 3,018 building features. I also visually inspected the map to check the spatial relationship between the buildings and the 200 m river buffer.

I manually checked a building on the map to confirm that it was located within the buffer area.

## What Surprised Me

I was surprised by the number of buildings located within the 200 m river buffer. I initially expected around 1,000 or slightly more buildings, but the analysis identified 3,018 buildings.

This shows that many mapped buildings are located relatively close to the river network. However, being within 200 m of a river does not by itself mean that a building will flood. River proximity is only one factor that should be considered in a wider flood-risk assessment.

## Data I Still Need

The 200 m river buffer only considers the distance between buildings and rivers. To develop a more complete flood-risk analysis, I still need additional data such as:

- Elevation/DEM
- Slope
- Land cover
- Rainfall data
- Historical flood occurrence data
- Soil data
- Drainage and waterway data
- Population 