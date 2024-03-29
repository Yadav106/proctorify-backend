from flask import Blueprint, request
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
        members = [User.query.filter_by(username=i).first() for i in members_list]
        if user not in members:
            members.append(user)

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
        

@team_api.route("/team/get_all_teams", methods=["GET"])
@jwt_required()
def get_all_teams():
    err_msg = None
    try:
        user_identity = get_jwt_identity()
        username = user_identity.get('username', None)
        user = User.query.filter_by(username=username).one_or_none()
        if not user:
            err_msg = "User not found"
            raise

        teams = user.joined_teams
        
        ret = []
        for team in teams:
            leader = User.query.filter_by(id=team.leader_id).first()
            if not leader:
                err_msg = "leader not found for team {}".format(team.name)
                raise

            ret_obj = {
                "name" : team.name,
                "leader" : leader.name,
                "ongoing" : team.ongoing,
                "code" : team.code
            }

            ret.append(ret_obj)

        return set_response({"data" : ret, "msg" : "success"})
    except Exception as ex:
        if not err_msg:
            err_msg = "Error while getting all teams"
        app.logger.error("Error while getting all teams. Error message : %s. Exception %s", err_msg, ex)
        raise InternalError(err_msg)

@team_api.route("/team/start_meeting", methods=['POST'])
def start_meeting():
    err_msg = None
    try:
        if not request.is_json:
            err_msg = "Missing body in request"
            raise

        if request.json is None:
            err_msg = "Request body is none"
            raise

        code = request.json.get('code')
        if not code:
            err_msg = "code required"
            raise

        name = request.json.get('name')
        if not name:
            err_msg = "team name is required"
            raise

        team = Team.query.filter_by(name=name).first()
        if not team:
            err_msg = "no team found"
            raise

        team.ongoing = True
        team.code = code
        team.save()

        return set_response({"msg" : "meeting started"})
    except Exception as ex:
        if not err_msg:
            err_msg = "Error while creating a meet"

        app.logger.error("Error while creating a meet. Error message : %s. Exception %s", err_msg, ex)
        raise InternalError(err_msg);
