from werkzeug.security import generate_password_hash, check_password_hash
from config.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, name, email, phone_number, username, password_hash):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.username = username
        self.password_hash = password_hash

    def set_password(self, password):
        password_hash = generate_password_hash(password)
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_identity(self):
        user_identity = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "username": self.username
        }

        return user_identity

    def save(self, commit=True):
        db.session.add(self)

        if commit:
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise

    def delete(self, commit=True):
        db.session.delete(self)

        if commit:
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise

    def __repr__(self) -> str:
        return '<User {}>'.format(self.email)
