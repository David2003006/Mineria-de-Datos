import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("canciones_1960-2023.csv")

# Agrupar por año de lanzamiento y calcular el promedio de la popularidad
grouped = df.groupby('Year_release')['Popularity'].mean().reset_index()

# Crear un gráfico de dispersión con la regresión lineal
plt.figure(figsize=(12, 6))
data = grouped
plt.scatter(data['Year_release'], data['Popularity'], label="Promedio de Popularidad", color='blue')

# Realizar la regresión lineal
coefficients = np.polyfit(data['Year_release'], data['Popularity'], 1)
poly = np.poly1d(coefficients)
plt.plot(data['Year_release'], poly(data['Year_release']), linestyle='-', color='red', label="Regresión Lineal")

plt.xlabel('Año de Lanzamiento')
plt.ylabel('Promedio de Popularidad')
plt.title('Dispersión de Promedio de Popularidad a lo largo del tiempo')
plt.legend()
plt.grid(True)
plt.savefig('grafico_dispersion_regresion.jpg', format='jpg')
plt.show()

