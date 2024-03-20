from config.extensions import db
from sqlalchemy import ForeignKey, Boolean

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    leader_id = db.Column(db.Integer, ForeignKey('user.id'))
    leader = db.relationship('User', backref='teams')
    code = db.Column(db.String(200), nullable=True)
    ongoing = db.Column(Boolean, nullable=True)

    members = db.relationship('User', secondary='team_members', backref="joined_teams")

    def __init__(self, name, leader_id, members=None):
        self.name = name
        self.leader_id = leader_id
        self.members = members or []
        self.code = None
        self.ongoing = False

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise

    def __repr__(self) -> str:
        return '<Team {}>'.format(self.name)


team_members = db.Table('team_members',
    db.Column('team_id', db.Integer, ForeignKey('team.id'), primary_key=True),
    db.Column('user_id', db.Integer, ForeignKey('user.id'), primary_key=True)
)
