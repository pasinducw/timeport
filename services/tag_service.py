"""Service for managing tags."""

from typing import List, Optional
from models import db, Tag, TimeEntry

class TagService:
    @staticmethod
    def create_tag(name: str, color: Optional[str] = None) -> Tag:
        """Create a new tag.
        
        Args:
            name: Name of the tag.
            color: Optional hex color code (e.g., '#ff0000').
            
        Returns:
            The created tag.
            
        Raises:
            ValueError: If tag with name already exists.
        """
        if Tag.query.filter_by(name=name).first():
            raise ValueError(f"Tag '{name}' already exists")
            
        tag = Tag(name=name, color=color)
        db.session.add(tag)
        db.session.commit()
        return tag
    
    @staticmethod
    def get_tag(tag_id: int) -> Tag:
        """Get a tag by ID."""
        return Tag.query.get_or_404(tag_id)
    
    @staticmethod
    def list_tags() -> List[Tag]:
        """List all tags ordered by name."""
        return Tag.query.order_by(Tag.name).all()
    
    @staticmethod
    def update_tag(tag_id: int, name: Optional[str] = None,
                  color: Optional[str] = None) -> Tag:
        """Update a tag's details."""
        tag = Tag.query.get_or_404(tag_id)
        
        if name and name != tag.name:
            if Tag.query.filter_by(name=name).first():
                raise ValueError(f"Tag '{name}' already exists")
            tag.name = name
            
        if color is not None:
            tag.color = color
            
        db.session.commit()
        return tag
    
    @staticmethod
    def delete_tag(tag_id: int) -> None:
        """Delete a tag.
        
        Note: This will remove the tag from all associated time entries.
        """
        tag = Tag.query.get_or_404(tag_id)
        db.session.delete(tag)
        db.session.commit()
        
    @staticmethod
    def add_tag_to_entry(entry_id: int, tag_id: int) -> TimeEntry:
        """Add a tag to a time entry."""
        entry = TimeEntry.query.get_or_404(entry_id)
        tag = Tag.query.get_or_404(tag_id)
        
        if tag not in entry.tags:
            entry.tags.append(tag)
            db.session.commit()
            
        return entry
    
    @staticmethod
    def remove_tag_from_entry(entry_id: int, tag_id: int) -> TimeEntry:
        """Remove a tag from a time entry."""
        entry = TimeEntry.query.get_or_404(entry_id)
        tag = Tag.query.get_or_404(tag_id)
        
        if tag in entry.tags:
            entry.tags.remove(tag)
            db.session.commit()
            
        return entry
