import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

df = pd.read_csv('canciones_1960-2023.csv')

def convert_min_sec_to_ms(min_sec):
    parts = min_sec.split()
    minutes = int(parts[0])
    seconds = int(parts[2])
    return (minutes * 60 + seconds) * 1000

df['Track Duration (ms)'] = df['Track Duration (ms)'].apply(convert_min_sec_to_ms)

x = df['Track Duration (ms)'].to_numpy().reshape(-1, 1)  # Convierte a matriz NumPy
y = df['Track Duration (ms)']

print(len(x))
print(len(y))

X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.1, random_state=42)

knn = KNeighborsClassifier(n_neighbors=3)
scores = cross_val_score(knn, x, y, cv=3)

knn.fit(X_train, Y_train)

y_pred = knn.predict(X_test)

accuracy = accuracy_score(Y_test, y_pred)
print("Exactitud del modelo K-NN:", accuracy)

plt.figure(figsize=(10,6))
plt.scatter(x, y)
plt.title('Gráfica de Dispersión del Conjunto de Datos de duración de pista')
plt.xlabel('Duración (ms)')
plt.ylabel('Duración (ms)')
plt.savefig('grafica_de_clasificacion_duracion_pista.jpg', format='jpg')
plt.show()