from datetime import datetime
from typing import Dict, Any, List
from models import db, time_utils
from models.base import Base

class Session(Base):
    """Represents a time tracking session.
    
    A session is a container for time entries that represents a period of work.
    It has a start time, an optional end time, and can contain multiple time entries.
    
    Attributes:
        id: Unique identifier for the session.
        name: Display name for the session.
        start_time: UTC timestamp when the session started.
        end_time: UTC timestamp when the session ended, or None if still active.
        entries: List of time entries belonging to this session.
    """
    
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=time_utils.get_utc_now)
    end_time = db.Column(db.DateTime)
    
    # Relationship to time entries
    entries = db.relationship('TimeEntry', backref='session', lazy=True,
                            cascade='all, delete-orphan')

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'start_time': time_utils.format_to_iso8601(self.start_time),
            'end_time': time_utils.format_to_iso8601(self.end_time) if self.end_time else None,
            'entry_count': len(self.entries)
        }
