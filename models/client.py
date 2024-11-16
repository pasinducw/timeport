from typing import Dict, Any
from models import db
from models.base import Base

class Client(Base):
    """Client model for associating time entries with clients."""
    
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(200))
    notes = db.Column(db.Text)
    
    # Relationship to time entries
    entries = db.relationship('TimeEntry', backref='client', lazy=True)

    def to_dict(self) -> Dict[str, Any]:
        """Convert client to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'notes': self.notes
        }
