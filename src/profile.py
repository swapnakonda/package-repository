import csv

import boto3


def lambda_handler(event, context):
    print('')
    # Read the data from S3

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('csv-profile-management')
    obj = s3.get_object(Bucket='csv-profile-management', Key='*.csv')
    data = obj['Body'].read().decode('utf-8').splitlines()
    records = csv.reader(data)
    print(records)
    validate_email_phone(records)




def validate_email_phone(records):
    for row in records:

    #proces the data into dynamo