import logging

from flask import Flask
from celery import Celery
from config.config import ProdConfig
from config.extensions import db, migrate, cors, jwt
from utils.constants import (
    API_URL_PREFIX
)

from utils.custom_exception import CustomException
from config.error_handlers import handle_invalid_usage

from api import user_api

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

    stream_handler = logging.StreamHandler()

    stream_handler.setFormatter(logging.Formatter(
        fmt='[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S %z'
    ))

    stream_handler.setLevel(log_level)

    while app.logger.handlers:
        app.logger.handlers.pop()
    app.logger.addHandler(stream_handler)

    register_blueprints(app)
    register_error_handlers(app)
    register_extensions(app)

    return app

def register_blueprints(app):
    app.register_blueprint(user_api.user_api, url_prefix=API_URL_PREFIX)

def register_extensions(app):
    cors.init_app(app, max_age=3600)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

def register_error_handlers(app):
    app.errorhandler(CustomException)(handle_invalid_usage)

app = create_app(ProdConfig)
celery_app = Celery(
        __name__, 
        backend=ProdConfig.CELERY_RESULT_BACKEND,
        broker=ProdConfig.CELERY_BROKER_URL,
    )
app.app_context().push()
