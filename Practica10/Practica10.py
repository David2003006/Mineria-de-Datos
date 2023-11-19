import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt


df= pd.read_csv('canciones_1960-2023.csv')

disqueras= ''.join(df["Disquera"].dropna().astype(str))

wordcloud = WordCloud(width = 800, height = 400, background_color ='white').generate(disqueras)

# Mostrar la nube de palabras
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig("Disqueras.png")
plt.show()
