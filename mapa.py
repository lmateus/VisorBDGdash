import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import assign
import pandas as pd
from pyproj import Proj, transform
import numpy as np


class GeneraMapa():
    def __init__(self,df_data):

        self.df_data = df_data

        file_exploracion = self.df_data.get('EXPLORACION')
        X_coord = file_exploracion['COORDENADA_X']
        Y_coord = file_exploracion['COORDENADA_Y']

        df_random =  pd.Series(np.random.randn(172)) * 10
        print(df_random)

        X_coord_al = X_coord #+ df_random
        Y_coord_al = Y_coord #+ df_random

        #sistema_BDG = 'epsg:9377'
        sistema_BDG = 'epsg:3116'
        sistema_wgs = 'epsg:4326'
        inProj = Proj(init=sistema_BDG)
        outProj = Proj(init=sistema_wgs)
        x1,y1 = X_coord_al,Y_coord_al
        x2,y2 = transform(inProj,outProj,x1,y1)

        file_exploracion['X_wgs'] = x2
        file_exploracion['Y_wgs'] = y2

        #file_exp = pd.read_csv('exploracion.csv')
        array_coord = file_exploracion[['ID_EXPLORACION','X_wgs','Y_wgs']].values
        print (f"Se cambiaron las coordenadas de {sistema_BDG} a {sistema_wgs}")
        sondeos = []   

        for i in range(len(array_coord)):
            sondeo = array_coord[i]
            latitud = sondeo[2]
            longitud = sondeo[1]
            
            sondeos.append(dict(name=sondeo[0],lon=longitud,lat=latitud))

        self.geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in sondeos])
        print('**********')
        print(f'el numero de sondeos es {len(sondeos)}')



    def mapa_exploraciones(self):
        url = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
        attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '

        self.mapa = html.Div([
            dl.Map(children=[
                dl.TileLayer(url,attribution),
                dl.GeoJSON(data=self.geojson, id="geojson")
                ], style={'width': '95%', 'height': '500px','marginLeft': 20, 'marginTop': 25}, center=(5.544477, -73.357466), zoom=14),
            ])
