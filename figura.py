from distutils.log import info
from statistics import mode
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import math
# Class created by me
from Extrae import ExtraeDatos

class GeneraFigura():
    def __init__(self,df_data,nombre):
        self.nombre = nombre
        self.df_data = df_data
    def figura(self):
        # Cargamos la informacion de una perforacion en especifico
        info_sondeo = ExtraeDatos(self.df_data,self.nombre)
        info_sondeo.ExtraeMuestras()
        # Cuantos ensayos tenemos?
        df_info_muestras = info_sondeo.muestras_sondeo
        numero_graficas = df_info_muestras.shape[1] 
        num_columns = 4
        num_filas = math.ceil(numero_graficas/num_columns)
        
        no_ensayos = len(list(df_info_muestras.columns))

        if no_ensayos == 0:
            self.fig = make_subplots(rows=1, cols=1 , vertical_spacing = 0.1)
            self.fig.add_trace(
                            go.Scatter(x=[0,0], y=[0,0] ,mode='markers'),
                            row=1, col=1
                        )
            self.fig.update_layout(title_text=f"El sondeo {self.nombre} no tiene muestras",height=900)
        else:
            self.fig = make_subplots(rows=num_filas, cols=num_columns , vertical_spacing = 0.1)
            # Contador campo en lista df_info_muestras.columns
            ensayos = list(df_info_muestras.columns)
            # Iteramos sobre las filas y las columnas del subplot para agregar los plot de cada ensayo de laboratorio     
            a = 0
            for i in range(num_filas):
                for j in range(num_columns):
                    if a < numero_graficas:
                        ensayo = ensayos[a]
                        self.fig.add_trace(
                            go.Scatter(x=df_info_muestras[ensayo], y=df_info_muestras['PROF_MEDIA_(m)'],mode='markers' ),
                            row=i+1, col=j+1
                        )
                        self.fig.update_xaxes(title_text=f"{ensayo}", row=i+1, col=j+1)
                        self.fig.update_yaxes(autorange="reversed", row=i+1, col=j+1)
                        
                        a = a + 1

            # Prueba de agregar la informacion del sondeo en el titulo:
            info_exp = self.df_data.get('EXPLORACION') 
            info_ubicacion = info_exp[info_exp['ID_EXPLORACION'] == self.nombre]
            sector = info_ubicacion['REF_SECTOR'].max()
            ubicacion = info_ubicacion['REF_UBICACION'].max()
            No_referencia = info_ubicacion['NO_REFERENCIA'].max()
            titulo = f"Informacion sondeo {self.nombre},<br> Sector {sector} Ubicacion {ubicacion},<br> No Referencia {No_referencia}"

            self.fig['layout']['yaxis']['autorange'] = "reversed"
            self.fig.update_layout(title_text=titulo,height=900)
            self.fig.update_layout(showlegend=False)

            # Intentamos agregar ensayos de campo
            df_campo = info_sondeo.campo_sondeo
            ensayos_campo = list(info_sondeo.campo_sondeo.columns)
        
            # Contador campo en lista df_info_muestras.columns
            ensayos_campo = list(df_campo.columns)
            # Iteramos sobre las filas y las columnas del subplot para agregar los plot de cada ensayo de laboratorio     
            a = 0
            num_ensayos_campo = len(ensayos_campo)
                        
            if num_ensayos_campo == 0:
                
                self.fig_2 = make_subplots(rows=1, cols=1 , vertical_spacing = 0.1)
                self.fig_2.add_trace(
                                go.Scatter(x=[0,0], y=[0,0] ,mode='markers'),
                                row=1, col=1
                            )
                self.fig_2.update_layout(title_text=f"El sondeo {self.nombre} no tiene campo",height=900)
            else:
                self.fig_2 = make_subplots(rows=num_ensayos_campo, cols=1 , vertical_spacing = 0.1)
                # Contador campo en lista df_info_muestras.columns
                ensayos_campo = list(df_campo.columns)
                # Iteramos sobre las filas y las columnas del subplot para agregar los plot de cada ensayo de laboratorio     
                a = 0
                for i in range(num_ensayos_campo):
                    for j in range(1):
                        if a < num_ensayos_campo:
                            ensayo = ensayos_campo[a]
                            self.fig_2.add_trace(
                                go.Scatter(x=df_campo[ensayo], y=df_campo['PROF_MEDIA_(m)'],mode='markers' ),
                                row=i+1, col=j+1
                            )
                            self.fig_2.update_xaxes(title_text=f"{ensayo}", row=i+1, col=j+1)
                            self.fig_2.update_yaxes(autorange="reversed", row=i+1, col=j+1)
                            
                            a = a + 1

                
                self.fig_2['layout']['yaxis']['autorange'] = "reversed"
                self.fig_2.update_layout(title_text=f"Campo {self.nombre}",height=900)
                self.fig_2.update_layout(showlegend=False)
                
                
                
            

            

            
        
        
        
        
        