from flask import Blueprint, request
from flask import current_app as app
from utils.custom_exception import InternalError
from utils.response import set_response
from models.team import Team

team_api = Blueprint("team_api", __name__)
