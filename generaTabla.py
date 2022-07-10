import pandas as pd
from Extrae import ExtraeDatos
from dash import dash_table

class GeneraTabla():
    def __init__(self,df_data,nombre):
        self.nombre = nombre
        self.df_data = df_data
    def tabla(self):
        # Cargamos la informacion de una perforacion en especifico
        info_sondeo = ExtraeDatos(self.df_data,self.nombre)
        info_sondeo.ExtraeEstratos()
        self.df_info_estratos = info_sondeo.estratos_per_perf
        
        self.df_info_estratos = self.df_info_estratos[['TRAMO_DESDE_(m)','TRAMO_HASTA_(m)','CLASIF_USCS','Descripción']]
        #self.dict_tabla = tabla_html.to_dict('records'), [{"name": i, "id": i} for i in tabla_html.columns]
        self.dict_tabla = dash_table.DataTable(self.df_info_estratos.to_dict('records'), [{"name": i, "id": i} for i in self.df_info_estratos.columns], 
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'lineHeight': '15px'
        },
        style_table={'minWidth': '100%'},
        style_cell={'textAlign': 'left'} )

