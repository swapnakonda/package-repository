from src.exceptions.custom_exceptions import EventInputValidationException
from src.profile_business import get_profile_based_on_email
from http import HTTPStatus


def construct_response(status_code: int, status_message: str, payload: list):
    client_response = {
        'code': status_code,
        'message': status_message,
        'payload': payload
    }
    return client_response


def lambda_handler(event, context):
    """
    This lambda gives a profile based on the email given
    :param event: We take the email in the event as input
    :param context:
    :return: We send success along with profile data  when the profile is present in profile table
            200 - Success
            400 - BadRequest
            500 - InternalServerError
    """
    try:
        # input email reading
        email_value = event["queryStringParameters"]["email"]
        if email_value is None:
            print('Input email is none')
            raise EventInputValidationException("invalid email")

        # BusinessLayer
        sent_response = get_profile_based_on_email(email_value)

        # validations
        if sent_response is not None:
            print(f'record found for the {email_value} given')
        return construct_response(HTTPStatus.OK, f'data found', sent_response)
    except EventInputValidationException as ex:
        print('EventInputValidationException Occurred - ', ex.args)
        return construct_response(HTTPStatus.BAD_REQUEST, f'validation failed-{ex.args}', [])
    except Exception as e:
        print('Mother exception as thrown -', e.args)
        return construct_response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error', [])
