from flask import Blueprint, request, request_tearing_down
from flask import current_app as app
from models.user import User
from utils.custom_exception import InternalError
from utils.response import set_response
from models.team import Team
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)

team_api = Blueprint("team_api", __name__)

@team_api.route("/team/new", methods=["POST"])
@jwt_required()
def register_team():
    err_msg = None
    try:
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

        name = request.json.get("name", None)
        if not name:
            err_msg = "Name is required"
            raise

        members_list = request.json.get("members", None)
        members = [User.query.filter_by(id=i).first() for i in members_list]

        team = Team(
            name=name,
            leader_id=user.id,
            members=members
        )
        team.save()
        return set_response({"msg": "team saved"})
    except Exception as ex:
        if not err_msg:
            err_msg = "Error while creating a team"

        app.logger.error("Error while creating a team. Error message : %s. Exception %s",  err_msg, ex)
        raise InternalError(err_msg);
        

