import boto3


def put_item(row):
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
    print(f'response from put_item:-{response}')
    return response
