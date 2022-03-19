import csv

import boto3

from src import profile_business
from src.profile_dao import get_profile

def lambda_handler(event, context):
    print(f'event - {event}')
    print('event key object -', event['Records'][0]['s3']['object']['key'])
    object_key_value: str = event['Records'][0]['s3']['object']['key']
    bucket_name: str = event['Records'][0]['s3']['bucket']['name']

    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=object_key_value)
    data = obj['Body'].read().decode('utf-8').splitlines()
    records = csv.DictReader(data)
    profile_business.profile_operations(records)
    final_response = {
        'status_code': 200,
        'status_message': 'Succesfully processed profile csv'
    }
    return final_response


def lambda_handler_database_update(event, context):
    event = {
        "resource": "/",
        "path": "/",
        "httpMethod": "GET",
        "requestContext": {
            "resourcePath": "/",
            "httpMethod": "GET",
            "path": "/Prod/"
        },
        "headers": {
            "accept": "text/html",
            "accept-encoding": "gzip, deflate, br",
            "Host": "xxx.us-east-2.amazonaws.com",
            "User-Agent": "Mozilla/5.0"
        },
        "multiValueHeaders": {
            "accept": [
                "json"
            ],
            "accept-encoding": [
                "gzip, deflate, br"
            ],

        },
        "queryStringParameters": {
            "postcode": 12345,
            "email": "jeorge.mike@cogni.com"
        },

    }


    email_value = event["queryStringParameters"]["email"]

    #BusinessLayer
    profile_business.get_profile_based_on_email(email_value)



