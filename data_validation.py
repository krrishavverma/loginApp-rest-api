import json
import re
import datetime
import time

def user_data_validation(self, userDetail):
    gender_match = False
    date0fbirth_match = False

    user_password = userDetail['password']
    password_expression = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&].{8,}"
    password_pattern = re.compile(password_expression) 
    password_match = re.search(password_pattern, user_password)

    user_email = userDetail['email']
    email_expression = "^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$"
    email_pattern = re.compile(email_expression) 
    email_match = re.search(email_pattern, user_email)

    user_phone = str(userDetail['phone'])
    phone_expression = "(0/91)?[7-9][0-9]{9}"
    phone_pattern = re.compile(phone_expression) 
    phone_match = re.search(phone_pattern, user_phone)

    user_gender = userDetail['gender']
    if (user_gender == "Male" or user_gender == "Female" or user_gender == "Other"):
        gender_match = True

    user_dateofbirth = userDetail['dateofbirth']
    isValidDate = False
    try :
        if (user_dateofbirth[4] == '-' and user_dateofbirth[7] == '-'):
            isValidDate = True
        if isValidDate:
            year,month,day = user_dateofbirth.split('-')
            datetime.datetime(int(year),int(month),int(day))
    except ValueError :
        isValidDate = False

    if (isValidDate and len(month) == 2 and len(day) == 2 and len(year) == 4):
        currentDate = (time.strftime("%m-%d-%Y"))

        currentMonth, currentDay, currentYear = currentDate.split('-')

        if currentYear > year:
            date0fbirth_match = True
        elif currentYear == year:
            if currentMonth > month:
                date0fbirth_match = True
            elif currentMonth == month:
                if currentDay >= day:
                    date0fbirth_match = True
            else:
                date0fbirth_match = False
        else:
            date0fbirth_match = False

    if (password_match and email_match and phone_match and gender_match and date0fbirth_match):
        return True
    else:
        return False
