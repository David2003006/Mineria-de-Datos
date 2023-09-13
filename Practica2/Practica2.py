import pandas as pd


data= pd.read_csv("top_10000_1960-now.csv", encoding='latin1')

columns_to_delete = [
    'Track URI', 'Artist URI(s)', 'Album URI', 'Album Artist URI(s)', 
    'Album Image URL', 'Track Preview URL', 'Added By', 'Added At', 
    'Album Genres', 'Copyrights', 'Mode', 'Loudness', 'Energy', 
    'Danceability', 'Speechiness', 'Acousticness', 'Instrumentalness', 
    'Liveness', 'Time Signature'
]

#Aqui borro las columnas inecesarias de mi dataset 
def delete_colum(data, columns_to_delete ):
    data.drop(columns=columns_to_delete, inplace=True)
    

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
       

delete_colum(data, columns_to_delete)    
data['Tempo']= data['Tempo'].apply(define_tempo)
data = data.rename(columns={'Valence': 'Emocionalidad'})
data= data.rename(columns={'Label':'Disquera'})
data['Emocionalidad']=data['Emocionalidad'].apply(define_Emocion)
data.to_csv('Canciones_1960-2023.csv', index= False)

    
