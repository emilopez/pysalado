import funprono
import pandas as pd

alturas = pd.read_csv("datos/test_data.csv", decimal=",", sep=";")
print(alturas)

pronoR70 = funprono.get_prono_R70(alturas)

pronoR62 = funprono.get_prono_R62(alturas)
print(pronoR62)
