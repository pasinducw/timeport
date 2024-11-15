from models import db, Session, TimeEntry, time_utils

class EntryService:
    @staticmethod
    def create_entry(session_id, description):
        """Create a new time entry and end any active entry"""
        session = Session.query.get_or_404(session_id)
        
        if session.end_time:
            raise ValueError('Cannot add entries to ended session')
            
        if not description:
            raise ValueError('Description is required')
        
        # End previous active entry
        active_entry = TimeEntry.query.filter_by(
            session_id=session_id,
            end_time=None
        ).first()
        
        if active_entry:
            active_entry.end_time = time_utils.get_utc_now()
            db.session.commit()

        # Create new entry
        entry = TimeEntry(
            session_id=session_id,
            description=description,
            start_time=time_utils.get_utc_now()
        )
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def stop_entry(session_id):
        """Stop the active entry in a session"""
        session = Session.query.get_or_404(session_id)
        
        if session.end_time:
            raise ValueError('Session has ended')
            
        active_entry = TimeEntry.query.filter_by(
            session_id=session_id,
            end_time=None
        ).first()
        
        if not active_entry:
            raise ValueError('No active time entry')
            
        active_entry.end_time = time_utils.get_utc_now()
        db.session.commit()
        return active_entry

    @staticmethod
    def update_notes(entry_id, notes):
        """Update notes for a time entry"""
        entry = TimeEntry.query.get_or_404(entry_id)
        entry.notes = notes.strip() if notes else None
        db.session.commit()
        return entry

    @staticmethod
    def delete_entry(entry_id):
        """Delete a time entry"""
        entry = TimeEntry.query.get_or_404(entry_id)
        db.session.delete(entry)
        db.session.commit()

    @staticmethod
    def list_entries(session_id):
        """List all entries for a session"""
        return TimeEntry.query.filter_by(session_id=session_id).order_by(TimeEntry.start_time.desc()).all()
