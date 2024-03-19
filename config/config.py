import os
from celery import Celery
from utils.common import get_current_directory

class ProdConfig:
    debug = os.environ.get("DEBUG")
    SO_DEMO_SETUP = os.environ.get("SO_DEMO_SETUP")
    DEBUG = False
    if debug == "true" or debug == "True":
        DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + get_current_directory() + '/data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
