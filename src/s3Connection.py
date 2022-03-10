import boto3
import csv

s3 = boto3.resource('s3')
bucket = s3.Bucket('csv-profile-management')
obj = s3.get_object(Bucket='csv-profile-management', Key='*.csv')
data = obj['Body'].read().decode('utf-8').splitlines()
records = csv.reader(data)


