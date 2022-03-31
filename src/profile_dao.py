import boto3


def upload(row):
    dynamodb = boto3.resource('dynamodb', region_name='cn-northwest-1')
    table_obj = dynamodb.Table('Profile')
    response = table_obj.put_item(
        Item={
            'email': row['email'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'sur_name': row['sur_name'],
            'dob': row['dob'],
            'phone': row['phone'],
            'address': row['address'],
            'stream': row['stream']
        }
    )
    print(f'profile_dao:response from profile put_item:-{response}')
    return response


def get_profile(email):
    dynamodb_obj = boto3.resource('dynamodb', region_name='cn-northwest-1')
    table = dynamodb_obj.Table('Profile')
    response = table.get_item(
        Key={
            'email': email
        })
    return response


def update_profile(email, url):
    dynamodb_obj = boto3.resource('dynamodb', region_name='cn-northwest-1')
    table = dynamodb_obj.Table('Profile')
    response_update = table.update_item(
        Key={'email': email},
        UpdateExpression="set s3url=:u",
        ExpressionAttributeValues={":u": url},
        ReturnValues="UPDATED_NEW"
    )
    print(f'update profile response - {response_update}')
    return response_update
