from pathlib import Path
import json
import os

import pandas as pd

base_path = Path(os.getcwd())
output_path = os.path.join(base_path, 'output')
csv_name = 'dataset.csv'
csv_path = os.path.join(output_path, csv_name)

# Read the CSV file
df = pd.read_csv(csv_path)

# Perform data analysis
# Example: Get the number of rows and columns in the dataset
num_rows = df.shape[0]
num_cols = df.shape[1]

# Example: Get the summary statistics of numerical columns
summary_stats = df.describe()


# Example: Get the unique values in a specific column
unique_values = {}
for column in df.columns:
    unique_values[column] = df[column].unique()

disc_number_unique_values = df['disc_number'].unique()

# Example: Perform data filtering
filtered_data = df[df['column_name'] > 10]

# Example: Perform data aggregation
aggregated_data = df.groupby('column_name').mean()

# Example: Plotting data
df['column_name'].plot(kind='hist')

# Example: Save the analyzed data to a new CSV file
df.to_csv('analyzed_dataset.csv', index=False)
