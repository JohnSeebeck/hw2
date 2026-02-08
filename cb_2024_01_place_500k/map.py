import geopandas as gpd
import folium

places_shpfil = gpd.read_file("cb_2024_01_place_500k.shp")
print(places_shpfil)

places_reproj = places_shpfil.to_crs(epsg=4326)

places_shpfil.plot()