import pandas as pd
from scipy import stats
from tabulate import tabulate

pt = pd.read_csv("canciones_1960-2023.csv")

def convert_min_sec_to_ms(min_sec):
    parts = min_sec.split()
    minutes = int(parts[0])
    seconds = int(parts[2])
    return (minutes * 60 + seconds) * 1000

def convert_ms_to_min_sec(ms):
    seconds = ms / 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{int(minutes)} minutos {int(seconds)} segundos"

# Convierte la duración a milisegundos si no lo has hecho ya.
pt['Track Duration (ms)'] = pt['Track Duration (ms)'].apply(convert_min_sec_to_ms)

# Crea una columna 'Decade' para representar las décadas de lanzamiento.
pt['Decade'] = ((pt['Year_release'] // 10) * 10).astype(str) + 's'

# Realiza un ANOVA para comparar la duración entre las décadas.
decade_groups = [group['Track Duration (ms)'] for name, group in pt.groupby('Decade')]
f_statistic, p_value = stats.f_oneway(*decade_groups)

# Define el nivel de significancia (alfa)
alfa = 0.05

# Determina si la hipótesis nula es verdadera o no
if p_value < alfa:
    conclusion = "Rechazamos la hipótesis nula. Existe una diferencia significativa en la duración de las canciones entre las décadas, por lo tanto si van aumentando los minutos de las canciones."
else:
    conclusion = "No tenemos evidencia suficiente para rechazar la hipótesis nula. No hay una diferencia significativa en la duración de las canciones entre las décadas."

# Imprime los resultados en forma tabular
result_table = [["Estadística F", f_statistic], ["Valor p", p_value], ["Conclusión", conclusion]]
table = tabulate(result_table, headers=["Resultado", "Valor"], tablefmt="pretty")
print(table)





