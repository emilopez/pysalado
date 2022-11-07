import numpy as np
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
            if len(ultimo_registro)==0:
                metadataframe.loc[idx2,"fecha_ultimo_dato"] = ""
                metadataframe.loc[idx2,"ultimo_dato"] = ""
            else:    
                metadataframe.loc[idx2,"fecha_ultimo_dato"] = str(ultimo_registro.iat[0,0])
                metadataframe.loc[idx2,"ultimo_dato"] = str(ultimo_registro.iat[0,1])
    return metadataframe