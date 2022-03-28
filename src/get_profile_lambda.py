from src.exceptions.custom_exceptions import EventInputValidationException
from src.profile_business import get_profile_based_on_email


def construct_response(status_code: int, status_message: str, payload: list):
    client_response = {
        'code': status_code,
        'message': status_message,
        'payload': payload
    }
    return client_response


def lambda_handler(event, context):
    try:
        email_value = event["queryStringParameters"]["email"]
        if email_value is None:
            print('Input email is none')
            raise EventInputValidationException("invalid email")
        # BusinessLayer
        sent_response = get_profile_based_on_email(email_value)
        if sent_response is not None:
            print(f'record found for the {email_value} given')
        return construct_response(200,f'data found',sent_response)
    except EventInputValidationException as ex:
        print('EventInputValidationException Occurred - ', ex.args)
        return construct_response(400,f'validation failed-{ex.args}',[])
    except Exception as e:
        print('Mother exception as thrown -', e.args)
        return construct_response(500, 'Internal Server Error', [])

        
      
