import json
import os
from io import StringIO, BytesIO

import utils_io
import pandas as pd
from datetime import datetime
import pandas as pd


# 1. Completeness 
# 2. Uniqueness 
# 3. Timeliness 
# 4. Validity
# 5. Accuracy
# 6. Consistency

# Perform data analysis
def dataset_properties(df):
    # Get the number of rows and columns in the dataset
    num_rows = df.shape[0]
    num_cols = df.shape[1]
    total_data = num_cols * num_rows

    ds_prop = {'rows': num_rows, 'cols': num_cols, 'all': total_data}

    return ds_prop

## Test definitions
# Check if there are null values in the column
def column_has_null_values(df, column):
    # Check if there are null values in the column
    null_values = df[column].isnull()
    null_values_count = df[column].isnull().sum()

    data = {'nulls': null_values, 'count': null_values_count}

    if null_values_count > 0:
        return data
    else:
        return False

# Check if there are duplicated rows in the dataset
def dataset_has_duplicate_rows(df):
    # Check if there are duplicates in the dataset
    duplicates = df.duplicated()
    duplicates_count = df.duplicated().sum()

    # Get the unique values that are duplicated
    duplicates = df.loc[duplicates, :]

    data = {'duplicates': duplicates, 'count': duplicates_count}

    if duplicates_count > 0:
        return data
    else:
        return False

# Check if the text column has incorrect format
def column_has_incorrect_text_format(df, column, format):
    # Filter empty values
    df = df.dropna()
    noNaN = df[column].dropna()
    # Look for the defined format
    if format == 'lower':
    # Check if the text column has incorrect format
        incorrect_format = noNaN.str.islower()
    elif format == 'upper':
        incorrect_format = noNaN.str.isupper()
    elif format == 'title':
        incorrect_format = noNaN.str.istitle()
    else:
        return False

    incorrect_format_count = incorrect_format.sum()
    incorrect_format = df.loc[incorrect_format, column].unique().tolist()

    data = {'incorrect_format': incorrect_format, 'count': incorrect_format_count}

    if incorrect_format_count > 0:
        return data
    else:
        return False 

# Check is the text column has bad encoded apostrophes
def column_has_bad_encoding(df, column):
    # Filter empty values
    df = df.dropna()
    # Check is the text column has bad encoding characters or symbols
    bad_encoding = df[column].apply(func=utils_io.contains_bad_encoding)
    bad_encoding_count = bad_encoding.sum()
    bad_encoding = df.loc[bad_encoding, column].unique().tolist()

    data = {'bad_encoding': bad_encoding, 'count': bad_encoding_count}

    if bad_encoding_count > 0:
        return data
    else:
        return False

# Check if the column has incorrect boolean values
def column_has_incorrect_boolean_values(df, column):
    # Check if the column has incorrect boolean values
    incorrect_boolean = ~df[column].isin(['True', 'False'])
    incorrect_boolean_count = incorrect_boolean.sum()
    incorrect_boolean = df.loc[incorrect_boolean, column].unique().tolist()

    data = {'incorrect_boolean': incorrect_boolean, 'count': incorrect_boolean_count}

    if incorrect_boolean_count > 0:
        return data
    else:
        return False
    
# Check if the column has incorrect numeric values
def column_has_incorrect_numeric_values(df, column):
    # Check if the column has incorrect numeric values
    incorrect_numeric = ~df[column].str.isnumeric()
    incorrect_numeric_count = incorrect_numeric.sum()
    incorrect_numeric = df.loc[incorrect_numeric, column].unique().tolist()

    data = {'incorrect_numeric': incorrect_numeric, 'count': incorrect_numeric_count}

    if incorrect_numeric_count > 0:
        return data
    else:
        return False

# Check if column type is numeric
def column_is_numeric(df, column):
    # Check if column type is numeric
    column_type = df[column].dtypes.name

    if column_type == 'int64' or column_type == 'float64':
        return True
    else:
        return False

# Check if column type is datetime
def column_is_datetime(df, column):
    # Check if column type is datetime
    column_type = df[column].dtypes.name

    if column_type == 'datetime64[ns]':
        return True
    else:
        return False

# Check if column can't be converted to numeric
def column_cant_be_converted_to_numeric(df, column):
    # Check if column can't be converted to numeric
    cant_be_converted = ~df[column].apply(func=utils_io.can_be_converted)
    cant_be_converted_count = cant_be_converted.sum()
    cant_be_converted = df.loc[cant_be_converted, column].unique().tolist()

    data = {'cant_be_converted': cant_be_converted, 'count': cant_be_converted_count}

    if cant_be_converted_count > 0:
        return data
    else:
        return False
    
# Check if column has values outside the range
def column_has_values_outside_range(df, column, min, max):
    # Check if column has values outside the range
    outside_range = ~df[column].between(min, max, inclusive='both')
    outside_range_count = outside_range.sum()
    outside_range = df.loc[outside_range, column].unique().tolist()

    data = {'outside_range': outside_range, 'count': outside_range_count}

    if outside_range_count > 0:
        return data
    else:
        return False

## Data analysis
# Dataset overview
def overview(df):
    ds_prop = dataset_properties(df)

    # Get the summary statistics of numerical columns
    summary_stats = df.describe()

    # Check data types
    # data_types = df.dtypes
    numerics = df.dtypes[df.dtypes == 'int64'].count() + df.dtypes[df.dtypes == 'float64'].count()
    strings = df.dtypes[df.dtypes == 'O'].count()
    date_time = df.dtypes[df.dtypes == 'datetime64[ns]'].count()

    # Check for missing values
    missing_values = df.isnull().sum()

    # Get the percentage of total missing values in each column
    total_missing_values = missing_values.sum()
    missing_values_percentage = (missing_values / ds_prop['rows']) * 100
    total_missing_values_percentage = (total_missing_values / ds_prop['all']) * 100

    # Check for duplicates
    duplicate_rows = df.duplicated().sum()
    duplicate_rows_percentage = (duplicate_rows / ds_prop['rows']) * 100

    # Get the number of unique values per column type and transform it into a list of lists
    obj = df.select_dtypes(include=object).nunique().to_dict()
    obj = [[col,value] for col,value in obj.items()]
    num = df.select_dtypes(include=[int, float]).nunique().to_dict()
    num = [[col,value] for col,value in num.items()]
    date = df.select_dtypes(include='datetime64[ns]').nunique().to_dict()
    date = [[col,value] for col,value in date.items()]

    # Check if there are no values in a type
    for i in [obj, num, date]:
        if not i:
            i.append(['Sin valores', ""])
        else:
            pass

    unique_values_per_type = {'num_types': num, 'str_types': obj, 'date_types': date}

    data = {
        'numerics': numerics,
        'strings': strings,
        'date_time': date_time,
        'total_missing_values': total_missing_values,
        'total_missing_values_percentage': total_missing_values_percentage,
        'duplicate_rows': duplicate_rows,
        'duplicate_rows_percentage': duplicate_rows_percentage,
    }
    data = data | ds_prop | unique_values_per_type

    return data

# 1 - Completeness: A measure of the absence of blank (null or empty string) values or the presence of non­blank values.
def completeness(df):
    ds_prop = dataset_properties(df)
    # Check for missing values
    missing_values = df.isnull().sum()

    # Get the percentage of total missing values in each column
    total_missing_values = missing_values.sum()
    missing_values_percentage = (missing_values / ds_prop['rows']) * 100
    total_missing_values_percentage = (total_missing_values / ds_prop['all']) * 100

    return total_missing_values

# 2 - Uniqueness: No thing will be recorded more than once based upon how that thing is identified.
def uniqueness(df):
    ds_prop = dataset_properties(df)
    # Check for duplicates
    duplicate = dataset_has_duplicate_rows(df)
    duplicate_rows = duplicate['count']
    duplicate_rows_percentage = (duplicate_rows / ds_prop['rows']) * 100

    return duplicate_rows


# 4 - Validity: Data are valid if it conforms to the syntax (format, type, range) of its definition.
def validity(df):
    ds_prop = dataset_properties(df)
    # Count the number of track names that are outliers based on the convention of song naming in English
    incorrect_track_names = column_has_incorrect_text_format(df, 'track_name', 'lower')
    incorrect_track_names = incorrect_track_names['count']

    # Count the number of track names that have bad enconding characters or symbols
    special_character_track_names = column_has_bad_encoding(df, 'track_name')
    special_character_track_names = special_character_track_names['count']

    # Count the number of anomalies in the column Explicit
    explicit_anomalies = column_has_incorrect_boolean_values(df, 'explicit')
    explicit_anomalies = explicit_anomalies['count']

    # Count the number of anomalies in the column total tracks
    total_tracks_anomalies = column_has_incorrect_numeric_values(df, 'album_total_tracks')
    total_tracks_anomalies = total_tracks_anomalies['count']

    # Data type of album release date must be datetime, and it's an object
    # album_release_date_type_is_datetime = column_is_datetime(df, 'album_release_date')

    # Data type of instrumentalness audio feature must be numeric, and it's an object
    instrumentalness_type_is_numeric = column_is_numeric(df, 'audio_features.instrumentalness')

    # Data in instrumentalness audio feature after being converted to numeric has inconsistent values
    instrumentalness_type_conver_anomalies = column_cant_be_converted_to_numeric(df, 'audio_features.instrumentalness')
    instrumentalness_type_conver_anomalies = instrumentalness_type_conver_anomalies['count']

    # Count the number of Track.ids blanks
    track_id_blanks = column_has_null_values(df, 'track_id')
    track_id_blanks = track_id_blanks['count']

    invalid_data = incorrect_track_names + special_character_track_names + explicit_anomalies + total_tracks_anomalies + ~instrumentalness_type_is_numeric  + instrumentalness_type_conver_anomalies + track_id_blanks # + ~album_release_date_type_is_datetime
    
    return invalid_data


# 5 - Accuracy: What data is inaccurate?
def accuracy(df):
    ds_prop = dataset_properties(df)

    # Count the number of anomalies (values outside 0 - 1) in the column danceability
    danceability_anomalies = column_has_values_outside_range(df, 'audio_features.danceability', 0, 1)
    danceability_anomalies = danceability_anomalies['count']

    # Count the number of anomalies (values outside 0 - 1) in the column energy
    energy_anomalies = column_has_values_outside_range(df, 'audio_features.energy', 0, 1)
    energy_anomalies = energy_anomalies['count']

    # Count the number of anomalies (values outside 0 - 1) in the column acousticness
    acousticness_anomalies = column_has_values_outside_range(df, 'audio_features.acousticness', 0, 1)
    acousticness_anomalies = acousticness_anomalies['count']

    # Count the number of anomalies (values outside 0 - 1) in the column liveness
    liveness_anomalies = column_has_values_outside_range(df, 'audio_features.liveness', 0, 1)
    liveness_anomalies = liveness_anomalies['count']

    # Count the number of anomalies (values outside -1 to 11) in the column key
    key_anomalies = column_has_values_outside_range(df, 'audio_features.key', -1, 11)
    key_anomalies = key_anomalies['count']

    # Count the number of anomalies (values outside -60 to 0) in the column loudness
    loudness_anomalies = column_has_values_outside_range(df, 'audio_features.loudness', -60, 0)
    loudness_anomalies = loudness_anomalies['count']

    # Count the number of anomalies (values outside 3 - 7) in the column time_signature
    time_signature_anomalies = column_has_values_outside_range(df, 'audio_features.time_signature', 3, 7)
    time_signature_anomalies = time_signature_anomalies['count']

    # Count the number of anomalies (values outside 0 - 100) in the column Track Popularity
    popularity_anomalies = column_has_values_outside_range(df, 'track_popularity', 0, 100)
    popularity_anomalies = popularity_anomalies['count']

    # Count the numver of anomalies (values outside 0 - 100) in the column Artist Popularity
    artist_popularity_anomalies = column_has_values_outside_range(df, 'artist_popularity', 0, 100)
    artist_popularity_anomalies = artist_popularity_anomalies['count']

    # The common duration of pop songs are typically between one and a half to four minutes long.
    duration_ms_anomalies = column_has_values_outside_range(df, 'duration_ms', 82000, 630000)
    duration_ms_anomalies = duration_ms_anomalies['count']

    # Taylor Swift's first album was released in 2006, so the year should be greater than or equal 2006 and less than or equal to today's year
    first_album = datetime(2006,1,1).strftime('%Y-%m-%d')
    actual_year = datetime.now().strftime('%Y-%m-%d')
    year_anomalies = column_has_values_outside_range(df, 'album_release_date', first_album, actual_year)
    year_anomalies = year_anomalies['count']

    inaccurate_data = danceability_anomalies + energy_anomalies + key_anomalies + loudness_anomalies + acousticness_anomalies + liveness_anomalies + time_signature_anomalies + popularity_anomalies + artist_popularity_anomalies + duration_ms_anomalies + year_anomalies

    return inaccurate_data

# 6 - Consistency: What data gives conflicting answers?
def consistency(df):
    # No comprobation of this kind
    return 0

# 3. Timeliness: Number of records with delayed changes
def timeliness(df):
    # No comprobation of this kind
    return 0

def anomalies_data(df):
    total_anomalies = completeness(df) + uniqueness(df) + validity(df) + accuracy(df) + consistency(df) + timeliness(df)
    data = {'Completitud': completeness(df), 'Unicidad': uniqueness(df), 'Validez': validity(df), 'Precisión': accuracy(df), 'Coherencia': consistency(df), 'Temporalidad': timeliness(df), 'Total': total_anomalies}

    return data

## Data analysis report data

def sources_report():
    source = """
    Fuente: API Spotify <br/>
    Datos: Discografía Taylor Swift <br/>
    """

    description = """
    La información analizada en este informe ha sido recopilada utilizando la interfaz de programación de aplicaciones (API) de Spotify, una plataforma líder en streaming de música. Específicamente, los datos examinados se centran en la artista Taylor Swift, cuya presencia en la industria musical ha sido un fenómeno notable. <br/>

    La API de Spotify proporcionó acceso a una variedad de atributos detallados relacionados con las canciones, álbumes y artistas disponibles en su extenso catálogo. En este análisis, nos sumergimos en los datos asociados con Taylor Swift, explorando aspectos que van desde las características musicales de sus canciones hasta la popularidad de sus álbumes.
    """

    data_definition = """
    Definición de dato: <br/>

    En el contexto de este informe, un "dato" se refiere a la información específica obtenida mediante el cruce entre una fila y una columna en el conjunto de datos. Cada celda en esta matriz de datos representa un valor singular que proporciona detalles sobre aspectos particulares de la discografía de Taylor Swift. Estos valores abarcan desde atributos detallados de canciones, álbumes y artistas hasta métricas relacionadas con la popularidad, características musicales y otra información relevante recopilada de la API de Spotify."""
    
    data = {'source': source, 'description': description, 'definition': data_definition}

    return data

def regards_data(df):
    null_value = df[df.isnull().any(axis=1)].head(1)
    null_index = null_value.index[0]
    null_column = null_value.columns[null_value.isnull().any()][0]
    null_value = null_value[null_column]

    anomalies = {
        "Id de canción nulo:": 
        f"""
        Se encontraron {column_has_null_values(df, 'track_id')['count']} canciones con el id nulo de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        {df.loc[column_has_null_values(df, 'track_id')['nulls'], 'track_id'].head(1).to_string()}<br/>
        <br/>
        """,

        "Filas duplicadas:":
        f"""
        Se encontraron {dataset_has_duplicate_rows(df)['count']} filas duplicadas de {dataset_properties(df)['rows']}. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        5 Indices de filas duplicadas: <br/>
        {dataset_has_duplicate_rows(df)['duplicates'].head().index.to_list()}<br/>
        <br/>
        """,

        "Valores nulos:": 
        f"""
        Se encontraron {completeness(df)} valores nulos de {dataset_properties(df)['all']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        null_value_column = {null_column} <br/>
        null_index_value = {null_value.to_string()} <br/>
        <br/>
        """,

        "Formato incorrecto en nombres de canciones según la convencion de nombramiento en inglés:": 
        f"""
        Se encontraron {column_has_incorrect_text_format(df, 'track_name', 'lower')['count']} nombres de canciones con formato incorrecto de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        incorrect_track_names = {column_has_incorrect_text_format(df, 'track_name', 'lower')['incorrect_format'][:4]}<br/>
        <br/>
        NOTA: <br/>
        Puede no ser necesariamente una anomalía. Es importante destacar que, en la industria musical, la creatividad y la expresión artística a menudo influyen en la elección de nombres de canciones, lo que puede llevar a variaciones en el formato. Este hallazgo se menciona con la precaución de que la divergencia del formato convencional puede ser intencional y parte del estilo artístico. <br/>
        <br/>""",

        "Caracteres mal codificados en nombres de canciones:":
        f"""
        Se encontraron {column_has_bad_encoding(df, 'track_name')['count']} nombres de canciones con caracteres mal codificados de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        track_name_anomalies = {column_has_bad_encoding(df, 'track_name')['bad_encoding'][41:45]}<br/>
        <br/>""",

        "Datos no booleanos en la columna ‘explicit’:": f"""
        Se encontraron {column_has_incorrect_boolean_values(df, 'explicit')['count']} datos no booleanos en la columna ‘explicit’ de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        explicit_anomalies = {column_has_incorrect_boolean_values(df, 'explicit')['incorrect_boolean']}<br/>
        <br/>
        <br/>""",

        "Datos no numéricos en la columna ‘album_total_tracks’:": f"""
        Se encontraron {column_has_incorrect_numeric_values(df, 'album_total_tracks')['count']} datos no numéricos en la columna ‘album_total_tracks’ de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        album_total_tracks_anomalies = {column_has_incorrect_numeric_values(df, 'album_total_tracks')['incorrect_numeric']}<br/>
        <br/>""",

        # "Formato diferente a fecha en la columna ‘album_release_date’:": f"""
        # La columna ‘album_release_date’ tiene un formato diferente a fecha. <br/>
        # <br/>
        # Ejemplo: <br/>
        # <br/>
        # album_release_date_type_is_datetime = {column_is_datetime(df, 'album_release_date')}<br/>
        # <br/>""",

        "Formato no numérico en la columna ‘audio_features.instrumentalness’:": f"""
        La columna ‘audio_features.instrumentalness’ tiene un formato no numérico. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        instrumentalness_type_is_numeric = {column_is_numeric(df, 'audio_features.instrumentalness')}<br/>
        instrumentalness_type_anomalies = {df['audio_features.instrumentalness'].head().tolist()}<br/>
        <br/>""",

        "Datos no convertibles a numéricos en la columna ‘audio_features.instrumentalness’:": f"""
        Se encontraron {column_cant_be_converted_to_numeric(df, 'audio_features.instrumentalness')['count']} datos no convertibles a numéricos en la columna ‘audio_features.instrumentalness’ de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        instrumentalness_type_conver_anomalies = {column_cant_be_converted_to_numeric(df, 'audio_features.instrumentalness')['cant_be_converted']} <br/>
         <br/>""",

        "Valores fuera del rango [0,1] en la columna 'audio_features.danceability':": f"""
        Se encontraron {column_has_values_outside_range(df, 'audio_features.danceability', 0, 1)['count']} valores fuera del rango [0,1] en la columna 'audio_features.danceability' de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        danceability_anomalies = {column_has_values_outside_range(df, 'audio_features.danceability', 0, 1)['outside_range']}<br/>
        <br/>""",

        "Valores fuera del rango [0,1] en la columna 'audio_features.energy’:": f"""
        Se encontraron {column_has_values_outside_range(df, 'audio_features.energy', 0, 1)['count']} valores fuera del rango [0,1] en la columna 'audio_features.energy’ de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        energy_anomalies = {column_has_values_outside_range(df, 'audio_features.energy', 0, 1)['outside_range']}<br/>
        <br/>""",

        "Valores fuera del rango [0,1] en la columna 'audio_features.liveness’:": f"""
        Se encontraron {column_has_values_outside_range(df, 'audio_features.liveness', 0, 1)['count']} valores fuera del rango [0,1] en la columna 'audio_features.liveness’ de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        liveness_anomalies = {column_has_values_outside_range(df, 'audio_features.liveness', 0, 1)['outside_range']}<br/>
        <br/>""",

        "Valores fuera del rango [3,7] en la columna 'audio_features.time_signature’:": f"""
        Se encontraron {column_has_values_outside_range(df, 'audio_features.time_signature', 3, 7)['count']} valores fuera del rango [3,7] en la columna 'audio_features.time_signature’ de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        time_signature_anomalies = {column_has_values_outside_range(df, 'audio_features.time_signature', 3, 7)['outside_range']}<br/>
        <br/>""",

        "Valores fuera del rango [-1,11] en la columna 'audio_features.key’:": f"""
        Se encontraron {column_has_values_outside_range(df, 'audio_features.key', -1, 11)['count']} valores fuera del rango [-1,11] en la columna 'audio_features.key’ de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        key_anomalies = {column_has_values_outside_range(df, 'audio_features.key', -1, 11)['outside_range']}<br/>
        <br/>""",

        "Valores fuera del rango [-60,0] en la columna 'audio_features.loudness’:": f"""
        Se encontraron {column_has_values_outside_range(df, 'audio_features.loudness', -60, 0)['count']} valores fuera del rango [-60,0] en la columna 'audio_features.loudness’ de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        loudness_anomalies = {column_has_values_outside_range(df, 'audio_features.loudness', -60, 0)['outside_range']}<br/>
        <br/>""",

        "Valores fuera del rango [0,100] en la columna 'track_popularity’:": f"""
        Se encontraron {column_has_values_outside_range(df, 'track_popularity', 0, 100)['count']} valores fuera del rango [0,100] en la columna 'track_popularity’ de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        track_popularity_anomalies = {column_has_values_outside_range(df, 'track_popularity', 0, 100)['outside_range']}<br/>
        <br/>""",

        "Valores fuera del rango [0,100] en la columna 'artist_popularity’:": f"""
        Se encontraron {column_has_values_outside_range(df, 'artist_popularity', 0, 100)['count']} valores fuera del rango [0,100] en la columna 'artist_popularity’ de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        artist_popularity_anomalies = {column_has_values_outside_range(df, 'artist_popularity', 0, 100)['outside_range']}<br/>
        <br/>""",

        "Valores fuera del rango [82000, 630000] en la columna ‘duration_ms’:": f"""
        Se encontraron {column_has_values_outside_range(df, 'duration_ms', 82000, 630000)['count']} valores fuera del rango [82000, 630000] en la columna ‘duration_ms’ de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        duration_ms_anomalies = {column_has_values_outside_range(df, 'duration_ms', 82000, 630000)['outside_range']}<br/>
        <br/>
        Nota: <br/>
        Los limites superior e inferior de 630,000 y 82,000 milisegundos se eligen basados en la duración de la canción más larga y más corta de Taylor Swift, que tienen aproximadamente 10 minutos y 1 minuto y 22 segundos respectivamente. <br/>
        <br/>""",

        "Valores fuera del rango [2006, 2024] en la columna ‘album_release_date’:": f"""
        Se encontraron {column_has_values_outside_range(df, 'album_release_date', '2006-01-01', '2024-01-01')['count']} valores fuera del rango [2006, 2024] en la columna ‘album_release_date’ de {dataset_properties(df)['rows']} datos. <br/>
        <br/>
        Ejemplo: <br/>
        <br/>
        year_anomalies = {column_has_values_outside_range(df, 'album_release_date', '2006-01-01', '2024-01-01')['outside_range']}<br/>
        <br/>""",
    }

    return anomalies

def analysis_stats(df):
    ds_prop = dataset_properties(df)
    # Analized columns
    analized = [ 
        'track_name', 
        'explicit', 
        'album_total_tracks', 
        'audio_features.instrumentalness', 
        'album_release_date', 
        'track_id', 
        'audio_features.danceability', 
        'audio_features.energy', 
        'audio_features.acousticness', 
        'audio_features.liveness', 
        'audio_features.key', 
        'audio_features.loudness', 
        'audio_features.time_signature', 
        'track_popularity', 
        'artist_popularity', 
        'duration_ms', 
        'album_id', 
        'audio_features.speechiness',
        'audio_features.tempo', 
        'album_name']
    
    # Get the columns that are not analyzed
    not_analyzed = [column for column in df.columns if column not in analized]

    data_notanaly = len(not_analyzed) * ds_prop['rows']
    data_analy = anomalies_data(df)['Total']
    good_data = ds_prop['all'] - data_notanaly - data_analy

    stats = {'notAnalyzed': data_notanaly , 'analyzed': data_analy, 'good': good_data}

    return stats