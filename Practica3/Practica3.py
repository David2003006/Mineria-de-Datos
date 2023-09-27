import pandas as pd

ruta = "canciones_1960-2023.csv"
df = pd.read_csv(ruta, encoding='ISO-8859-1')

# Función para convertir milisegundos a "X minutos X segundos"
def convert_ms_to_min_sec(ms):
    seconds = ms / 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{int(minutes)} minutos {int(seconds)} segundos"

# Función para convertir "X minutos X segundos" a milisegundos
def convert_min_sec_to_ms(min_sec):
    parts = min_sec.split()
    minutes = int(parts[0])
    seconds = int(parts[2])
    return (minutes * 60 + seconds) * 1000

# Encuentra el índice de la fila con el valor mínimo en la columna 'Popularity'
indice_min_popularity = df["Popularity"].idxmin()

# Encuentra el índice de la fila con el valor máximo en la columna 'Popularity'
indice_max_popularity = df["Popularity"].idxmax()

#Estoy sacanado la moda de duracion de las canciones a lo largo del tiempo
df['Duration (ms)'] = df['Track Duration (ms)'].apply(convert_min_sec_to_ms)
moda_duracion_ms = df['Duration (ms)'].mode().values[0]
moda_duracion = convert_ms_to_min_sec(moda_duracion_ms)

#El promedio de duracion de una cancion y su popularidad desde 1960-2023
df['Duration (ms)']= df['Track Duration (ms)'].apply(convert_min_sec_to_ms)
promedio_duracion_ms= df['Duration (ms)'].mean()
promedio_duracion= convert_ms_to_min_sec(promedio_duracion_ms)

# Obtiene los nombres de las canciones correspondientes a los índices encontrados
nombre_cancion_min_popularity = df.loc[indice_min_popularity, "Track Name"]
nombre_cancion_max_popularity = df.loc[indice_max_popularity, "Track Name"]

moda_duracion = df["Track Duration (ms)"].mode().values[0]

artista_menos_popular= df.loc[indice_min_popularity, "Artist Name(s)"]
artista_mas_popular= df.loc[indice_max_popularity, "Artist Name(s)"]

#varianza en la columna de rack Duration (ms)
varianza = df['Duration (ms)'].var()
nueva_varianza=convert_ms_to_min_sec(varianza)

# Calcula la matriz de covarianza entre 'Popularity' y 'Track Duration (ms)'
df['Track Duration (ms)'] = df['Track Duration (ms)'].apply(convert_min_sec_to_ms)
covarianza = df[['Popularity', 'Track Duration (ms)']].cov()

# Obtén el valor de covarianza entre estas dos columnas
covarianza_popularity_duration = covarianza.loc['Popularity', 'Track Duration (ms)']
covarianza_popularity_duration_redondeada = round(covarianza_popularity_duration, 2)


print("La canción con la popularidad más baja es:", nombre_cancion_min_popularity)
print("La canción con la popularidad más alta es:", nombre_cancion_max_popularity)

print("el artista menos escuchado es:", artista_menos_popular)
print("el artista mas escuchado es:", artista_mas_popular)

print("La moda para que dure una cancion es de:", moda_duracion)

print("El promedio de duracion de una cancion es de:", promedio_duracion)

print("La varianza de la columna Track Duration (ms) es de :", nueva_varianza )

print("La covarianza entre 'Popularity' y 'Track Duration (ms)' es :", covarianza_popularity_duration_redondeada)