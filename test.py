from turtle import width
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Output, Input, dash_table
import dash_leaflet as dl
from mapa import GeneraMapa
from figura import GeneraFigura
from generaTabla import GeneraTabla
import pandas as pd

file_1 = 'Plantilla_BDG 2022_VF.xlsx'
file_2 = './../BDG_Tunja/InfoMS/BDG_Tunja_Norte.xlsx'
df_data = pd.read_excel(file_2,sheet_name=['ESTRATO','MUESTRA','CAMPO','EXPLORACION'])

nombre_sondeo = 'UPT1P1'

X = GeneraMapa(df_data)
X.mapa_exploraciones()

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([
                    dbc.Row([X.mapa]),
                    dbc.Row(dbc.Col(html.H3(),id='tabla_sondeo'))
                ],width=5),
                
                dbc.Col(dbc.Col(html.H3(),id='info_sondeo'),width=5),
                dbc.Col(dbc.Col(html.H3(),id='info_campo'),width=2)
            ]
        ),
    ]
)
app.layout = row

# Pruebas de callback graph
@app.callback(Output("info_sondeo", "children"), [Input("geojson", "click_feature")])
def capital_click(feature):
    if feature is not None:
        #return f"You clicked {feature['properties']['name']}"
        Y = GeneraFigura(df_data,feature['properties']['name'])
        Y.figura()
        a = dbc.Col(dcc.Graph(figure=Y.fig))
        return a

@app.callback(Output("tabla_sondeo", "children"), [Input("geojson", "click_feature")])
def capital_click(feature):
    if feature is not None:
        #return f"You clicked {feature['properties']['name']}"
        Z = GeneraTabla(df_data,feature['properties']['name'])
        Z.tabla()
        b = dbc.Col(Z.dict_tabla)
        return b

@app.callback(Output("info_campo", "children"), [Input("geojson", "click_feature")])
def capital_click(feature):
    if feature is not None:
        #return f"You clicked {feature['properties']['name']}"
        W = GeneraFigura(df_data,feature['properties']['name'])
        print(feature)
        W.figura() 
        try:
            return dbc.Col(dcc.Graph(figure=W.fig_2))
        except:
            return html.H6('Problemas'+feature['properties']['name'])

if __name__ == '__main__':
    app.run_server(debug=True)