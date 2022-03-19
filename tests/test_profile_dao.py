from unittest import TestCase

import boto3
import moto

from src import profile_dao
from src.profile_dao import upload


class ProfileDaoTest(TestCase):

    # setup method
    def setUp(self):
        print('in setup method')

    def tearDown(self):
        print('in tear down')

    def create_profile_table(self):
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

    @moto.mock_dynamodb2
    def test_put_item_success_scenario(self):
        # given
        self.create_profile_table()

        row = self.row_as_input()
        # when
        response = upload(row)
        # then
        self.assertIsNotNone(response)
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        print(status_code)
        self.assertEqual(200, status_code)

    def row_as_input(self):
        row = {
            'email': 'jeorge.mike@cogni.com',
            'first_name': 'George',
            'last_name': 'mike',
            'sur_name': 'mike',
            'dob': '1983-07-10',
            'phone': '9876231498',
            'address': 'full address',
            'stream': 'RPA'
        }
        return row

    @moto.mock_dynamodb2
    def test_get_profile(self):
        # given
        self.create_profile_table()
        row = self.row_as_input()
        upload(row)

        # when
        response = profile_dao.get_profile("jeorge.mike@cogni.com")
        print(response)

        # then
        self.assertIsNotNone(response)
        print('response is not none')
        status_code_get_item = response['ResponseMetadata']['HTTPStatusCode']
        print(status_code_get_item)
        self.assertEqual(200,status_code_get_item)
        self.assertEqual(row['email'],response['Item']['email'])
