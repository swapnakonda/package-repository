import csv
import re
from validations import validate_email

file = open(r'C:\Users\user\CogniBots-Project\package-repository\profile.csv')
data = csv.reader(file)
print(data)
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
for row in data:
        print('row - ', row)
        email = row[0]
        email_validation_response = validate_email(email)
        print('email validation response - ', email_validation_response)
        if email_validation_response is not None:
                # store the complete row in dynamo





