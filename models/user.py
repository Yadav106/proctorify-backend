from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from config.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        password_hash = generate_password_hash(password)
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
