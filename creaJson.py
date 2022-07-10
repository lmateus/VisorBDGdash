import pandas as pd 
import dash_leaflet.express as dlx

file = pd.read_csv('exploracion.csv')
array_coord = file[['ID_EXPLORACION','X_wgs','Y_wgs']].values

sondeos = []   

for sondeo in array_coord:
    sondeos.append(dict(name=sondeo[0],lon=sondeo[2],lat=sondeo[1]))

geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in sondeos])
print(geojson)