from pathlib import Path
import json
import os

import utils_io
import pandas as pd

# Paths to input and output folders
base_path = Path(os.getcwd())
input_path = os.path.join(base_path, 'input')
output_path = os.path.join(base_path, 'output')

# Input json link and output csv name
json_link = "https://drive.google.com/file/d/1O-z8fCDXy5IleKfU6wRAJZjyz_FIGv9F"
csv_name = 'dataset.csv'
csv_path = os.path.join(output_path, csv_name)

# Get json data from Google Drive using the link
data = utils_io.get_json_from_drive(json_link)

# Normalize json data
tracks = pd.json_normalize(data, record_path=['albums','tracks'], meta=['artist_id'])
albums = pd.json_normalize(data, record_path=['albums'], meta=['artist_id'])
artists = pd.json_normalize(data)

# Merge dataframes into one dataset
dataset = tracks.merge(artists, on='artist_id')
dataset = dataset.merge(albums, on='artist_id')
dataset = dataset.drop(columns=['tracks', 'albums'])

# Save dataset to csv file locally
dataset.to_csv(csv_path, index=False)

# Upload csv dataset to S3
bucket = 'dataqualitychallenge'
utils_io.df_to_s3(dataset, bucket, csv_name)