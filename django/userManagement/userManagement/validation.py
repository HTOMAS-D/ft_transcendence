import re

def passwordValidation(password) -> bool:
    # Check password length
    if (len(password) < 8):
        return False
    # Check if password contains any numbers
    if (not any(c.isdigit() for c in password)):
        return False

    # Check for upper case letter
    if (not any(c.isupper() for c in password)):
        return False

    # Check allowed special characters
    s_c = " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    if (not any(c in password for c in s_c)):
        return False

    a_c = 'abcdefghijklmnopqrstuvwxyz' +\
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +\
          '0123456789' +  s_c
    # Check if something is not in )the allowed character list
    if (any(c not in a_c for c in password)):
        return False
    return True

def emailValidation(email) -> bool:
    return re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)

def usernameValidation(uname) -> bool:
    return re.fullmatch(r"([A-Z]|[a-z]|_|-|[1-9])+", uname) and len(uname) >= 3