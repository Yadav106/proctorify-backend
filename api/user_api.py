from flask import Blueprint, request
from flask import current_app as app
from utils.common import password_policy_check
from utils.custom_exception import InternalError
from werkzeug.security import generate_password_hash
from flask_jwt_extended import (
    get_jti,
    jwt_required,
    create_access_token,
    create_refresh_token,
)
from config.redisconfig import redis
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

        access_token = create_access_token(identity=user.get_identity())
        refresh_token = create_refresh_token(identity=user.get_identity())
        access_expires = app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        refresh_expires = app.config["JWT_REFRESH_TOKEN_EXPIRES"]

        access_jti = get_jti(encoded_token=access_token)
        refresh_jti = get_jti(encoded_token=refresh_token)
        if access_jti is None:
            err_msg = "access jti is none"
            raise
        if refresh_jti is None:
            err_msg = "refresh jti is None"
            raise

        redis.set(access_jti, 'false', access_expires * 1.2)
        redis.set(refresh_jti, 'false', refresh_expires * 1.2)

        return_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "msg": "New user registered"
        }

        return set_response(return_data)

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

        access_token = create_access_token(identity=user.get_identity())
        refresh_token = create_refresh_token(identity=user.get_identity())

        access_expires = app.config["JWT_ACCESS_TOKEN_EXPIRES"]
        refresh_expires = app.config["JWT_REFRESH_TOKEN_EXPIRES"]

        access_jti = get_jti(encoded_token=access_token)
        refresh_jti = get_jti(encoded_token=refresh_token)

        if access_jti is None:
            err_msg = "access jti is none"
            raise
        if refresh_jti is None:
            err_msg = "refresh jti is None"
            raise

        redis.set(access_jti, 'false', access_expires * 1.2)
        redis.set(refresh_jti, 'false', refresh_expires * 1.2)

        return_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "msg": "Authenticated"
        }

        return set_response(return_data)
    except Exception as ex:
        if not err_msg:
            err_msg = "Error while logging in"

        app.logger.error("Error while logging in user %s. Error message : %s. Exception %s", email, err_msg, ex)
        raise InternalError(err_msg);

@user_api.route("/user/get_teams", methods=["POST"])
def get_team():
    try:
        if request.json is None:
            raise
        id = request.json.get("id")
        user = User.query.filter_by(id=id).first()
        if not user:
            app.logger.error("can't fidn your user")
            raise
        joined_teams = user.joined_teams

        app.logger.info("Joined teams is %s", joined_teams)

        return set_response({"data": "Found teams, check logs"})

    except Exception as ex:
        app.logger.error("can't get error, %s", ex)
        raise InternalError(ex)
