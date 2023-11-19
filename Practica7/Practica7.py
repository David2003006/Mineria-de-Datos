import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

df = pd.read_csv('canciones_1960-2023.csv')

def convert_min_sec_to_ms(min_sec):
    parts = min_sec.split()
    minutes = int(parts[0])
    seconds = int(parts[2])
    return (minutes * 60 + seconds) * 1000

df['Track Duration (ms)'] = df['Track Duration (ms)'].apply(convert_min_sec_to_ms)

df_promedio = df.groupby(['Track Duration (ms)', 'Year_release'])['Popularity'].mean().reset_index()

x = df_promedio[['Track Duration (ms)']].to_numpy()
y = df_promedio['Popularity']

X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.1, random_state=42)

regression_model = LinearRegression()
regression_model.fit(X_train, Y_train)

y_pred = regression_model.predict(X_test)

plt.figure(figsize=(10,6))
plt.scatter(X_test, Y_test, label='Datos reales')
plt.plot(X_test, y_pred, color='red', label='Predicciones')
plt.title('Regresión lineal de la duración de la pista vs. Popularidad')
plt.xlabel('Duración (ms)')
plt.ylabel('Popularidad')
plt.legend()
plt.savefig('regresion_duracion_pista_popularidad.jpg', format='jpg')
plt.show()