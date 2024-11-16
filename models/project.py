from typing import Dict, Any
from models import db
from models.base import Base

class Project(Base):
    """Project model for grouping time entries."""
    
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # Relationship to time entries
    entries = db.relationship('TimeEntry', backref='project', lazy=True)

    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
