from flask import Blueprint, request
from flask import current_app as app
from utils.common import password_policy_check
from utils.custom_exception import InternalError
from werkzeug.security import generate_password_hash
import phonenumbers

from utils.response import set_response

from models.user import User

user_api = Blueprint("user_api", __name__)

@user_api.route("/check", methods=["GET"])
def check():
    return set_response("checking")

@user_api.route("/users/register", methods=["POST"])
def register():
    err_msg = None
    email = None
    try:
        if not request.is_json:
            err_msg = "Missing body in request"
            raise

        if request.json is None:
            err_msg = "Request json is none"
            raise

        name = request.json.get("name", None)
        if not name:
            err_msg = "Name not provided"
            raise

        email = request.json.get("email", None)
        if not email:
            err_msg = "Email not provided"
            raise

        phone_number = request.json.get("phone_number", None)
        if not phone_number:
            err_msg = "Phone Number not provided"
            raise
        try:
            if not phonenumbers.is_valid_number(phonenumbers.parse(phone_number)):
                err_msg = "Invalid phone number"
                raise
            phone_number = phonenumbers.format_number(phonenumbers.parse(phone_number), phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except Exception as ex:
            err_msg = "Invalid phone number"
            raise

        username = request.json.get("username", None)
        if not username:
            err_msg = "Username not provided"
            raise

        password = request.json.get("password", None)
        if not password:
            err_msg = "Password not provided"
            raise

        is_password_valid, msg = password_policy_check(password)
        if not is_password_valid:
            err_msg = msg
            raise
        else:
            password = generate_password_hash(password)

        user = User(
            name=name,
            email=email,
            phone_number=phone_number,
            username=username,
            password_hash=password
        )

        try:
            user.save()
        except Exception as ex:
            err_msg = "Error while saving user"
            raise

        return set_response({msg : "User registered"})

    except Exception as ex:
        if not err_msg:
            err_msg = "Error while registering a user"
        app.logger.error("User %s registration failed. Error message : %s. Exception : %s", email, err_msg, ex)
        raise InternalError(err_msg)
        
@user_api.route("/users/login", methods=["POST"])
def login():
    err_msg = None
    email = None
    try:
        if not request.is_json:
            err_msg = "Missing body in request"
            raise

        if request.json is None:
            err_msg = "Request body is none"
            raise

        username = request.json.get("username")
        if not username:
            err_msg = "Username not found in request"
            raise

        password = request.json.get("password")
        if not password:
            err_msg = "Password not found in request"
            raise

        user = User.query.filter_by(username=username).first()
        if not user:
            err_msg = "User not found"
            raise

        if not user.check_password(password):
            err_msg = "Invalid credentials"
            raise

        return set_response({"msg" : "Authenticated"})
    except Exception as ex:
        if not err_msg:
            err_msg = "Error while logging in"

        app.logger.error("Error while logging in user %s. Error message : %s. Exception %s", email, err_msg, ex)
        raise InternalError(err_msg);


