import pandas as pd
import matplotlib.pyplot as plt

ruta = "canciones_1960-2023.csv"
df = pd.read_csv(ruta, encoding='ISO-8859-1')

emociones = ['Triste', 'Feliz', 'Neutro']

# Función para obtener los valores de "Popularidad" para una emoción dada
def obtener_valores_emocion(df, emocion):
    filtrar_emocion = df[df['Emocionalidad'] == emocion]
    valores_emocion = filtrar_emocion['Popularity'].tolist()
    return valores_emocion

# Obtener valores de "Popularidad" para cada emoción
valores_emociones = [obtener_valores_emocion(df, emocion) for emocion in emociones]

# Colores correspondientes a cada emoción
colores = ['blue', 'green', 'yellow']

# Estilo de marcador para los puntos
marcadores = ['o', 's', 'D']  # Puedes cambiarlos según tus preferencias

# Crear un gráfico de dispersión con colores y marcadores diferentes
for i, emocion in enumerate(emociones):
    plt.scatter(valores_emociones[i], [i] * len(valores_emociones[i]), label=emocion, color=colores[i], marker=marcadores[i])

plt.xlabel('Popularidad')
plt.yticks(range(len(emociones)), emociones)
plt.title('Distribución de Popularidad por Emoción')
plt.legend()
plt.savefig('grafico_dispersion_emociones.jpg', format='jpg')
plt.show()