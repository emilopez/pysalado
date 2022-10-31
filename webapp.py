import funprono

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import datetime


#mapbox_access_token = open(".mapbox_token").read()
mapbox_access_token = st.secrets["mapbox_token"]

st.set_page_config(
     page_title="Pronóstico Río Salado",
     page_icon="❤️",
     layout="wide",
     initial_sidebar_state="collapsed",
)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

st.header("Río Salado - Sistema de Alerta Hidrológico - Pronósticos")

with st.sidebar:
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
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP70 + data_altura_rios.RP70, mode="markers+lines", name="Ruta 70"))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP62 + data_altura_rios.RP62, mode="markers+lines", name="Ruta 62"))

    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP39 + data_altura_rios.RP39, mode="markers+lines", name="RP 39"))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP02 + data_altura_rios.RP02, mode="markers+lines", name="RP 02"))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP04 + data_altura_rios.RP04, mode="markers+lines", name="RP 04"))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRN11 + data_altura_rios.RN11, mode="markers+lines", name="RN 11"))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroPTOSFE + data_altura_rios.PTOSFE, mode="markers+lines", name="Puerto SFe"))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP262 + data_altura_rios.RP262, mode="markers+lines", name="RP 262"))
    fig.add_trace(go.Scattergl(x=data_altura_rios.Fecha, y = ceroRP50S + data_altura_rios.RP50S, mode="markers+lines", name="RP 50S"))
    
    # Pronosticos
    # último día de mediciones
    last_date = pd.to_datetime(data_altura_rios.Fecha.values[-1])
    
    # 3 días de pronóstico para RP70
    tres = 3
    x_prono_RP70 = [last_date + datetime.timedelta(days=dia) for dia in range(1,tres+1)]
    yRP70_prono = np.array(funprono.get_prono_R70(data_altura_rios))
    
    # 2 dias de pronostico para RP62
    dos = 2
    x_prono_RP62 = [last_date + datetime.timedelta(days=dia) for dia in range(1,dos+1)]
    yRP62_prono = np.array(funprono.get_prono_R62(data_altura_rios))
    
    # trazas de pronosticos
    fig.add_trace(go.Scattergl(x=x_prono_RP70, y=ceroRP70 + yRP70_prono, mode="markers+lines", name="Prono R70"))
    fig.add_trace(go.Scattergl(x=x_prono_RP62, y=ceroRP62 + yRP62_prono, mode="markers+lines", name="Prono R62"))
    
    # DATAFRAMES con datos de pronostico
    values_prono_R70 = pd.DataFrame({"Día":[1, 2, 3], "Fecha":x_prono_RP70, "Altura h [m]": yRP70_prono, "Nivel H [m IGN]": ceroRP70 + yRP70_prono})
    values_prono_R70.set_index("Día")
    values_prono_R70["RMSE"] = pd.Series(funprono.RMSE_R70)
    values_prono_R70["H-RMSE"] = values_prono_R70["Nivel H [m IGN]"] - values_prono_R70["RMSE"]
    values_prono_R70["H+RMSE"] = values_prono_R70["Nivel H [m IGN]"] + values_prono_R70["RMSE"]

    values_prono_R62 = pd.DataFrame({"Día":[1, 2],"Fecha":x_prono_RP62, "Altura h [m]": yRP62_prono,"Nivel H [m IGN]": ceroRP62 + yRP62_prono})
    values_prono_R62.set_index("Día")
    values_prono_R62["RMSE"] = pd.Series(funprono.RMSE_R62)
    values_prono_R62["H-RMSE"] = values_prono_R62["Nivel H [m IGN]"] - values_prono_R62["RMSE"]
    values_prono_R62["H+RMSE"] = values_prono_R62["Nivel H [m IGN]"] + values_prono_R62["RMSE"]

    # Grafico bandas de error
    #  RP70
    fig.add_trace(go.Scatter(name='Banda superior', x = values_prono_R70['Fecha'], y = values_prono_R70["H+RMSE"],
        mode='lines', marker=dict(color="#444"), line=dict(width=0), showlegend=False),
    )
    fig.add_trace(go.Scatter(name='Banda inferior', x=values_prono_R70['Fecha'], y=values_prono_R70["H-RMSE"],
        marker=dict(color="#444"), line=dict(width=0), mode='lines', fillcolor='rgba(0, 88, 20, 0.2)', fill='tonexty', showlegend=False)
    )
    #  RP62
    fig.add_trace(go.Scatter(name='Banda superior', x = values_prono_R62['Fecha'], y = values_prono_R62["H+RMSE"],
        mode='lines', marker=dict(color="#444"), line=dict(width=0), showlegend=False),
    )
    fig.add_trace(go.Scatter(name='Banda inferior', x=values_prono_R62['Fecha'], y=values_prono_R62["H-RMSE"],
        marker=dict(color="#444"), line=dict(width=0), mode='lines', fillcolor='rgba(55, 0, 20, 0.2)', fill='tonexty', showlegend=False)
    )

    fig.update_layout(
        height =630,
        font  = dict(family = "Calibri", size = 20,),
        xaxis = dict(title = "Fecha", showline = True, showgrid = True, tickformat="%d/%m/%Y",tickfont = dict(family = 'Calibri')),
        yaxis = dict(title = "Nivel [m IGN]", showline = True, showgrid = True,tickfont = dict(family = 'Calibri')),
        legend = dict(orientation="h",yanchor="bottom", y=1),
        margin ={'l':0,'t':50,'b':0,'r':0},
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
        st.table(values_prono_R70.style.format({"Altura h [m]": "{:.2f}","Nivel [m IGN]": "{:.2f}", "H-RMSE":"{:.2f}", "H+RMSE":"{:.2f}"}))
    with c4.expander("Valores Pronosticados RP62"):
        st.table(values_prono_R62.style.format({"Altura h [m]": "{:.2f}","Nivel [m IGN]": "{:.2f}", "H-RMSE":"{:.2f}", "H+RMSE":"{:.2f}"}))

    c1, c2 = st.columns([2, 1])
    c1.plotly_chart(fig, use_container_width=True)
    with c1.expander("Ver datos telemétricos"):
        st.write(data_altura_rios)

    #---------------------------------------
    #       COLUMNA 2
    #---------------------------------------
    # LEO archivo de metadatos de estaciones
    estaciones_sah_df = pd.read_csv("datos/meta_estaciones_sah.csv", sep=";", decimal = ',')

    # agrega al dataframe ùltimas lecturas telemétricas a las estaciones del modelo
    estaciones_sah_df = funprono.add_data_to_metadata(estaciones_sah_df, data_altura_rios)

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
