import csv

import boto3

from src.profile_business import profile_operations


def lambda_handler(event, context):
    print(f'event - {event}')
    print('event key object -', event['Records'][0]['s3']['object']['key'])
    object_key_value: str = event['Records'][0]['s3']['object']['key']
    bucket_name: str = event['Records'][0]['s3']['bucket']['name']

    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=object_key_value)
    data = obj['Body'].read().decode('utf-8').splitlines()
    records = csv.DictReader(data)
    profile_operations(records)
    final_response = {
        'status_code': 200,
        'status_message': 'Succesfully processed profile csv'
    }
    return final_response
