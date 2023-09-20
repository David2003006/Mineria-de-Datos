import requests 
from bs4 import BeautifulSoup
import tempfile
import os
import urllib.request

#link directo a la pagina
direct_link = "https://www.kaggle.com/datasets/joebeachcapital/top-10000-spotify-songs-1960-now"
response = requests.get(direct_link)

if response.status_code == 200:
    # Crear un archivo temporal para guardar el contenido descargado
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(response.content)
        # Obtener la ruta del archivo temporal
        temp_file_path = temp_file.name

    # Abrir el archivo descargado
    os.startfile(temp_file_path)  # Esto abrirá el archivo con la aplicación predeterminada
else:
    print("Error al descargar el archivo.")