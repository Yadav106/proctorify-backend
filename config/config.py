import os
from celery import Celery
from utils.common import get_current_directory
import datetime

class ProdConfig:
    debug = os.environ.get("DEBUG")
    SO_DEMO_SETUP = os.environ.get("SO_DEMO_SETUP")
    DEBUG = False
    if debug == "true" or debug == "True":
        DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + get_current_directory() + '/data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    CELERY_BROKER_URL = 'redis://{host}:{port}/{db}'.format(
        host=os.environ.get("REDIS_HOST"),
        port=os.environ.get("REDIS_PORT"),
        db=os.environ.get("REDIS_DB_NUMBER")
    )

    CELERY_RESULT_BACKEND= 'redis://{host}:{port}/{db}'.format(
        host=os.environ.get("REDIS_HOST"),
        port=os.environ.get("REDIS_PORT"),
        db=os.environ.get("REDIS_DB_NUMBER")
    )

celery_app = Celery(
    __name__,
    backend=ProdConfig.CELERY_RESULT_BACKEND,
    broker=ProdConfig.CELERY_BROKER_URL
)
