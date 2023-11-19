import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans

df = pd.read_csv('canciones_1960-2023.csv')

def convert_min_sec_to_ms(min_sec):
    parts = min_sec.split()
    minutes = int(parts[0])
    seconds = int(parts[2])
    return (minutes * 60 + seconds) * 1000

df['Track Duration (ms)'] = df['Track Duration (ms)'].apply(convert_min_sec_to_ms)

# Eliminar filas con valores nulos en 'Year_release'
df.dropna(subset=['Year_release'], inplace=True)

# Agrupar por 'Year_release'
grouped = df.groupby('Year_release')

# Realizar la regresión lineal para cada grupo y hacer predicciones
predictions = {}
for name, group in grouped:
    x = group['Year_release'].values.reshape(-1, 1)
    y = group['Track Duration (ms)']
    
    imputer = SimpleImputer(strategy='mean')
    x = imputer.fit_transform(x)
    
    modelo = LinearRegression()
    modelo.fit(x, y)
    
    año_prediccion = np.array([[name]])  # Usamos el año del grupo actual como la entrada de predicción
    duracion_predicha = modelo.predict(año_prediccion)
    predictions[name] = duracion_predicha[0]

# Convertir 'predictions' a un DataFrame
df_predictions = pd.DataFrame.from_dict(predictions, orient='index', columns=['Track Duration (ms)'])
df_predictions['Year_release'] = df_predictions.index

# Aplicar K-Means a los datos predichos
X = df_predictions[['Year_release', 'Track Duration (ms)']].values
kmeans = KMeans(n_clusters=4, random_state=0).fit(X)
df_predictions['Cluster'] = kmeans.labels_

# Información de duración por cluster
duracion_clusters = {
    0: '2:00',
    1: '2:30',
    2: '3:00',
    3: '3:30'
}

# Graficar los datos y la línea de regresión
plt.figure(figsize=(10, 6))
plt.scatter(df['Year_release'], df['Track Duration (ms)'], label='Datos')

for cluster in range(4):
    cluster_data = df_predictions[df_predictions['Cluster'] == cluster]
    plt.scatter(cluster_data['Year_release'], cluster_data['Track Duration (ms)'], label=f'Cluster {cluster}')
    
    # Añadir información de duración al cuadro de información (tooltip)
    x_mean = cluster_data['Year_release'].mean()
    y_mean = cluster_data['Track Duration (ms)'].mean()
    plt.text(x_mean, y_mean, duracion_clusters[cluster], ha='center', va='center', fontsize=10, color='black')

plt.xlabel('Año')
plt.ylabel('Duración')
plt.legend()
plt.savefig("Predicciones_Regresion_Color_Info.png")
plt.show()