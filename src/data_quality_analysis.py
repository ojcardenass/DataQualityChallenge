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

    # Count the number of anomalies (values outside -1 to 11) in the column key
    key_anomalies = (~df['audio_features.key'].between(-1, 11)).sum()
    key_anomalies_percentage = (key_anomalies / ds_prop['rows']) * 100

    # Count the number of anomalies (values outside -60 to 0) in the column loudness
    loudness_anomalies = (~df['audio_features.loudness'].between(-60, 0)).sum()
    loudness_anomalies_percentage = (loudness_anomalies / ds_prop['rows']) * 100

    # Count the number of anomalies (values outside 0 - 1) in the column acousticness
    acousticness_anomalies = (~df['audio_features.acousticness'].between(0, 1)).sum()
    acousticness_anomalies_percentage = (acousticness_anomalies / ds_prop['rows']) * 100

    # Count the number of anomalies (values outside 0 - 1) in the column liveness
    liveness_anomalies = (~df['audio_features.liveness'].between(0, 1)).sum()
    liveness_anomalies_percentage = (liveness_anomalies / ds_prop['rows']) * 100

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
    # Albums with the same album id
    duplicated_albums = df.drop_duplicates(subset=['album_id'], keep=False)
