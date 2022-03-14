import boto3
import moto

from unittest import TestCase
from src.profile_dao import put_item


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
        # when
        response = put_item(row)
        # then
        self.assertIsNotNone(response)
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        print(status_code)
        self.assertEqual(200, status_code)

