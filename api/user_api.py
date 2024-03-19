from flask import Blueprint
from flask import current_app as app

from utils.response import set_response


user_api = Blueprint("user_api", __name__)

@user_api.route("/check", methods=["GET"])
def check():
    return set_response("checking")
