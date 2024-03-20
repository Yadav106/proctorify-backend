from flask import Blueprint, request
from flask import current_app as app
from models.user import User
from models.team import Team
from models.meeting import Meeting
from utils.custom_exception import InternalError
from utils.response import set_response
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

meeting_api = Blueprint("meeting_api", __name__)

@meeting_api.route("/meeting/new", methods=["POST"])
@jwt_required()
def new_meeting():
    err_msg = None
    try:
        print('khichdi pak rhi hai')
        user_identity = get_jwt_identity()
        username = user_identity.get('username', None)
        user = User.query.filter_by(username=username).one_or_none()
        if not user:
            err_msg = "User not found"
            raise

        if not request.is_json:
            err_msg = "Request is not json"
            raise

        if request.json is None:
            err_msg = "Request json is None"
            raise
        return set_response({"data" : "nice"})
    except Exception as ex:
        raise InternalError(err_msg, ex)
