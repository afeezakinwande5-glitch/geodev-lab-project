# Data Notes

## 1. Abeokuta South LGA Boundary

* **Source**: GRID3
* **URL**: https://data.grid3.org
* **Downloaded**: 13 September 2026
* **Format**: Shapefile
* **Features**: 1
* **Columns**: ward_code, ward_name, state
* **Nulls**: Not yet assessed
* **Geometry**: MultiPolygon
* **CRS**: WGS 84 / EPSG:4326
* **Coverage**: Abeokuta South LGA, Ogun State, Nigeria
* **Purpose**: Defines the study area for the project.
* **Notes**: GRID3 administrative boundary data selected to define the study area. Dataset version should be confirmed.

## 2. OSM Waterways/Drainage, extracted via QuickOSM

* **Source**: OpenStreetMap
* **Extraction method**: QuickOSM
* **Query**: waterway within Abeokuta South LGA extent
* **Extracted**: 13 September 2026
* **Format**: GeoPackage
* **Features**: 15
* **Columns**: osm_id, name, waterway, layer, bridge, tunnel
* **Nulls**: Some name and waterway-related attributes may be empty; exact count not assessed
* **Geometry**: Line
* **CRS**: WGS 84 / EPSG:4326 
* **Coverage**: Expected to show mapped waterways within and around the study area; completeness not yet assessed
* **Notes**: OpenStreetMap is crowdsourced. Some waterways or drainage features may be missing or incompletely mapped.

## 3. OSM Buildings/Settlements, extracted via QuickOSM

* **Source**: OpenStreetMap
* **Extraction method**: QuickOSM
* **Query**: building within Abeokuta South LGA extent
* **Extracted**: 13 September 2026
* **Format**: GeoPackage
* **Features**: To be confirmed in QGIS
* **Columns**: osm_id, building, name, addr_street, addr_housenumber 
* **Nulls**: Many buildings may have no name or address attributes; exact count not assessed
* **Geometry**: Polygon
* **CRS**: WGS 84 / EPSG:4326
* **Coverage**: Expected to be denser in built-up areas; completeness not yet assessed
* **Notes**: Building coverage may be incomplete because OpenStreetMap data is crowdsourced. Some building features may have no name or address information.

## 4. OSM Roads, extracted via QuickOSM

* **Source**: OpenStreetMap
* **Extraction method**: QuickOSM
* **Query**: highway within Abeokuta South LGA extent
* **Extracted**: 13 September 2026
* **Format**: GeoPackage
* **Features**: 20566
* **Columns**: osm_id, highway, name, surface, oneway, maxspeed
* **Nulls**: Some roads may lack name, surface, or speed-limit information; exact count not assessed
* **Geometry**: Line
* **CRS**: WGS 84 / EPSG:4326
* **Coverage**: Expected to be denser in built-up areas; completeness not yet assessed
* **Notes**: Road coverage and attributes may be incomplete in some areas because OpenStreetMap is crowdsourced. Some roads may not have surface or name tags.

## 5. Copernicus DEM

* **Source**: Copernicus Data Space Ecosystem
* **URL**: https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM
* **Downloaded**: 13 September 2026
* **Format**: GeoTIFF
* **Resolution**: 30 m
* **CRS**: WGS 84 
* **Elevation units**: Metres
* **Coverage**: Intended to cover Abeokuta South study area; verify raster extent
* **Purpose**: Provides elevation data for terrain and flood-related analysis.
* **Notes**: The DEM may not capture small-scale terrain features, drainage structures, or local elevation variations. Confirm the product resolution and CRS from the downloaded file.

## 6. WorldPop Population 2026

* **Source**: WorldPop
* **URL**: https://www.worldpop.org/
* **Region**: Nigeria
* **Year**: 2026
* **Date of production**: 2025-09-01
* **Version**: R2025A v1
* **Format**: GeoTIFF
* **Resolution**: 3 arc-seconds
* **CRS**: WGS84
* **Units**: Number of people per pixel
* **Mapping approach**: Random Forest-based dasymetric redistribution
* **Purpose**: Estimates the population potentially exposed to flood risk.
* **Notes**: Alpha-version dataset that may be updated. Population values are modelled estimates, not direct headcounts.
* **DOI**: 10.5258/SOTON/WP00839