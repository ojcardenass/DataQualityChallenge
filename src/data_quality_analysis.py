import json
import os

import utils_io
import pandas as pd
from datetime import datetime
import pandas as pd

# Read the CSV file using the selected method
df = utils_io.get_dataset('url')

# Perform data analysis
# Get the number of rows and columns in the dataset
num_rows = df.shape[0]
num_cols = df.shape[1]
total_data = num_cols * num_rows

# 1. Completeness 
# 2. Uniqueness 
# 3. Timeliness 
# 4. Validity
# 5. Accuracy
# 6. Consistency

# Get the summary statistics of numerical columns
summary_stats = df.describe()
# Check data types
data_types = df.dtypes

# 1 - Completeness: A measure of the absence of blank (null or empty string) values or the presence of non­blank values.
# Check for missing values
missing_values = df.isnull().sum()
# Get the percentage of total missing values in each column
total_missing_values = missing_values.sum()
missing_values_percentage = (missing_values / num_rows) * 100
total_missing_values_percentage = (missing_values / total_data) * 100


# 2 - Validity: Data are valid if it conforms to the syntax (format, type, range) of its definition.

# Count the number of track names that are outliers based on the convention of song naming in English
incorrect_track_names = df['track_name'].dropna()
incorrect_track_names = (incorrect_track_names.str.islower()).sum()
incorrect_track_names_percentage = (incorrect_track_names / num_rows) * 100

# Count the number of track names that have bad enconding characters or symbols
special_character_track_names = df['track_name'].dropna()
special_character_track_names = special_character_track_names.apply(func=utils_io.contains_bad_encoding).sum()
special_character_track_names_percentage = (special_character_track_names / num_rows) * 100

# Count the number of anomalies in the column Explicit
explicit_anomalies = (~df['explicit'].isin(['True', 'False'])).sum()
explicit_anomalies_percentage = (explicit_anomalies / num_rows) * 100

# Count the number of anomalies in the column total tracks
total_tracks_anomalies = (~df['album_total_tracks'].str.isnumeric()).sum()
total_tracks_anomalies_percentage = (total_tracks_anomalies / num_rows) * 100

# Data type of instrumentalness audio feature must be numeric, and it's an object
instrumentalness_type = df['audio_features.instrumentalness']
instrumentalness_type_is_numeric = (instrumentalness_type.dtypes.name).isnumeric()

# Data in instrumentalness audio feature after being converted to numeric has inconsistent values
instrumentalness_type_conver_anomalies = (~instrumentalness_type.apply(func=utils_io.can_be_converted)).sum()
instrumentalness_type_conver_anomalies_percentage = (instrumentalness_type_conver_anomalies / num_rows) * 100


# 3 - Uniqueness: No thing will be recorded more than once based upon how that thing is identified.

# Check for duplicates
duplicate_rows = df.duplicated().sum()
duplicate_rows_percentage = (duplicate_rows / num_rows) * 100


# 4 - Accuracy: What data is inaccurate?

# Count the number of anomalies (values outside 0 - 1) in the column danceability
danceability_anomalies = (~df['audio_features.danceability'].between(0, 1)).sum()
danceability_anomalies_percentage = (danceability_anomalies / num_rows) * 100

# Count the number of anomalies (values outside 0 - 1) in the column energy
energy_anomalies = (~df['audio_features.energy'].between(0, 1)).sum()
energy_anomalies_percentage = (energy_anomalies / num_rows) * 100

# Count the number of anomalies (values outside -1 to 11) in the column key
key_anomalies = (~df['audio_features.key'].between(-1, 11)).sum()
key_anomalies_percentage = (key_anomalies / num_rows) * 100

# Count the number of anomalies (values outside -60 to 0) in the column loudness
loudness_anomalies = (~df['audio_features.loudness'].between(-60, 0)).sum()
loudness_anomalies_percentage = (loudness_anomalies / num_rows) * 100

# Count the number of anomalies (values outside 0 - 1) in the column acousticness
acousticness_anomalies = (~df['audio_features.acousticness'].between(0, 1)).sum()
acousticness_anomalies_percentage = (acousticness_anomalies / num_rows) * 100

# Count the number of anomalies (values outside 0 - 1) in the column liveness
liveness_anomalies = (~df['audio_features.liveness'].between(0, 1)).sum()
liveness_anomalies_percentage = (liveness_anomalies / num_rows) * 100

# Count the number of anomalies (values outside 0 - 1) in the column time_signature
time_signature_anomalies = (~df['audio_features.time_signature'].between(3, 7)).sum()
time_signature_anomalies_percentage = (time_signature_anomalies / num_rows) * 100

# Count the number of anomalies (values outside 0 - 100) in the column Track Popularity
popularity_anomalies = (~df['track_popularity'].between(0, 100)).sum()
popularity_anomalies_percentage = (popularity_anomalies / num_rows) * 100

# Count the numver of anomalies (values outside 0 - 100) in the column Artist Popularity
artist_popularity_anomalies = (~df['artist_popularity'].between(0, 100)).sum()
artist_popularity_anomalies_percentage = (artist_popularity_anomalies / num_rows) * 100

# The common duration of pop songs are typically between one and a half to four minutes long.
duration_ms_anomalies = (~df['duration_ms'].between(82000, 10000000)).sum()
duration_ms_anomalies_percentage = (duration_ms_anomalies / num_rows) * 100

# Taylor Swift's first album was released in 2006, so the year should be greater than or equal 2006 and less than or equal to today's year
first_album = datetime(2006,1,1).strftime('%Y-%m-%d')
actual_year = datetime.now().strftime('%Y-%m-%d')
year_anomalies = (~df['album_release_date'].between(first_album, actual_year, inclusive='both')).sum()
year_anomalies_anomalies_percentage = (year_anomalies / num_rows) * 100


# 5 - Validity: What data is invalid?
# Count the number of Track.ids blanks
track_id_blanks = df['track_id'].isnull().sum()
track_id_blanks_percentage = (track_id_blanks / num_rows) * 100


# 6 - Consistency: What data gives conflicting answers?
# Albums with the same album id
duplicated_albums = df.drop_duplicates(subset=['album_id'], keep=False)

data = {
    'Metric': ['Incorrect Track Names', 'Special Character Track Names', 'Explicit Anomalies', 'Total Tracks Anomalies',
               'Instrumentalness Type (Numeric)', 'Instrumentalness Type Conversion Anomalies', 'Duplicate Rows',
               'Danceability Anomalies', 'Energy Anomalies', 'Key Anomalies', 'Loudness Anomalies',
               'Acousticness Anomalies', 'Liveness Anomalies', 'Time Signature Anomalies', 'Popularity Anomalies',
               'Artist Popularity Anomalies', 'Duration Anomalies', 'Year Anomalies', 'Track ID Blanks'],
    'Percentage': [incorrect_track_names_percentage, special_character_track_names_percentage, explicit_anomalies_percentage,
                   total_tracks_anomalies_percentage, instrumentalness_type_is_numeric, instrumentalness_type_conver_anomalies_percentage,
                   duplicate_rows_percentage, danceability_anomalies_percentage, energy_anomalies_percentage,
                   key_anomalies_percentage, loudness_anomalies_percentage, acousticness_anomalies_percentage,
                   liveness_anomalies_percentage, time_signature_anomalies_percentage, popularity_anomalies_percentage,
                   artist_popularity_anomalies_percentage, duration_ms_anomalies_percentage,
                   year_anomalies_anomalies_percentage, track_id_blanks_percentage]
}

data = pd.DataFrame(data)

print(data)
# Example: Save the analyzed data to a new CSV file
# df.to_csv('analyzed_dataset.csv', index=False)
