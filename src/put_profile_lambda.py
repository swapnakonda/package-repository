import csv
from http import HTTPStatus

import boto3

from src import profile_business
from src.exceptions.custom_exceptions import EventInputValidationException


def lambda_handler(event, context):
    """
    This lambda process the csv into profile table.
    :param event:
    :param context:
    :return:
           200 - Success
           400 - BadRequest
           500 - InternalServerError
    """
    print(f'event - {event}')
    try:
        # input reading
        file_name: str = event['Records'][0]['s3']['object']['key']
        bucket_name: str = event['Records'][0]['s3']['bucket']['name']

        print(f'lambda_handler:event file_name - {file_name}')
        print(f'lambda_handler:event bucket_name - {bucket_name}')

        # validations
        if bucket_name is None:
            print("there is no bucket")
            raise EventInputValidationException("no bucket configuration")

        if file_name is None:
            print("there are no csv files in the bucket")
            raise EventInputValidationException("no csv files")

        # reading data from s3
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket_name, Key=file_name)
        data = obj['Body'].read().decode('utf-8').splitlines()
        if data is None:
            message = 'unable to decode the data'
            print(f"error occurred {message}")
            raise EventInputValidationException(message)
        records = csv.DictReader(data)

        # business
        no_of_records, response_list = profile_business.profile_operations(records)
        print('lambda_handler:no_of_records - ', no_of_records)
        print('lambda_handler:response_list - ', response_list)

        if no_of_records == len(response_list):
            final_response = construct_response(HTTPStatus.OK, f'Successfully processed {file_name}', [])
        else:
            final_response = construct_response(HTTPStatus.INTERNAL_SERVER_ERROR,
                                                f'Error occurred while  processing {file_name}', [])

    except EventInputValidationException as obj:
        print('EventInputValidationException occurred - ', obj.args)
        final_response = construct_response(HTTPStatus.BAD_REQUEST, 'Validation failed', [])

    return final_response


def construct_response(code: int, message: str, payload: list):
    final_response = {
        'status_code': code,
        'status_message': message,
        'payload': payload
    }
    return final_response
