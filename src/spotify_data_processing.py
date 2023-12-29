from pathlib import Path
import json
import os

import pandas as pd

# Paths to input and output folders
base_path = Path(os.getcwd())
input_path = os.path.join(base_path, 'input')
output_path = os.path.join(base_path, 'output')

# 
json_path = os.path.join(input_path, 'taylor_swift_spotify.json')
csv_path = os.path.join(output_path, 'dataset.csv')

# Load data from json file
with open(json_path) as f:
    data = json.load(f)

# Normalize json data
tracks = pd.json_normalize(data, record_path=['albums','tracks'], meta=['artist_id'])
albums = pd.json_normalize(data, record_path=['albums'], meta=['artist_id'])
artists = pd.json_normalize(data)

# Merge dataframes into one dataset
dataset = tracks.merge(artists, on='artist_id')
dataset = dataset.merge(albums, on='artist_id')
dataset = dataset.drop(columns=['tracks', 'albums'])

# Save dataset to csv
dataset.to_csv(csv_path, index=False)