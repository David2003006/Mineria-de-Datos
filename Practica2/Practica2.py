import pandas as pd

ruta = "top_10000_1960-now.csv"
pt = pd.read_csv(ruta, encoding='latin-1')

columns_to_delete = [
    'Track URI', 'Artist URI(s)', 'Album URI', 'Album Artist URI(s)',
    'Album Image URL', 'Track Preview URL', 'Added By', 'Added At',
    'Album Genres', 'Copyrights', 'Mode', 'Loudness', 'Energy',
    'Danceability', 'Speechiness', 'Acousticness', 'Instrumentalness',
    'Liveness', 'Time Signature', 'ISRC', 'Album Artist Name(s)'
]

generos = ["indie", "rock", "metal", "britpop", "australian", "punk", "alternativo", "pop", "rap", "r&b", "post-grunge", "dance pop", "disco", "folk"]


# Aquí borro las columnas innecesarias de mi dataset
def delete_column(pt, columns_to_delete):
    pt.drop(columns=columns_to_delete, inplace=True)

# Aquí en la columna del 'Tempo' checo qué número es para regresar Lento, Moderado, etc.
# para más claridad
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

# Aquí hago algo similar a la columna 'Tempo', solo que ahora con valance
# Checo si es válido con cierto valor y devuelvo 'Triste' o 'Feliz', y si no se cumple, 'Neutro'
def define_emocion(valor):
    distancia_a_0 = abs(valor)
    distancia_a_1 = abs(1 - valor)

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

def ajustar_fecha(fecha):
    if isinstance(fecha, str):
        # Eliminar corchetes si están presentes
        fecha = fecha.replace('[', '').replace(']', '')
        partes_slash = fecha.split('/')
        partes_dash = fecha.split('-')
        
        if len(partes_slash) == 1 and len(partes_dash) == 2:
            # En caso de que esté en formato 'yyyy-mm', cambiamos a '01/mm/yyyy'
            fecha = f'01/{partes_dash[1]}/{partes_dash[0]}'
        elif len(partes_slash) == 1 and len(partes_dash) == 1:
            # Si no se puede separar por "/" ni por "-", ignoramos la fecha
            return None
        elif len(partes_slash) == 1:
            # Solo se proporcionó el año, agregamos el mes y el día
            fecha = f'01/01/{partes_slash[0]}'
        elif len(partes_slash) == 2:
            # En formato 'mm/yyyy', cambiamos a '01/mm/yyyy'
            fecha = f'01/{partes_slash[1]}/{partes_slash[0]}'
        elif len(partes_slash) == 3:
            # Verificar que el día y el mes sean valores válidos
            day, month, year = partes_slash
            try:
                day = int(day)
                month = int(month)
                year = int(year)
                if 1 <= day <= 31 and 1 <= month <= 12:
                    fecha = f'{day:02d}/{month:02d}/{year}'
                else:
                    # Corregir si los valores están fuera de rango
                    fecha = f'01/01/{year}'
            except ValueError:
                # En caso de valores no numéricos
                fecha = f'01/01/{year}'
                print(f"Falle en esta fecha: {fecha}")
    return fecha

def cambiar_orden_fecha(fecha):
    if isinstance(fecha, str):
        partes_slash = fecha.split('/')
        partes_dash = fecha.split('-')

        if len(partes_slash) == 3:
            try:
                # Intenta convertir las partes a números para validar la fecha
                int(partes_slash[0])
                int(partes_slash[1])
                int(partes_slash[2])
                fecha = f'{partes_slash[2]}/{partes_slash[1]}/{partes_slash[0]}'  # Formato correcto
            except ValueError:
                # Si no se pueden convertir a números, intentamos con el formato con guiones
                if len(partes_dash) == 3:
                    try:
                        int(partes_dash[0])
                        int(partes_dash[1])
                        int(partes_dash[2])
                        fecha = f'{partes_dash[2]}/{partes_dash[1]}/{partes_dash[0]}'  # Formato correcto con guiones
                    except ValueError:
                        print(f"Falle en esta fecha: {fecha}")
                        return None
                else:
                    print(f"Falle en esta fecha: {fecha}")
                    return None
        elif len(partes_slash) == 1 and len(partes_dash) == 2:
            # En caso de que esté en formato 'yyyy-mm', cambiamos a '01/mm/yyyy'
            fecha = f'01/{partes_dash[1]}/{partes_dash[0]}'
        elif len(partes_slash) == 1:
            # Si no se puede separar por "/" ni por "-", ignoramos la fecha
            return None
    return fecha

# Aplica la función para ajustar las fechas
pt['Album Release Date'] = pt['Album Release Date'].apply(ajustar_fecha)

def asignar_genero(row):
    for genero in generos:
        row[genero] = 0  # Establecer valor inicial en 0 para cada género
        artist_genres = str(row['Artist Genres']).lower()
        for genero in generos:
            if genero in artist_genres:
                row[genero] = 1
        return row

pt = pt.apply(asignar_genero, axis=1)
pt.drop(columns=['Artist Genres'], inplace=True)
delete_column(pt, columns_to_delete)
pt['Tempo'] = pt['Tempo'].apply(define_tempo)
pt = pt.rename(columns={'Valence': 'Emocionalidad'})
pt['Track Duration (ms)'] = pt['Track Duration (ms)'].apply(convert_ms_to_min_sec)
pt = pt.rename(columns={'Label': 'Disquera'})
pt['Emocionalidad'] = pt['Emocionalidad'].apply(define_emocion)

# Aplica la función para ajustar las fechas
pt['Album Release Date'] = pt['Album Release Date'].apply(ajustar_fecha)
# Convierte las fechas a tipo datetime
pt['Album Release Date'] = pd.to_datetime(pt['Album Release Date'], format='%d/%m/%Y')
pt['Year_release'] = pt['Album Release Date'].dt.year
pt.to_csv('canciones_1960-2023.csv', index=False)
