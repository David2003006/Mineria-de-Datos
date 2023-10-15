import pandas as pd
import matplotlib.pyplot as plt

df= pd.read_csv("canciones_1960-2023.csv")

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

# Agrupar por año de lanzamiento y emoción, calculando el promedio de la popularidad
grouped = df.groupby(['Year_release', 'Emocionalidad'])['Popularity'].mean().reset_index()

# Crear un gráfico de dispersión para cada emoción
emotions = ['Triste', 'Feliz', 'Neutro']
colors = ['red', 'blue', 'green']

plt.figure(figsize=(12, 6))

for i, emotion in enumerate(emotions):
    data = grouped[grouped['Emocionalidad'] == emotion]
    plt.scatter(data['Year_release'], data['Popularity'], label=emotion, color=colors[i])

plt.xlabel('Año de Lanzamiento')
plt.ylabel('Promedio de Popularidad')
plt.title('Dispersión de Emocionalidad vs. Popularidad a lo largo del tiempo')
plt.legend()
plt.grid(True)
plt.savefig('grafico_dispersion_emociones.jpg', format='jpg')
plt.show()

# Aplicar la función para convertir a milisegundos
df['Track Duration (ms)'] = df['Track Duration (ms)'].apply(convert_min_sec_to_ms)

# Filtra los datos para incluir solo las filas con popularidad 0, 25, 50, 75 o 100
filtered_data = df[df['Popularity'].isin([0, 25, 50, 75, 100])]

# Agrupar por popularidad y año de lanzamiento, calculando el promedio de la duración en milisegundos
grouped = filtered_data.groupby(['Popularity', 'Year_release'])['Track Duration (ms)'].mean().reset_index()

# Convierte el promedio de milisegundos nuevamente al formato "minutos segundos"
grouped['Track Duration (minutos_segundos)'] = grouped['Track Duration (ms)'].apply(convert_ms_to_min_sec)

plt.figure(figsize=(12, 6))

# Crear un gráfico de dispersión para cada nivel de popularidad
popularities = filtered_data['Popularity'].unique()

for popularity in popularities:
    data = grouped[grouped['Popularity'] == popularity]
    plt.scatter(data['Year_release'], data['Track Duration (minutos_segundos)'], label=f'Popularity {popularity}')

# Limita la cantidad de etiquetas en el eje Y a 5
plt.yticks(plt.yticks()[0][::len(plt.yticks()[0]) // 5])

plt.xlabel('Año de Lanzamiento')
plt.ylabel('Promedio de Duración (minutos segundos)')
plt.title('Dispersión de Duración Promedio vs. Año de Lanzamiento por Popularidad')
plt.legend(title='Popularidad')
plt.grid(True)
plt.savefig('Promedio_de_minutos_limitado.jpg', format='jpg')
plt.show()