import re

from profile_dao import put_item

regex_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
regex_phone = re.compile(r'(^[6-9]\d{9}$)')


def profile_operations(records):
    for row in records:
        print(row['email'])
        email_validation_response = re.fullmatch(regex_email, row['email'])
        phone_validation_response = re.fullmatch(regex_phone, row['phone'])
        if email_validation_response is not None and phone_validation_response is not None:
            put_item(row)
        else:
            print("alarm")
