from datetime import datetime
from .base import db
from .time_utils import format_to_iso8601, get_utc_now

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=get_utc_now)
    end_time = db.Column(db.DateTime)
    entries = db.relationship('TimeEntry', backref='session', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_time': format_to_iso8601(self.start_time),
            'end_time': format_to_iso8601(self.end_time) if self.end_time else None,
            'entry_count': len(self.entries)
        }
