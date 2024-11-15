from datetime import datetime
from .base import db
from .time_utils import format_to_iso8601, get_utc_now

class TimeEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=get_utc_now)
    end_time = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'description': self.description,
            'start_time': format_to_iso8601(self.start_time),
            'end_time': format_to_iso8601(self.end_time) if self.end_time else None,
            'notes': self.notes
        }
