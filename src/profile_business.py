import csv
import re
import boto3

regex_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
regex_phone = re.compile(r'(^[6-9]\d{9}$)')


def profile_validation():
    with open(r'C:\Users\user\CogniBots-Project\package-repository\profile.csv') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            print(row['email'])
            email_validation_response = re.fullmatch(regex_email, row['email'])
            phone_validation_response = re.fullmatch(regex_phone, row['phone'])
            if email_validation_response is not None and phone_validation_response is not None:
                put_item_into_dynamodb(row)
            else:
                print("alarm")


def put_item_into_dynamodb(row):
    dynamodb = boto3.resource('dynamodb')
    tableobj = dynamodb.Table('Profile')
    tableobj.put_item(
        Item={
            'email': row['email'],
            'first_name':row['first_name'],
            'last_name' : row['last_name'],
            'sur_name' : row['sur_name'],
            'dob' : row['dob'],
            ''


    }

    )