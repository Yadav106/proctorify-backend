import os
from pathlib import Path
from flask import current_app as app
from utils.constants import (
    MIN_PASSWORD_LENGTH
)

def get_home_directory():
    return str(Path.home())

def get_current_directory():
    return os.getcwd()

def password_policy_check(password):
    msg = "success"
    if len(password) < MIN_PASSWORD_LENGTH:
        msg = "Min password length is {}".format(MIN_PASSWORD_LENGTH)
        return False, msg
    elif not validate_password_policy(password)[0]:
        return False, "Please choose a stronger password"
    else:
        return True, msg

def validate_password_policy(password):
    """
    Password should contain
        - at least 1 uppercase character (A-Z)
        - at least 1 lowercase character (a-z)
        - at least 1 digit (0-9)
        - at least 1 special character (punctuation)
    """

    msg = "At least 1 uppercase character"
    if not any(c.isupper() for c in password):
        return False, msg

    msg = "At least 1 lowercase character"
    if not any(c.islower() for c in password):
        return False, msg

    msg = "At least 1 digit"
    if not any(c.isdigit() for c in password):
        return False, msg

    msg = "At least 1 special character (punctuation)"
    special_chars = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    if not any(c in special_chars for c in password):
        return False, msg

    msg = "valid"
    return True, msg
