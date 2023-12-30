from io import StringIO
import os

import requests
import json
import logging
import boto3
from botocore.exceptions import ClientError


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




