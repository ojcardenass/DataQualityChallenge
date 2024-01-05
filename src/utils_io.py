from io import StringIO, BytesIO
from pathlib import Path
import os
import re
from urllib.request import urlopen

import requests
import json
import logging
import boto3
from botocore.exceptions import ClientError
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def df_to_s3(df, bucket, csv_name):
    # Save dataframe to csv file in memory
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    # Upload csv file to s3 bucket
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, csv_name).put(Body=csv_buffer.getvalue())

def get_json_from_drive(link):
    # Get the url id
    url_id = link.split('/')[-1]
    # Construct the url to download the json file
    url = "https://drive.google.com/uc?id=" + url_id

    # Download the json file
    response = requests.get(url)
    # Convert the response to json format
    json_data = response.json()

    # Return the json data
    return json_data

def get_dataset(method):
    try:
        method = method.lower()
        if method == 's3':
            df = csv_from_s3('dataqualitychallenge', 'dataset.csv')
        elif method == 'url':         
            # Get the csv file from the url
            url = "https://dataqualitychallenge.s3.us-east-2.amazonaws.com/dataset.csv"
            with urlopen(url) as conn:
                df = pd.read_csv(conn)

        elif method == 'local':
            # Paths to input and output folders | Local version
            base_path = Path(os.getcwd())
            output_path = os.path.join(base_path, 'output')
            csv_name = 'dataset.csv'
            csv_path = os.path.join(output_path, csv_name)
            df = pd.read_csv(csv_path)
        return df
    except:
        raise ValueError('Invalid method')
        


def csv_from_s3(bucket, csv_name):
    # Download csv file from s3 bucket
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=csv_name)
    df = pd.read_csv(obj['Body'])
    return df

def contains_bad_encoding(value):
    # Apostrophe bad decoded
    a = '’'.encode('utf-8').decode('cp1252')
    b = '‘'.encode('utf-8').decode('cp1252')
    
    # Function to check if a value contains bad encoding characters
    regex = re.compile(f'[‘’{a}{b}]')
    # Check if the value contains bad encoding characters
    if regex.search(value) is not None:
        return True
    else:
        return False

# Function to test if a string can be converted to a float value
def can_be_converted(value):
    try:
        float_value = float(value)
        return True
    except ValueError:
        return False
    
def multiple_row_height(row_height, data):
    # List of row heights
    multiple_row_heights = [row_height] * len(data)
    # Define the height for shading the second row
    multiple_row_heights[1] = row_height / 5
    # Define a smaller height for rows beyond the second row
    for i in range(2, len(data)):
        multiple_row_heights[i] = row_height / 2.8

    return multiple_row_heights

# Auxiliar functions for graph ploting
def donut_plot(data, title):
    # Create a pieplot        
    plt.subplots()
    plt.pie(data, colors=sns.color_palette('Accent'))
    # add a circle at the center to transform it into a donut chart
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    # Set the title of the graph
    plt.title(title, fontsize=18)

    # Add annotation in the center of the figure
    percentage = (1 - (data[1] / data[0])) * 100
    plt.text(0, 0, f'{percentage:.1f}%', horizontalalignment='center', verticalalignment='center', fontsize=20)

    # Save the image as a stream of in-memory bytes
    imgdata = BytesIO()
    plt.savefig(imgdata, format='png', bbox_inches='tight')
    imgdata.seek(0)  # rewind the data

    return imgdata

def pie_plot(data, title, labels):
    # Create a pieplot        
    plt.subplots()
    plt.pie(data, colors=sns.color_palette('Accent'), labels=labels, autopct='%1.0f%%')

    # Set the title of the graph
    plt.title(title, fontsize=16)

    # Save the image as a stream of in-memory bytes
    imgdata = BytesIO()
    plt.savefig(imgdata, format='png', bbox_inches='tight')
    imgdata.seek(0)  # rewind the data

    return imgdata