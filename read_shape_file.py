import geopandas
import pandas as pd
import folium
import itertools
from operator import itemgetter
import numpy as np
from scipy.spatial import cKDTree
from shapely.geometry import Point, LineString
import geojson


def ckdnearest(gdfA, gdfB, gdfB_cols=['Place']):
    A = np.concatenate(
        [np.array(geom.coords) for geom in gdfA.geometry.to_list()])
    B = [np.array(geom.coords) for geom in gdfB.geometry.to_list()]
    B_ix = tuple(itertools.chain.from_iterable(
        [itertools.repeat(i, x) for i, x in enumerate(list(map(len, B)))]))
    B = np.concatenate(B)
    ckd_tree = cKDTree(B)
    dist, idx = ckd_tree.query(A, k=1)
    idx = itemgetter(*idx)(B_ix)
    gdf = pd.concat(
        [gdfA, gdfB.loc[idx, gdfB_cols].reset_index(drop=True), pd.Series(dist, name='dist')], axis=1)
    return gdf
  
def df_to_geojson(df, properties, lat='jetson_rpi_lat', lon='jetson_rpi_lng'):
    df.fillna(0, inplace=True)
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature','properties':{},'geometry':{'type':'Point','coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

#sert location file to use
location = 'maryland'
#Load route from rpi file
df = pd.read_csv("master_log.csv")
geoj = df_to_geojson(df, [])
with open('{}.geojson'.format(location), 'w+') as f:
  f.write(geojson.dumps(geoj))
  f.close()
#convert rpi lat/lon to geopandas points
rpi_route = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df['jetson_rpi_lat'], df['jetson_rpi_lng']))
#load shape file
geodf = geopandas.read_file(f"{location}.shp")
# get min and max coordinates of rpi route
ymin = df['jetson_rpi_lat'].max()
ymax = df['jetson_rpi_lat'].min()
xmin = df['jetson_rpi_lng'].max()
xmax = df['jetson_rpi_lng'].min()
#crop shape file to fit route
cropped_map_data = geodf.cx[xmin:xmax, ymin:ymax]
#convert geodataframe to folium map
c = ckdnearest(rpi_route, geodf)
c.to_csv('test.csv')
map = cropped_map_data.explore()
#Iterate through rpi points and create polyline
loc = []
for i in range(len(df)):
  if abs(df['jetson_rpi_lat'][i]) >=1 and abs(df['jetson_rpi_lng'][i]) >= 1:
    loc.append((df['jetson_rpi_lat'][i], df['jetson_rpi_lng'][i]))
  else:
    pass
line = folium.PolyLine(loc, weight=5, color='red')
#add polyline to map
line.add_to(map)
#convert map to html
html_string = map.get_root().render()
#write html to file
output_file = open("output.html","w+")
output_file.write(html_string)
output_file.close()


########### Old Commands #############
# print(geodf.columns.tolist())
# print(geodf.head(10))
# geodf.to_csv(f"{location}.csv")
# rpi_route.to_csv(f"rpi_route.csv")
# sf = shapefile.Reader(f"{location}.shp")
# records = sf.records()
# print(records)


# #zip the coordinates into a point object and convert to a GeoData Frame
# geometry = [Point(xy) for xy in zip(df['jetson_rpi_lat'], df['jetson_rpi_lng'])]
# geo_df = geopandas.GeoDataFrame(df, geometry=geometry)

# geo_df2 = geo_df.groupby(df.index / 2)['geometry'].apply(lambda x: LineString(x.tolist()))
# geo_df2 = geopandas.GeoDataFrame(geo_df2, geometry='geometry')
# geo_df2.to_file("df2.csv")

# folium.PolyLine(location=[df['jetson_rpi_lat'][i], df['jetson_rpi_lng'][i]], weight=5, color='red').add_to(map)
# folium.CircleMarker(location=[df['jetson_rpi_lat'][0], df['jetson_rpi_lng'][0]], radius=5, color='red').add_to(map)
# MULTILINESTRING ((-77.3012729 39.1500298, -77.3009974 39.1501898), (-77.3009974 39.1501898, -77.3003327 39.1505764), (-77.3003327 39.1505764, -77.2999789 39.1507678), (-77.2999789 39.1507678, -77.2996428 39.1509152), (-77.2996428 39.1509152, -77.2993557 39.1510284), (-77.2993557 39.1510284, -77.2989717 39.1511593), (-77.2989717 39.1511593, -77.2982319 39.1513945), (-77.2982319 39.1513945, -77.2976083 39.1515928), (-77.2976083 39.1515928, -77.2973074 39.151705), (-77.2973074 39.151705, -77.2970808 39.1518046), (-77.2970808 39.1518046, -77.2968667 39.151912), (-77.2968667 39.151912, -77.2966313 39.152037), (-77.2966313 39.152037, -77.2964717 39.1521341), (-77.2964717 39.1521341, -77.2962888 39.1522646), (-77.2962888 39.1522646, -77.296239 39.1523001))
# fig, ax = plt.subplots()
# file.plot()
# plt.show()
# plt.savefig('MD.svg', dpi='figure', format='svg')