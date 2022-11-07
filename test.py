import funprono
import pandas as pd
import numpy as np

def test_pronosticos():
    """ Testeo que los pronosticos se generen bien con datos faltantes

        Paso dataframe con menos filas para ver el resultado. 
    """
    alturas = pd.read_csv("datos/test_data2.csv", decimal=",", sep=";", comment="#")

    # Test pronosticos con datos completos a insuficientes
    for i in range(len(alturas)+1):
        print(f"Datos menos {i} filas")
        print("=====================")
        pronoR70 = funprono.get_prono_R70(alturas[i:])
        pronoR62 = funprono.get_prono_R62(alturas[i:])

        print("Dataset")
        print(alturas[i:])

        print("Pronostico RP 70: ", end="")
        print(np.array(pronoR70))

        print("Pronostico RP 62: ", end="")
        print(np.array(pronoR62))
        print()

def test_mapa():
    # test mapas
    alturas = pd.read_csv("datos/test_data4.csv", decimal=",", sep=";", comment="#")
    # LEO archivo de metadatos de estaciones
    estaciones_sah_df = pd.read_csv("datos/meta_estaciones_sah.csv", sep=";", decimal = ',')

    # agrega al dataframe ùltimas lecturas telemétricas a las estaciones del modelo
    estaciones_sah_df = funprono.add_data_to_metadata(estaciones_sah_df, alturas)

    print(estaciones_sah_df)

#test_mapa()
test_pronosticos()