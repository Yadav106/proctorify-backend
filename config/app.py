import logging

from flask import Flask
from celery import Celery
from config.config import ProdConfig
from config.extensions import db, migrate, cors
from utils.constants import (
    API_URL_PREFIX
)

from utils.custom_exception import CustomException
from config.error_handlers import handle_invalid_usage
from utils.response import set_response

def create_app(config_obj):
    """
    Creates and configures an instance of a flask application
    """
    app = Flask(__name__)

    app.config.from_object(config_obj)

    if app.config['DEBUG']:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    app.jinja_env.globals.update(isinstance=isinstance)
    app.jinja_env.globals.update(enumerate=enumerate)
