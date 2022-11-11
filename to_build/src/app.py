# Autor: Emiliano Lopez <emiliano.lopez@gmail.com>
# Programa: PySalado v1.0.0
# Fecha: 11/11/2022

import os
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# --- funciones ---

# MLR Total
####################################################
#                RMSE para cada día de pronostico
####################################################
RMSE_R70 = [0.11, 0.21, 0.32]
RMSE_R62 = [0.08, 0.15]


##########################################
#                Ruta 70 COEFICIENTES
##########################################

# 1 DIA total
#   Coeficientes: [c1, c2, c3, c4, c5, c6, c7, b]
#   Predictores: [RP70(t), RP70(t-1), RP62(t), RP62(t-1), RP50S(t), RP50S(t-1), RN11(t), 1 ]
#   RP70(t+1) = c1 * RP70(t) + c2 * RP70(t-1) + c3 * RP62(t) + c4 * RP62(t-1) + c5 * RP50S(t) + c6 * RP50S(t-1) + c7 * RN11(t) + b 
#   RP70(t+1) = dot(coef, predictores)

# Coeficientes
coef_RP70_dia_1 = np.array([ 1.17413, # c1
                            -0.32751, # c2
                             0.18694, # c3
                            -0.08382, # c4
                             0.30954, # c5
                            -0.24036, # c6
                             0.04776, # c7
                            -0.12892])# b
# 2 DIAS total
# Coef: [c1, c2, c3, c4, c5, c6, c7, b]
# Predictores: RP70(t), RP70(t-1), RP62(t), RP62(t-2), RP50S(t), RP50S(t-1), RN11(t), 1  
coef_RP70_dia_2 = np.array([ 0.97744, # c1
                            -0.24272, # c2
                             0.42229, # c3
                            -0.24254, # c4
                             0.59380, # c5
                            -0.50060, # c6
                             0.08394, # c7
                            -0.21592])# b

# 3 DIAS total
# Coef: [c1, c2, c3, c4, c5, c6, c7, c8, b]
# Predictores: RP70(t), RP62(t), RP62(t-2), RP50S(t), RP50S(t-1), RN11(t), RN11(t-1), RP02(t), 1  
coef_RP70_dia_3 = np.array([ 0.65918, # c1
                             0.56498, # c2
                            -0.39852, # c3
                             0.67497, # c4
                            -0.58672, # c5
                             1.18960, # c6
                            -1.08753, # c7
                             0.05934, # c8
                            -0.43978])# b

###########################################
#                Ruta 62 COEFICIENTES
###########################################

# Coeficientes
# predictores: 
coef_RP62_dia_1 = np.array([ 1.20928, # c1
                            -0.29704, # c2
                             0.42301, # c3
                            -0.50108, # c4
                             0.14318, # c5
                             0.22558, # c6
                            -0.19703, # c7
                            -0.21601  ])# b
# 2 DIAS total
# Coef: [c1, c2, c3, c4, c5, c6, c7, b]
# Predictores:   
coef_RP62_dia_2 = np.array([ 0.97693, # c1
                            -0.21547, # c2
                             0.51801, # c3
                            -0.45941, # c4
                             0.35317, # c5
                            -0.28951, # c6
                             0.15197, # c7
                            -0.43172])# b

###########################################
#               REGRESIONES
###########################################

def compute_regression(coef, X):
    """Compute regressions, if any NaN value in X return []"""
    hay_NaN = np.sum(np.isnan(X))
    if not hay_NaN and (len(coef) == len(X)):
        prono = np.dot(coef, X)
    else:
        prono = np.nan
    return prono

def get_prono_R70(df, dias=3):
    def dia_1(df):
        """Predictores: RP70(t), RP70(t-1), RP62(t), RP62(t-1), RP50S(t), RP50S(t-1), RN11(t), 1 """
        X_RP70 = np.array(df[-2:]["RP70"][::-1].to_list()  + # [RP70(t), RP70(t-1)]
                          df[-2:]["RP62"][::-1].to_list()  + # [RP62(t), RP62(t-1)]
                          df[-2:]["RP50S"][::-1].to_list() + # [RP50S(t), RP50S(t-1)]
                          df[-1:]["RN11"].to_list()        + # [RN11(t)]
                          [1.0]                                              # 1: para coef independiente b
                          )
        return compute_regression(coef_RP70_dia_1, X_RP70)
    
    def dia_2(df):
        """Predictores: RP70(t), RP70(t-1), RP62(t), RP62(t-2), RP50S(t), RP50S(t-1), RN11(t), 1 """
        X_RP70 = np.array(df[-2:  ]["RP70" ][::-1].to_list()    + # [RP70(t), RP70(t-1)]
                          df[-3::2]["RP62" ][::-1].to_list()    + # [RP62(t), RP62(t-2)]
                          df[-2:  ]["RP50S"][::-1].to_list()    + # [RP50S(t), RP50S(t-1)]
                          df[-1:  ]["RN11" ].to_list()          + # [RN11(t)]
                          [1.0]                                                   # 1: para coef independiente b
                          )
        return compute_regression(coef_RP70_dia_2, X_RP70)
        
    def dia_3(df):
        """Predictores: RP70(t), RP62(t), RP62(t-2), RP50S(t), RP50S(t-1), RN11(t), RN11(t-1), RP02(t), 1 """
        X_RP70 = np.array(df[-1:  ]["RP70" ][::-1].to_list()    + # [RP70(t)]
                          df[-3::2]["RP62" ][::-1].to_list()    + # [RP62(t), RP62(t-2)]
                          df[-2:  ]["RP50S"][::-1].to_list()    + # [RP50S(t), RP50S(t-1)]
                          df[-2:  ]["RN11" ][::-1].to_list()    + # [RN11(t), RN11(t-1)]
                          df[-1:  ]["RP02" ].to_list()          + # [RP02(t)]
                          [1.0]                                                   # 1: para coef independiente b
                          )
        return compute_regression(coef_RP70_dia_3, X_RP70)
    
    if dias == 1:
        y_prono_R70 = [dia_1(df)]
    elif dias == 2:
        y_prono_R70 = [dia_1(df), dia_2(df)]
    elif dias == 3:
        y_prono_R70 = [dia_1(df), dia_2(df), dia_3(df)]
    else:
        y_prono_R70 = []
    return y_prono_R70

def get_prono_R62(df, dias=2):
    def dia_1(df):
        """Predictores (8): RP62(t), RP62(t-1), RP02(t), RP02(t-1), RP02(t-2), RP262(t), RP262(t-1), b"""
        X_RP62 = np.array(df[-2:]["RP62" ][::-1].to_list()    + # [RP62(t), RP62(t-1)]
                          df[-3:]["RP02" ][::-1].to_list()    + # [RP02(t), RP02(t-1), RP02(t-2)]
                          df[-2:]["RP262"][::-1].to_list()    + # [RP262(t), RP262(t-1)]
                          [1.0]                                 # 1: para coef independiente b
                          )
        return compute_regression(coef_RP62_dia_1, X_RP62)
    
    def dia_2(df):
        """Predictores (8): RP62(t), RP62(t-1), RP02(t), RP02(t-1), RP262(t), RP262(t-1), RP39(t), 1"""
        X_RP62 = np.array(df[-2:]["RP62" ][::-1].to_list()    + # [RP62(t), RP62(t-1)]
                          df[-2:]["RP02" ][::-1].to_list()    + # [RP02(t), RP02(t-1)]
                          df[-2:]["RP262"][::-1].to_list()    + # [RP262(t), RP262(t-1)]
                          df[-1:]["RP39" ].to_list()          + # [RP39] 
                          [1.0]                                 # 1: para coef independiente b
                          )
        return compute_regression(coef_RP62_dia_2, X_RP62)
    if dias == 1:
        y_prono_R62 = [dia_1(df)]
    elif dias >= 2:
        y_prono_R62 = [dia_1(df), dia_2(df)]
    return y_prono_R62

def add_data_to_metadata(metadataframe, dataframe):
    """Agrega últimos datos de altura al metadata frame, para visualizar en el mapa"""
    metadataframe["fecha_ultimo_dato"] = [""]*15
    metadataframe["ultimo_dato"]       = [""]*15

    # se agrega al dataframe de metadatos, la última fecha donde la estación tuvo datos y ese dato, caso contrario un NaN
    # voy a tener solamente de las estaciones usadas para el pronóstico, preguntar a Gustavo por la carga de datos

    for code in metadataframe['Codigo2']:
        try:
            d = dataframe[code]
        except:
            i = 1
        else:
            idx = d.notna()
            ultimo_registro = dataframe.loc[idx,['Fecha', code]][-1:] 
            idx2 = metadataframe['Codigo2'] == code
            if len(ultimo_registro)>0:    
                metadataframe.loc[idx2,"fecha_ultimo_dato"] = str(ultimo_registro.iat[0,0])
                metadataframe.loc[idx2,"ultimo_dato"] = str(ultimo_registro.iat[0,1])
    return metadataframe

# --- /funciones ---


#today_icon = random.choice(["🧉", "📉", "💧","🦩","🦟","🌎", "🇦🇷","🌅","🌉"]) #https://emojipedia.org/
st.set_page_config(
     page_title="Pronóstico Río Salado",
     page_icon="🇦🇷",
     layout="wide",
     initial_sidebar_state="expanded",
     #initial_sidebar_state="collapsed",
)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

mapbox_access_token = "pk.eyJ1IjoiZW1pbG9wZXoiLCJhIjoiY2swMTE1dTR0MHM4MDNkcDdwajY2eXEwOCJ9.2305I4WjeH4pUsVoif2XvA"
    

st.header("Río Salado - Sistema de Alerta Hidrológico - Pronósticos")

with st.sidebar:
    st.header("Acerca de PySalado")
    st.write("Programa:", "PySalado")
    st.write("Versión:",1.0)
    st.write("Fecha:", "11/11/2022")
    st.write("Autor:", "Mg. Ing. Emiliano P. López")
    st.write("Email:", "emiliano.lopez@gmail.com")

    st.header("Cotas Estaciones")
    ceroRP39   = st.number_input('Cero RP39',    value = 36.97) # Paso Las Piedras.
    ceroRP02   = st.number_input('Cero RP02',    value = 22.96) # San Justo
    ceroRP62   = st.number_input('Cero RP62',    value = 22.96) # Emilia
    ceroRP04   = st.number_input('Cero RP04',    value = 13.28) # Manucho
    ceroRP70   = st.number_input('Cero RP70',    value = 11.09) # Recreo
    ceroRN11   = st.number_input('Cero RN11',    value = 8.07)  # Santo Tomé
    ceroPTOSFE = st.number_input('Cero PTo SFe', value = 8.19)  # Riacho Santa Fe / Santa Fe
    ceroRP262  = st.number_input('Cero RP262',   value = 33.15) # Afluente Arroyo San Antonio / Petronilla
    ceroRP50S  = st.number_input('Cero RP50S',   value = 28.05) # Arroyo Cululu / Cululu


c1, c2, c3, c4 = st.columns([1.7,0.3,2.1,2.1])

uploaded_file = c1.file_uploader("Cargar archivo CSV [datos telemétricos]", type=["csv"])
desde_n_dias = c2.selectbox("Días previos", (7, 50, 100))
    

if uploaded_file is not None:
    
    # lectura archivo CSV
    data_altura_rios = pd.read_csv(uploaded_file, sep=";", parse_dates=["Fecha"], decimal = ',', comment="#", dayfirst=True)
    data_altura_rios = data_altura_rios[-desde_n_dias:]
    
    # trazas de alturas observadas telemetricamente
    fig = go.Figure()
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP70 + data_altura_rios.RP70, mode="markers+lines", name="Ruta 70",line=dict(color="dodgerblue")))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP62 + data_altura_rios.RP62, mode="markers+lines", name="Ruta 62",line=dict(color="salmon")))

    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP39 + data_altura_rios.RP39, mode="markers+lines", name="RP 39",line=dict(color="navy")))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP02 + data_altura_rios.RP02, mode="markers+lines", name="RP 02",line=dict(color="olive")))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP04 + data_altura_rios.RP04, mode="markers+lines", name="RP 04",line=dict(color="chocolate")))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRN11 + data_altura_rios.RN11, mode="markers+lines", name="RN 11",line=dict(color="lightgreen")))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroPTOSFE + data_altura_rios.PTOSFE, mode="markers+lines", name="Puerto SFe",line=dict(color="lightseagreen")))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP262 + data_altura_rios.RP262, mode="markers+lines", name="RP 262",line=dict(color="lightslategrey")))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP50S + data_altura_rios.RP50S, mode="markers+lines", name="RP 50S",line=dict(color="mediumvioletred")))
    
    # Pronosticos
    # último día de mediciones
    last_date = pd.to_datetime(data_altura_rios.Fecha.values[-1])
    
    # 3 días de pronóstico para RP70
    tres = 3
    x_prono_RP70 = [last_date + datetime.timedelta(days=dia) for dia in range(1,tres+1)]
    yRP70_prono = np.array(get_prono_R70(data_altura_rios))
    
    # 2 dias de pronostico para RP62
    dos = 2
    x_prono_RP62 = [last_date + datetime.timedelta(days=dia) for dia in range(1,dos+1)]
    yRP62_prono = np.array(get_prono_R62(data_altura_rios))
    
    # trazas de pronosticos
    fig.add_trace(go.Scattergl(x=x_prono_RP70, y=ceroRP70 + yRP70_prono, mode="markers+lines", name="Prono R70",line=dict(color="dodgerblue", width=3, dash='dot')))
    fig.add_trace(go.Scattergl(x=x_prono_RP62, y=ceroRP62 + yRP62_prono, mode="markers+lines", name="Prono R62",line=dict(color="salmon", width=3, dash='dot')))
    
    # DATAFRAMES con datos de pronostico
    values_prono_R70 = pd.DataFrame({"Día":[1, 2, 3], "Fecha":x_prono_RP70, "Altura h [m]": yRP70_prono, "Nivel H [m IGN]": ceroRP70 + yRP70_prono})
    values_prono_R70.set_index("Día")
    values_prono_R70["RMSE"] = pd.Series(RMSE_R70)
    values_prono_R70["H-RMSE"] = values_prono_R70["Nivel H [m IGN]"] - values_prono_R70["RMSE"]
    values_prono_R70["H+RMSE"] = values_prono_R70["Nivel H [m IGN]"] + values_prono_R70["RMSE"]

    values_prono_R62 = pd.DataFrame({"Día":[1, 2],"Fecha":x_prono_RP62, "Altura h [m]": yRP62_prono,"Nivel H [m IGN]": ceroRP62 + yRP62_prono})
    values_prono_R62.set_index("Día")
    values_prono_R62["RMSE"] = pd.Series(RMSE_R62)
    values_prono_R62["H-RMSE"] = values_prono_R62["Nivel H [m IGN]"] - values_prono_R62["RMSE"]
    values_prono_R62["H+RMSE"] = values_prono_R62["Nivel H [m IGN]"] + values_prono_R62["RMSE"]

    # Grafico bandas de error
    #  RP70
    fig.add_trace(go.Scatter(name='Banda superior', x = values_prono_R70['Fecha'], y = values_prono_R70["H+RMSE"],
        mode='lines', marker=dict(color="#444"), line=dict(width=0), showlegend=False),
    )
    fig.add_trace(go.Scatter(name='Banda inferior', x=values_prono_R70['Fecha'], y=values_prono_R70["H-RMSE"],
        marker=dict(color="#444"), line=dict(width=0), mode='lines', fillcolor='rgba(0, 88, 20, 0.4)', fill='tonexty', showlegend=False)
    )
    #  RP62
    fig.add_trace(go.Scatter(name='Banda superior', x = values_prono_R62['Fecha'], y = values_prono_R62["H+RMSE"],
        mode='lines', marker=dict(color="#444"), line=dict(width=0), showlegend=False),
    )
    fig.add_trace(go.Scatter(name='Banda inferior', x=values_prono_R62['Fecha'], y=values_prono_R62["H-RMSE"],
        marker=dict(color="#444"), line=dict(width=0), mode='lines', fillcolor='rgba(55, 0, 20, 0.4)', fill='tonexty', showlegend=False)
    )

    fig.update_layout(
        height =630,
        font  = dict(family = "Calibri", size = 20,),
        xaxis = dict(title = "Fecha", showline = True, showgrid = True, tickformat="%d/%m/%Y",tickfont = dict(family = 'Calibri')),
        yaxis = dict(title = "Nivel [m IGN]", showline = True, showgrid = True,tickfont = dict(family = 'Calibri')),
        legend = dict(orientation="h",yanchor="bottom", y=1),
        margin ={'l':0,'t':100,'b':0,'r':0},
        hovermode="x"
    )
    # show
    values_prono_R70['Fecha'] = pd.to_datetime(values_prono_R70['Fecha']).dt.strftime('%d/%m/%Y')
    values_prono_R62['Fecha'] = pd.to_datetime(values_prono_R62['Fecha']).dt.strftime('%d/%m/%Y')
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    with c3.expander("Valores Pronosticados RP70"):
        st.table(values_prono_R70.style.format({"Altura h [m]": "{:.2f}","Nivel H [m IGN]": "{:.2f}", "RMSE":"{:.2f}", "H-RMSE":"{:.2f}", "H+RMSE":"{:.2f}"}))
    with c4.expander("Valores Pronosticados RP62"):
        st.table(values_prono_R62.style.format({"Altura h [m]": "{:.2f}","Nivel H [m IGN]": "{:.2f}", "RMSE":"{:.2f}", "H-RMSE":"{:.2f}", "H+RMSE":"{:.2f}"}))

    c1, c2 = st.columns([2, 1])
    c1.plotly_chart(fig, use_container_width=True)
    with c1.expander("Ver datos telemétricos"):
        st.write(data_altura_rios)

    #---------------------------------------
    #       COLUMNA 2
    #---------------------------------------
    # LEO archivo de metadatos de estaciones
    meta_estaciones_sah = os.path.join(os.path.dirname(__file__), "datos", "meta_estaciones_sah.csv")
    estaciones_sah_df = pd.read_csv(meta_estaciones_sah, sep=";", decimal = ',')

    # agrega al dataframe ùltimas lecturas telemétricas a las estaciones del modelo
    estaciones_sah_df = add_data_to_metadata(estaciones_sah_df, data_altura_rios)

    # creo mapa plotly
    estaciones_sah_map = go.Scattermapbox(mode = "markers", lon = estaciones_sah_df["lng"], lat = estaciones_sah_df["lat"], marker = {'size': 10}, name = "",
                                        hovertemplate =   "<b>" + estaciones_sah_df["Nombre"] + "</b><br><br>" +
                                                        "Coord: %{lon},%{lat}<br>"+
                                                        "Río: " + estaciones_sah_df["Rio"] + "<br>" +
                                                        "Ruta: "+ estaciones_sah_df["Ruta"] +"<br>" +
                                                        "Descripción:" + estaciones_sah_df["Descripción"] + "<br><br>" + 
                                                        "Último dato (Altura h [m]): " + estaciones_sah_df["ultimo_dato"] + "<br>" + 
                                                        "Fecha: " + estaciones_sah_df["fecha_ultimo_dato"] 
                                        )
    layout = go.Layout(
        #title = "Estaciones SAH",
        title_x=0.5,
        title_y=0.95,
        width=400, height=630, 
        margin ={'l':0,'t':50,'b':0,'r':0},
        mapbox = {
            'accesstoken':mapbox_access_token,
            'center': {'lat': -30.3, 'lon': -61},
            'style': "satellite-streets",
            'zoom': 7})
    figure = go.Figure(data=[estaciones_sah_map], layout=layout)
    # show mapa 
    c2.plotly_chart(figure, use_container_width=True)
    with c2.expander("Ver datos estaciones"):
        st.write(estaciones_sah_df)
