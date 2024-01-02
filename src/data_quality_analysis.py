import json
import os

import utils_io
import pandas as pd
from datetime import datetime

# Read the CSV file using the selected method
df = utils_io.get_dataset('url')

# Perform data analysis
# Get the number of rows and columns in the dataset
num_rows = df.shape[0]
num_cols = df.shape[1]

# Seven pillars of data quality
# 1 - Completeness
# 2 - Conformity
# 3 - Uniqueness
# 4 - Accuracy
# 5 - Validity
# 6 - Consistency
# 7 - Integrity

# Get the summary statistics of numerical columns
summary_stats = df.describe()
# Check data types
data_types = df.dtypes

# 1 - Completeness: What percentage of the data is missing?
# Check for missing values
missing_values = df.isnull().sum()
# Get the percentage of total missing values in each column
total_missing_values = missing_values.sum()
total_missing_values_percentage = (missing_values / num_rows) * 100
missing_values_percentage = (missing_values / num_rows) * 100

# 3 - Uniqueness: What percentage of the data is duplicated?
# Check for duplicates
duplicate_rows = df.duplicated().sum()
duplicate_rows_percentage = (duplicate_rows / num_rows) * 100

# Get the unique values in object like columns
unique_values = pd.DataFrame(columns=['Column', 'Unique_Values'])
for column in df.columns:
    if df[column].dtype == 'object':    
        unique_values = unique_values._append({'Column': column, 'Unique_Values': df[column].unique()}, ignore_index=True, verify_integrity=True)

# Check for outliers in all columns with object data type
outliers = pd.DataFrame(columns=['Column', 'Outliers'])
for column in df.columns:
    if df[column].dtype == 'object':    
        outliers = outliers._append({'Column': column, 'Outliers': df[column].value_counts().head(10)}, ignore_index=True, verify_integrity=True)


# 2 - Conformity: Does the data conform to a specific format?

# Count the number of track names that are outliers based on the convention of song naming in English
# Count the number of track names that are not capitalized correctly
correct_track_names = df['track_name'].dropna()
correct_track_names = (~correct_track_names.str.islower()).sum()

# Count the number of track names that have special characters or symbols
special_character_track_names = df['track_name'].dropna()
special_character_track_names = special_character_track_names.apply(func=utils_io.contains_bad_encoding).sum()

# Count the number of anomalies in the column Explicit
explicit_anomalies_count = (~df['explicit'].isin(['True', 'False'])).sum()

# Count the number of anomalies in the column total tracks
total_tracks_anomalies_count = (~df['album_total_tracks'].str.isnumeric()).sum()


# 4 - Accuracy: What data is inaccurate?

# Count the number of anomalies (values outside 0 - 100) in the column Track Popularity
popularity_anomalies_count = (~df['track_popularity'].between(0, 100)).sum()

# The common duration of pop songs are typically between one and a half to four minutes long.
duration_ms_anomalies_count = (~df['duration_ms'].between(82000, 10000000)).sum()

# Taylor Swift's first album was released in 2006, so the year should be greater than 2006 and less than todays year
first_album = datetime(2006,1,1).strftime('%Y-%m-%d')
actual_year = datetime.now().strftime('%Y-%m-%d')
year_anomalies_count = (~df['album_release_date'].between(first_album, actual_year)).sum()

# 5 - Validity: What data is invalid?


# 6 - Consistency: What data gives conflicting answers?
# Albums with the same album id

# 7 - Integrity: What data id is missing?
# Track.ids blanks



# Example: Save the analyzed data to a new CSV file
# df.to_csv('analyzed_dataset.csv', index=False)
