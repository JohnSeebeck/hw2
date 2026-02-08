import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np
import cartopy.feature as cfeature
from shapely.geometry import Point, Polygon, LineString

places = gpd.read_file("cb_2024_01_place_500k.shp").to_crs(epsg=3857)

perimeters = places.length
areas = places.area

places['circularity'] = (4 * np.pi * areas) / (perimeters**2)

circs = places[['NAME', 'circularity']]

map_proj = ccrs.LambertConformal(central_longitude=-86.5, central_latitude=32.5)
data_proj = ccrs.PlateCarree()

fig = plt.figure(figsize=(10, 12), facecolor='black')
ax = fig.add_subplot(1, 1, 1, projection=map_proj)
ax.set_facecolor('black')

thres1 = 0.2
thres2 = 0.4
thres3 = 0.6
thres4 = 0.8

places_reproj = places.to_crs(epsg=4326)
very_high_circ = places_reproj[places_reproj['circularity'] > thres4]
other_circ1 = places_reproj[places_reproj['circularity'] <= thres4]
high_circ = other_circ1[other_circ1['circularity'] > thres3]
other_circ2 = other_circ1[other_circ1['circularity'] <= thres3]
medium_circ = other_circ2[other_circ2['circularity'] > thres2]
other_circ3 = other_circ2[other_circ2['circularity'] <= thres2]
low_circ = other_circ3[other_circ3['circularity'] > thres1]
very_low_circ = other_circ3[other_circ3['circularity'] <= thres1]

ax.add_feature(cfeature.STATES.with_scale('10m'), edgecolor='white', linewidth=1.5)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_geometries(very_high_circ.geometry, crs=data_proj, facecolor='red', alpha=0.4)
ax.add_geometries(high_circ.geometry, crs=data_proj, facecolor='orange', alpha=0.4)
ax.add_geometries(medium_circ.geometry, crs=data_proj, facecolor='yellow', alpha=0.4)
ax.add_geometries(low_circ.geometry, crs=data_proj, facecolor='green', alpha=0.4)
ax.add_geometries(very_low_circ.geometry, crs=data_proj, facecolor='blue', alpha=0.4)

plt.style.use('dark_background')
ax.set_extent([-88.5, -84.8, 30.1, 35.1], crs=data_proj)
plt.show()