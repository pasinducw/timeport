from datetime import datetime
from typing import Dict, Any, Optional, List
from models import db, time_utils
from models.base import Base

class TimeEntry(Base):
    """Represents a single time tracking entry.
    
    A time entry records a specific task or activity within a session.
    It has a description, start time, optional end time, and optional notes.
    It can be associated with a project, client, and multiple tags.
    
    Attributes:
        id: Unique identifier for the entry.
        session_id: ID of the session this entry belongs to.
        project_id: Optional ID of the associated project.
        client_id: Optional ID of the associated client.
        description: Description of the tracked activity.
        start_time: UTC timestamp when the entry started.
        end_time: UTC timestamp when the entry ended, or None if still active.
        notes: Optional additional notes about the entry.
    """
    
    __tablename__ = 'time_entry'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    description = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=time_utils.get_utc_now)
    end_time = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    def to_dict(self) -> Dict[str, Any]:
        """Convert time entry to dictionary representation."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'project_id': self.project_id,
            'client_id': self.client_id,
            'project': self.project.to_dict() if self.project else None,
            'client': self.client.to_dict() if self.client else None,
            'description': self.description,
            'start_time': time_utils.format_to_iso8601(self.start_time),
            'end_time': time_utils.format_to_iso8601(self.end_time) if self.end_time else None,
            'notes': self.notes,
            'tags': [tag.to_dict() for tag in self.tags]
        }
