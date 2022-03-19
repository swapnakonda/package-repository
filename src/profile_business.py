import re

from src import profile_dao

regex_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
regex_phone = re.compile(r'(^[6-9]\d{9}$)')


def profile_operations(records):
    for row in records:
        print(row['email'])
        email_validation_response = re.fullmatch(regex_email, row['email'])
        phone_validation_response = re.fullmatch(regex_phone, row['phone'])
        if email_validation_response is not None and phone_validation_response is not None:
            profile_dao.upload(row)
        else:
            print("alarm")


def get_profile_based_on_email(email):
    response = profile_dao.get_profile(email)
    print('response - ', response)
    if response is None:
        http_response = {
            'status_code': 200,
            'status_messg': f'There is no profile found for email - {email}'
        }
        return http_response
    sent_response = {
        'status_code': 200,
        'status_message': response
    }
    return sent_response


