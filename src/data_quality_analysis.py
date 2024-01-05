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

def regards_data():
    anomalies_list = [
        "Id de canción nulo.",
        "Filas duplicadas.",
        "Valores nulos.",
        "Formato incorrecto en nombres de canciones según la convencion de nombramiento en inglés.",
        "Caracteres mal codificados en nombres de canciones.",
        "Datos no booleanos en la columna ‘explicit’.",
        "Datos no numéricos en la columna ‘album_total_tracks’.",
        "Formato diferente a fecha en la columna ‘album_release_date’.",
        "Formato no numérico en la columna ‘audio_features.instrumentalness’.",
        "Datos no convertibles a numéricos en la columna ‘audio_features.instrumentalness’.",
        "Valores fuera del rango [0,1] en la columna 'audio_features.danceability'.",
        "Valores fuera del rango [0,1] en la columna 'audio_features.energy’.",
        "Valores fuera del rango [0,1] en la columna 'audio_features.liveness’.",
        "Valores fuera del rango [3,7] en la columna 'audio_features.time_signature’.",
        "Valores fuera del rango [-1,11] en la columna 'audio_features.key’.",
        "Valores fuera del rango [-60,0] en la columna 'audio_features.loudness’.",
        "Valores fuera del rango [0,100] en la columna 'track_popularity’.",
        "Valores fuera del rango [0,100] en la columna 'artist_popularity’.",
        "Valores fuera del rango [82000, 10000000] en la columna ‘duration_ms’.",
        "Valores fuera del rango [2006, 2024] en la columna ‘album_release_date’."
    ]

    return anomalies_list

# Perform data analysis
def dataset_properties(df):
    # Get the number of rows and columns in the dataset
    num_rows = df.shape[0]
    num_cols = df.shape[1]
    total_data = num_cols * num_rows

    ds_prop = {'rows': num_rows, 'cols': num_cols, 'all': total_data}

    return ds_prop

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

    # 1 - Completeness: A measure of the absence of blank (null or empty string) values or the presence of non­blank values.
    # Check for missing values
    missing_values = df.isnull().sum()

    # Get the percentage of total missing values in each column
    total_missing_values = missing_values.sum()
    missing_values_percentage = (missing_values / ds_prop['rows']) * 100
    total_missing_values_percentage = (total_missing_values / ds_prop['all']) * 100

    # 3 - Uniqueness: No thing will be recorded more than once based upon how that thing is identified.

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
            i.append(['No values', ""])
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
    duplicate_rows = df.duplicated().sum()
    duplicate_rows_percentage = (duplicate_rows / ds_prop['rows']) * 100

    return duplicate_rows


# 4 - Validity: Data are valid if it conforms to the syntax (format, type, range) of its definition.
def validity(df):
    ds_prop = dataset_properties(df)
    # Count the number of track names that are outliers based on the convention of song naming in English
    incorrect_track_names = df['track_name'].dropna()
    incorrect_track_names = (incorrect_track_names.str.islower()).sum()
    incorrect_track_names_percentage = (incorrect_track_names / ds_prop['rows']) * 100

    # Count the number of track names that have bad enconding characters or symbols
    special_character_track_names = df['track_name'].dropna()
    special_character_track_names = special_character_track_names.apply(func=utils_io.contains_bad_encoding).sum()
    special_character_track_names_percentage = (special_character_track_names / ds_prop['rows']) * 100

    # Count the number of anomalies in the column Explicit
    explicit_anomalies = (~df['explicit'].isin(['True', 'False'])).sum()
    explicit_anomalies_percentage = (explicit_anomalies / ds_prop['rows']) * 100

    # Count the number of anomalies in the column total tracks
    total_tracks_anomalies = (~df['album_total_tracks'].str.isnumeric()).sum()
    total_tracks_anomalies_percentage = (total_tracks_anomalies / ds_prop['rows']) * 100

    # Data type of instrumentalness audio feature must be numeric, and it's an object
    instrumentalness_type = df['audio_features.instrumentalness']
    instrumentalness_type_is_numeric = (instrumentalness_type.dtypes.name).isnumeric()

    # Data type of album release date must be datetime, and it's an object
    album_release_date_type = df['album_release_date']
    album_release_date_type_is_datetime = album_release_date_type.dtypes == 'datetime64[ns]'

    # Data in instrumentalness audio feature after being converted to numeric has inconsistent values
    instrumentalness_type_conver_anomalies = (~instrumentalness_type.apply(func=utils_io.can_be_converted)).sum()
    instrumentalness_type_conver_anomalies_percentage = (instrumentalness_type_conver_anomalies / ds_prop['rows']) * 100

    # Count the number of Track.ids blanks
    track_id_blanks = df['track_id'].isnull().sum()
    track_id_blanks_percentage = (track_id_blanks / ds_prop['rows']) * 100

    invalid_data = incorrect_track_names + special_character_track_names + explicit_anomalies + total_tracks_anomalies + ~instrumentalness_type_is_numeric + ~album_release_date_type_is_datetime + instrumentalness_type_conver_anomalies + track_id_blanks
    
    return invalid_data


# 5 - Accuracy: What data is inaccurate?
def accuracy(df):
    ds_prop = dataset_properties(df)

    # Count the number of anomalies (values outside 0 - 1) in the column danceability
    danceability_anomalies = (~df['audio_features.danceability'].between(0, 1)).sum()
    danceability_anomalies_percentage = (danceability_anomalies / ds_prop['rows']) * 100

    # Count the number of anomalies (values outside 0 - 1) in the column energy
    energy_anomalies = (~df['audio_features.energy'].between(0, 1)).sum()
    energy_anomalies_percentage = (energy_anomalies / ds_prop['rows']) * 100

    # Count the number of anomalies (values outside 0 - 1) in the column acousticness
    acousticness_anomalies = (~df['audio_features.acousticness'].between(0, 1)).sum()
    acousticness_anomalies_percentage = (acousticness_anomalies / ds_prop['rows']) * 100

    # Count the number of anomalies (values outside 0 - 1) in the column liveness
    liveness_anomalies = (~df['audio_features.liveness'].between(0, 1)).sum()
    liveness_anomalies_percentage = (liveness_anomalies / ds_prop['rows']) * 100

    # Count the number of anomalies (values outside -1 to 11) in the column key
    key_anomalies = (~df['audio_features.key'].between(-1, 11)).sum()
    key_anomalies_percentage = (key_anomalies / ds_prop['rows']) * 100

    # Count the number of anomalies (values outside -60 to 0) in the column loudness
    loudness_anomalies = (~df['audio_features.loudness'].between(-60, 0)).sum()
    loudness_anomalies_percentage = (loudness_anomalies / ds_prop['rows']) * 100

    # Count the number of anomalies (values outside 0 - 1) in the column time_signature
    time_signature_anomalies = (~df['audio_features.time_signature'].between(3, 7)).sum()
    time_signature_anomalies_percentage = (time_signature_anomalies / ds_prop['rows']) * 100

    # Count the number of anomalies (values outside 0 - 100) in the column Track Popularity
    popularity_anomalies = (~df['track_popularity'].between(0, 100)).sum()
    popularity_anomalies_percentage = (popularity_anomalies / ds_prop['rows']) * 100

    # Count the numver of anomalies (values outside 0 - 100) in the column Artist Popularity
    artist_popularity_anomalies = (~df['artist_popularity'].between(0, 100)).sum()
    artist_popularity_anomalies_percentage = (artist_popularity_anomalies / ds_prop['rows']) * 100

    # The common duration of pop songs are typically between one and a half to four minutes long.
    duration_ms_anomalies = (~df['duration_ms'].between(82000, 10000000)).sum()
    duration_ms_anomalies_percentage = (duration_ms_anomalies / ds_prop['rows']) * 100

    # Taylor Swift's first album was released in 2006, so the year should be greater than or equal 2006 and less than or equal to today's year
    first_album = datetime(2006,1,1).strftime('%Y-%m-%d')
    actual_year = datetime.now().strftime('%Y-%m-%d')
    year_anomalies = (~df['album_release_date'].between(first_album, actual_year, inclusive='both')).sum()
    year_anomalies_anomalies_percentage = (year_anomalies / ds_prop['rows']) * 100

    inaccurate_data = danceability_anomalies + energy_anomalies + key_anomalies + loudness_anomalies + acousticness_anomalies + liveness_anomalies + time_signature_anomalies + popularity_anomalies + artist_popularity_anomalies + duration_ms_anomalies + year_anomalies

    return inaccurate_data

# 6 - Consistency: What data gives conflicting answers?
def consistency(df):
    return 0

# 3. Timeliness: Number of records with delayed changes
def timeliness(df):
    return 0

def anomalies_data(df):
    total_anomalies = completeness(df) + uniqueness(df) + validity(df) + accuracy(df) + consistency(df) + timeliness(df)
    data = {'Completeness': completeness(df), 'Uniqueness': uniqueness(df), 'Validity': validity(df), 'Accuracy': accuracy(df), 'Consistency': consistency(df), 'Timeliness': timeliness(df), 'Total': total_anomalies}

    return data


def analysis_stats(df):
    ds_prop = dataset_properties(df)
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

    not_analyzed = [column for column in df.columns if column not in analized]

    data_notanaly = len(not_analyzed) * ds_prop['rows']
    data_analy = anomalies_data(df)['Total']
    good_data = ds_prop['all'] - data_notanaly - data_analy

    stats = {'notAnalyzed': data_notanaly , 'analyzed': data_analy, 'good': good_data}

    return stats

