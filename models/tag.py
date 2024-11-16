from typing import Dict, Any
from models import db
from models.base import Base

# Association table for many-to-many relationship between tags and time entries
time_entry_tags = db.Table('time_entry_tags',
    db.Column('time_entry_id', db.Integer, db.ForeignKey('time_entry.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Tag(Base):
    """Tag model for categorizing time entries."""
    
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(7), default='#808080')  # Default gray color
    
    # Many-to-many relationship with time entries
    entries = db.relationship('TimeEntry', 
                            secondary=time_entry_tags,
                            backref=db.backref('tags', lazy=True))

    def to_dict(self) -> Dict[str, Any]:
        """Convert tag to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color
        }
