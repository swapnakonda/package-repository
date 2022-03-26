import csv

import boto3

from src import profile_business
from src.exceptions.custom_exceptions import EventInputValidationException


def lambda_handler(event, context):
    print(f'event - {event}')
    try:
        print('event key object -', event['Records'][0]['s3']['object']['key'])
        object_key_value: str = event['Records'][0]['s3']['object']['key']
        bucket_name: str = event['Records'][0]['s3']['bucket']['name']
        if bucket_name is None:
            print("there is no bucket")
            raise EventInputValidationException("no bucket configuration")
        if object_key_value is None:
            print("there are no csv files in the bucket")
            raise EventInputValidationException("no csv files")
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket_name, Key=object_key_value)
        data = obj['Body'].read().decode('utf-8').splitlines()
        if data is None:
            print("unable to decode the data")
            raise EventInputValidationException("decoding error")
        records = csv.DictReader(data)
        response_list = profile_business.profile_operations(records)
        if len(records) == len(response_list):
            final_response =  construct_response(200, f'Successfully processed {object_key_value}', [])
        else:
            final_response = construct_response(500, f'Error occurred while  processing {object_key_value}', [])
    except EventInputValidationException as obj:
        print('EventInputValidationException occurred - ', obj.args)
        final_response = construct_response(400, 'Validation failed',[])

    return final_response


def construct_response(code: str, message: str, payload: list):
    final_response = {
        'status_code': code,
        'status_message': message,
        'payload':payload
    }
    return final_response