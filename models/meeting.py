from config.extensions import db
from sqlalchemy import ForeignKey, DateTime, Enum

class MeetingStatus(Enum):
    upcoming = "upcoming"
    ongoing = "ongoing"
    completed = "completed"

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start = db.Column(DateTime, nullable=False)
    notes = db.Column(db.Text)

    attendees = db.relationship('User', secondary='meeting_attendees', backref="meetings")
    status = db.Column(MeetingStatus, nullable=False, default=MeetingStatus.upcoming)

    team_id = db.Column(db.Integer, ForeignKey('team.id'))
    team = db.relationship('Team', backref='meetings')

    def __init__(self, title, start, notes=None, attendees=None, status=MeetingStatus.upcoming, team=None):
        self.title = title
        self.start = start
        self.notes = notes
        self.attendees = attendees or []
        self.status = status
        self.team = team

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise

    def __repr__(self) -> str:
        return '<Meeting {} - {} ({})'.format(self.title, self.start.strftime("%Y-%m-%d %H:%M"), self.status)

meeting_attendees = db.Table('meeting_attendees',
  db.Column('meeting_id', db.Integer, ForeignKey('meeting.id'), primary_key=True),
  db.Column('user_id', db.Integer, ForeignKey('user.id'), primary_key=True)
)
