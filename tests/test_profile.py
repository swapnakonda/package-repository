from unittest import TestCase

import boto3
from moto import mock_s3, mock_dynamodb2

from src import put_profile_lambda, get_profile_lambda


class TestProfileLambda(TestCase):
    s3_put_event = {'Records': [{
        'eventVersion': '2.1',
        'eventSource': 'aws:s3',
        'awsRegion': 'cn-northwest-1',
        'eventTime': '2022-03-13T17:55:17.399Z',
        'eventName': 'ObjectCreated:Put',
        'userIdentity': {
            'principalId': 'AWS:AROA3WETQ3X6OFKOEJ5SS:aa100482'
        },
        'requestParameters': {
            'sourceIPAddress': '92.35.39.203'
        }, 'responseElements': {
            'x-amz-request-id': 'E4S6TSAF6JAHDJV0',
            'x-amz-id-2': 'CK6ZAxBqIoZWAT5PhomSTm9JYWo4Dr2FwIbLXwwmSJSTiKSBHDewwRdrAgG3K0vqfbeU7VOesz2o'
                          '/bnHhUZIceRDsQjK47k4'},
        's3': {
            's3SchemaVersion': '1.0',
            'configurationId': '2b20c4c9-5ab6-4a66-a585-f618fc66d9ad',
            'bucket': {
                'name': 'csv-profile-management',
                'ownerIdentity': {
                    'principalId': '803468271100'
                },
                'arn': 'arn:aws-cn:s3:::csv-profile-management'},
            'object': {
                'key': 'profile.csv',
                'size': 137, 'eTag':
                    'f123c4b9eff6863ffe72988fbce695ce',
                'sequencer': '00622E30055B4F6490'}
        }}]}
    http_get_event ={
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
            "email": "jeorge.mike@cogni.com"
        },
    }
    http_empty_event = {
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
            "email":None
        },
    }

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def create_mock_s3_bucket(self):
        # create s3 bucket since we are in motos virtual aws zccount
        s3_obj = boto3.resource('s3', region_name='cn-northwest-1')
        s3_obj.create_bucket(Bucket='csv-profile-management',
                             CreateBucketConfiguration={'LocationConstraint': 'cn-northwest-1'})

        s3_obj.Bucket('csv-profile-management') \
            .upload_file(r'C:/Users/user/CogniBots-Project/package-repository/profile.csv', 'profile.csv')

        print('Bucket and Object created')

    def create_mock_profile_dynamo_table(self):
        dynamodb = boto3.resource('dynamodb', region_name='cn-northwest-1')
        self.table = dynamodb.create_table(
            TableName='Profile',
            KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print('table created successfully')

    @mock_s3
    @mock_dynamodb2
    def test_process_csv_should_insert_data_into_profile_table(self):
        # given
        self.create_mock_s3_bucket()
        self.create_mock_profile_dynamo_table()

        # when
        final_response = put_profile_lambda.lambda_handler(self.s3_put_event, context=None)

        # then
        self.assertEqual(200, final_response['status_code'])

    @mock_s3
    @mock_dynamodb2
    def test_process_csv_should_get_data_from_profile_table(self):
        # given
        self.create_mock_s3_bucket()
        self.create_mock_profile_dynamo_table()

        # when
        put_profile_lambda.lambda_handler(self.s3_put_event, context=None)
        get_response = get_profile_lambda.lambda_handler(self.http_get_event, context=None)

        # then
        self.assertEqual(200, get_response['status_message']['ResponseMetadata']['HTTPStatusCode'])
        self.assertIsNotNone('status_message')
        print(f'get_response-{get_response}')
        self.assertEqual('jeorge.mike@cogni.com', get_response['status_message']['Item']['email'])


    def test_process_empty_email_forprofile(self):
        # given

        # when
        response = get_profile_lambda.lambda_handler(self.http_empty_event, context = None)
        # then
        self.assertEqual(400,response['status_code'])
        self.assertEqual('given email is empty',response['error_message'])
