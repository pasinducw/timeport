"""Service for managing time entries."""

from typing import List, Optional
from models import db, Session, TimeEntry, Tag, time_utils

class EntryService:
    @staticmethod
    def create_entry(session_id: int, description: str,
                    project_id: Optional[int] = None,
                    client_id: Optional[int] = None) -> TimeEntry:
        """Create a new time entry.
        
        Args:
            session_id: ID of the session to create entry in.
            description: Description of the time entry.
            project_id: Optional ID of the associated project.
            client_id: Optional ID of the associated client.
            
        Returns:
            The created time entry.
            
        Raises:
            404: If session is not found.
            ValueError: If trying to create entry in ended session.
        """
        session = Session.query.get_or_404(session_id)
        if session.end_time:
            raise ValueError("Cannot create entry in ended session")

        # End any active entry
        active_entry = TimeEntry.query.filter_by(
            session_id=session_id,
            end_time=None
        ).first()
        
        if active_entry:
            active_entry.end_time = time_utils.get_utc_now()
        
        # Create new entry
        entry = TimeEntry(
            session_id=session_id,
            description=description,
            project_id=project_id,
            client_id=client_id,
            start_time=time_utils.get_utc_now()
        )
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def update_entry(entry_id: int,
                    project_id: Optional[int] = None,
                    client_id: Optional[int] = None) -> TimeEntry:
        """Update a time entry's project and client associations.
        
        Args:
            entry_id: ID of the entry to update.
            project_id: Optional new project ID.
            client_id: Optional new client ID.
            
        Returns:
            The updated time entry.
            
        Raises:
            404: If entry is not found.
        """
        entry = TimeEntry.query.get_or_404(entry_id)
        
        if project_id == 0:  # Handle explicit removal
            entry.project_id = None
        elif project_id is not None:
            entry.project_id = project_id
            
        if client_id == 0:  # Handle explicit removal
            entry.client_id = None
        elif client_id is not None:
            entry.client_id = client_id
            
        db.session.commit()
        return entry

    @staticmethod
    def add_tag_to_entry(entry_id: int, tag_id: int) -> TimeEntry:
        """Add a tag to a time entry.
        
        Args:
            entry_id: ID of the entry.
            tag_id: ID of the tag to add.
            
        Returns:
            The updated time entry.
            
        Raises:
            404: If entry or tag is not found.
        """
        entry = TimeEntry.query.get_or_404(entry_id)
        tag = Tag.query.get_or_404(tag_id)
        
        if tag not in entry.tags:
            entry.tags.append(tag)
            db.session.commit()
            
        return entry

    @staticmethod
    def remove_tag_from_entry(entry_id: int, tag_id: int) -> TimeEntry:
        """Remove a tag from a time entry.
        
        Args:
            entry_id: ID of the entry.
            tag_id: ID of the tag to remove.
            
        Returns:
            The updated time entry.
            
        Raises:
            404: If entry or tag is not found.
        """
        entry = TimeEntry.query.get_or_404(entry_id)
        tag = Tag.query.get_or_404(tag_id)
        
        if tag in entry.tags:
            entry.tags.remove(tag)
            db.session.commit()
            
        return entry

    @staticmethod
    def stop_entry(session_id: int) -> Optional[TimeEntry]:
        """Stop the active entry in a session."""
        session = Session.query.get_or_404(session_id)
        if session.end_time:
            raise ValueError("Session has ended")
            
        active_entry = TimeEntry.query.filter_by(
            session_id=session_id,
            end_time=None
        ).first()
        
        if not active_entry:
            raise ValueError("No active time entry")
            
        active_entry.end_time = time_utils.get_utc_now()
        db.session.commit()
        return active_entry

    @staticmethod
    def update_notes(entry_id: int, notes: str) -> TimeEntry:
        """Update the notes of a time entry."""
        entry = TimeEntry.query.get_or_404(entry_id)
        entry.notes = notes
        db.session.commit()
        return entry

    @staticmethod
    def delete_entry(entry_id: int) -> None:
        """Delete a time entry."""
        entry = TimeEntry.query.get_or_404(entry_id)
        db.session.delete(entry)
        db.session.commit()

    @staticmethod
    def list_entries(session_id: int) -> List[TimeEntry]:
        """List all entries in a session ordered by start time."""
        return TimeEntry.query.filter_by(session_id=session_id)\
            .order_by(TimeEntry.start_time.desc())\
            .all()
