import profile_dao
from exceptions.custom_exceptions import EventInputValidationException


def construct_response(status_code: int, status_message: str, payload: list):
    client_response = {
        'code': status_code,
        'message': status_message,
        'payload': payload
    }
    return client_response


def lambda_handler(event, context):
    # input
    print(f'event - {event}')
    try:
        bucket_name: str = event['Records'][0]['s3']['bucket']['name']
        region: str = event['Records'][0]['awsRegion']
        file_name: str = event['Records'][0]['s3']['object']['key']
        # validations
        if bucket_name is None:
            print('bucket name is empty')
            raise EventInputValidationException('No bucket config')

        if region is None:
            print('region is empty')
            raise EventInputValidationException('Region is empty')

        if file_name is None:
            print('file name is empty')
            raise EventInputValidationException('File Name is empty')

        email = file_name.replace('.pdf', '').rstrip()
        url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{file_name}"

        # Business
        response = profile_dao.update_profile(email, url)
        if response is not None:
            return construct_response(200, 'Successfully updated profile', [])

    except EventInputValidationException as ex:
        print('EventInputValidationException Occurred - ', ex.args)
        return construct_response(400, f'Input Validation Errors - {ex.args}', [])
    except Exception as e:
        print('Mother exception as thrown -', e.args)
        return construct_response(500, 'Internal Server Error', [])
