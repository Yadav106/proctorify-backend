from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

cors = CORS(max_age=3600)
db = SQLAlchemy()

migrate = Migrate(
    render_as_batch=True
)
