import pandas as pd
import plotly.graph_objects as go

class ExtraeDatos():
    '''Extraemos los datos de las hojas correspondientes
    Leemos una BDG en el formato SGC y filtramos por una exploracion de interes'''

    def __init__(self,df_data,nombre_exploracion):
        self.nombre_exp = nombre_exploracion
        self.df_data = df_data

    def ExtraeEstratos(self):
        #Leemos el archivo de la BDG en la pestana ESTRATO y filtramos por una exploracion
        file_estratos = self.df_data.get('ESTRATO')
        self.estratos_per_perf = file_estratos[file_estratos['ID_EXPLORACION']==self.nombre_exp]
        

        self.rectangle = go.Scatter(x=[0,10,10,0,0], y=[0,0,10,10,0], fill="toself")
        #self.rectangle2 = go.Scatter(x=[0,10,10,0,0], y=[10,10,15,10,0], fill="toself")
    def ExtraeMuestras(self):
        # Leemos el archivo de la BDF en la pestana MUESTRAS y filtramos por una exploracion
        file_muestras = self.df_data.get('MUESTRA')
        muestras_per_perf = file_muestras[file_muestras['ID_EXPLORACION']==self.nombre_exp]
        # Eliminamos las columnas de la muestra que estan vacias
        info_muestras = muestras_per_perf.dropna(how='all', axis=1)
        # Tambien hay unos campos que no nos interesa conocer
        campos_no_deseados = ['ID_MUESTRA', 'ID_ESTRATO', 'ID_EXPL_MUESTRA', 'ID_EXPLORACION', 'ID_ESTUDIO', 'ID_FUENTE', 'NO_ESTUDIO', 'NO_EXPLORACION',\
                            'TIPO_EXPLORACION', 'NO_ESTRATO', 'NO_MUESTRA', 'TRAMO_DESDE_(m)', 'TRAMO_HASTA_(m)', 'COORDENADA_X', 'COORDENADA_Y']
        # Buscamos solo los ensayos de laboratorio mirando la diferencia entre todas las columnas y los campos no deseados
        setA = set(info_muestras.columns)
        setB = set(campos_no_deseados)
        ensayos = list(setA.difference(campos_no_deseados))
        ensayos.sort()
        # El dataframe con solo los campos que tienen ensayos seria:
        self.muestras_sondeo = muestras_per_perf[ensayos]
                
        # Ahora buscamos los ensayos de campo que se tengan
        file_campo = self.df_data.get('CAMPO')
        campo_per_perf = file_campo[file_muestras['ID_EXPLORACION']==self.nombre_exp]
        info_campo = campo_per_perf.dropna(how='all', axis=1)
        # Hay campos que no nos interesa tener en el df para graficar
        campos_no_deseados_campo = ['ID_CAMPO', 'ID_ESTRATO', 'ID_EXPL_CAMPO', 'ID_EXPLORACION','ID_ESTUDIO', 'ID_FUENTE', 'NO_ESTUDIO', 'NO_EXPLORACION',\
                                    'TIPO_EXPLORACION', 'NO_ESTRATO', 'NO_ENSAYO', 'TIPO_ENSAYO', 'TRAMO_DESDE_(m)', 'TRAMO_HASTA_(m)', 'COORDENADA_X',\
                                     'COORDENADA_Y','N_(golpes-pie)']
        setC = set(info_campo.columns)
        setD = set(campos_no_deseados_campo)
        ensayos_campo = list(setC.difference(campos_no_deseados_campo))
        
        # El dataframe con solo los campos que tienen ensayos seria:
        self.campo_sondeo = campo_per_perf[ensayos_campo]
        print(f"El numero de ensayos de campo es {self.campo_sondeo.shape[0]}")

        
