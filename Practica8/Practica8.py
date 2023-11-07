import pandas as pd
import matplotlib.pyplot as plt
from typing import List
import numpy as np

df = pd.read_csv('canciones_1960-2023.csv')

def k_means(puntos: List[np.array], k: int):
    dime = len(puntos[0])
    n = len(puntos)
    kluster_num = k
    itera = 15
    
    x = np.array(puntos)
    y = np.random.randint(0, kluster_num, n)
    
    promedio = np.zeros((kluster_num, dime))
    
    for _ in range(itera):
        for j in range(kluster_num):
            promedio[j] = np.mean(x[y == j], axis=0)
        for m in range(n):
            distancia = np.sum((promedio - x[m])**2, axis=1)
            pred = np.argmin(distancia)
            y[m] = pred
    
    for kl in range(kluster_num):
        xp = x[y == kl, 0]
        yp = x[y == kl, 1]
        plt.scatter(xp, yp)
    
    plt.savefig("Resultado.png")
    plt.close()
    return promedio

def convert_min_sec_to_ms(min_sec):
    parts = min_sec.split()
    minutes = int(parts[0])
    seconds = int(parts[2])
    return (minutes * 60 + seconds) * 1000

df['Track Duration (ms)'] = df['Track Duration (ms)'].apply(convert_min_sec_to_ms)
df_promedio = df.groupby(['Track Duration (ms)', 'Year_release'])['Popularity'].mean().reset_index()

list_t = [np.array(row) for row in df_promedio[['Track Duration (ms)', 'Year_release']].to_numpy()]
points = [point for point in list_t]

kn = k_means(points, 4)
print(kn)