import pandas as pd


ruta ="top_10000_1960-now.csv"
pd= pd.read_csv(ruta)


columns_to_delete = [
    'Track URI', 'Artist URI(s)', 'Album URI', 'Album Artist URI(s)', 
    'Album Image URL', 'Track Preview URL', 'Added By', 'Added At', 
    'Album Genres', 'Copyrights', 'Mode', 'Loudness', 'Energy', 
    'Danceability', 'Speechiness', 'Acousticness', 'Instrumentalness', 
    'Liveness', 'Time Signature', 'ISRC', 'Album Artist Name(s)'
]

generos = ["indie", "rock", "metal", "britpop", "australian", "punk", "alternativo", "pop", "rap", "r&b", "post-grunge", "dance pop", "disco", "folk"]


    
#Aqui borro las columnas inecesarias de mi dataset 
def delete_colum(pd, columns_to_delete ):
    pd.drop(columns=columns_to_delete, inplace=True)
    

#Aqui en la columna del 'Tempo' checo que numero es para regresar Lento, Moderado etc... 
#para mas claridad
def define_tempo(valor):
   if 40 <= valor <= 60:
        return 'Lento'
   elif 76 <= valor < 108:
        return 'Andante'
   elif 108 <= valor < 120:
        return 'Moderado'
   elif 120 <= valor <= 168:
        return 'Allegro'
   elif valor > 168:
        return 'Presto'
   else:
       return 'Tempo imposible'
       
#Aqui hago un poco de lo mismo que con la columna 'Tempo' nomas que ahora con valance 
# checo si es valido con cierto valor y devuelvo 'Trsite' o 'Feliz' y si no se cumple 'Neutro'
def define_Emocion(valor):
    distancia_a_0= abs(valor)
    distancia_a_1= abs(1- valor)
    
    if distancia_a_0 < distancia_a_1:
        return 'Triste'
    elif distancia_a_1 < distancia_a_0:
        return 'Feliz'
    else:
        return 'Neutro'

def convert_ms_to_min_sec(ms):
    seconds = ms / 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{int(minutes)} minutos {int(seconds)} segundos"

def asignar_genero(row):
    for genero in generos:
        row[genero] = 0  # Establecer valor inicial en 0 para cada género
        artist_genres = str(row['Artist Genres']).lower()
    for genero in generos:
        if genero in artist_genres:
            row[genero] = 1
    return row

pd = pd.apply(asignar_genero, axis=1)
pd.drop(columns=['Artist Genres'], inplace=True)
delete_colum(pd, columns_to_delete)    
pd['Tempo']= pd['Tempo'].apply(define_tempo)
pd = pd.rename(columns={'Valence': 'Emocionalidad'})
pd['Track Duration (ms)'] = pd['Track Duration (ms)'].apply(convert_ms_to_min_sec)
pd= pd.rename(columns={'Label':'Disquera'})
pd['Emocionalidad']=pd['Emocionalidad'].apply(define_Emocion)
pd.to_csv('canciones_1960-2023.csv', index= False)



    
