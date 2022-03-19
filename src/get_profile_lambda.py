from src.profile_business import get_profile_based_on_email


def lambda_handler(event, context):

    email_value = event["queryStringParameters"]["email"]
    if email_value is None:
        print('Input email is none')
        http_response = {
            'status_code': 400,
            'error_message': 'given email is empty'
        }
        return http_response

    # BusinessLayer
    sent_response = get_profile_based_on_email(email_value)
    return sent_response
