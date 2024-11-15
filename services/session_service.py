from datetime import datetime
from models import db, Session, TimeEntry, time_utils

class SessionService:
    @staticmethod
    def create_session(name=None):
        """Create a new session and end any active sessions"""
        # End any active session
        active_session = Session.query.filter_by(end_time=None).first()
        if active_session:
            active_session.end_time = time_utils.get_utc_now()
            db.session.commit()
        
        # Create new session
        if not name:
            name = f'Session {datetime.now().strftime("%Y-%m-%d %H:%M")}'
        
        new_session = Session(name=name, start_time=time_utils.get_utc_now())
        db.session.add(new_session)
        db.session.commit()
        return new_session

    @staticmethod
    def end_session(session_id):
        """End a session and its active entry"""
        session = Session.query.get_or_404(session_id)
        if not session.end_time:
            # End active task if any
            active_entry = TimeEntry.query.filter_by(
                session_id=session_id,
                end_time=None
            ).first()
            if active_entry:
                active_entry.end_time = time_utils.get_utc_now()
            
            session.end_time = time_utils.get_utc_now()
            db.session.commit()
        return session

    @staticmethod
    def delete_session(session_id):
        """Delete a session and all its entries"""
        session = Session.query.get_or_404(session_id)
        
        # Don't allow deleting active sessions
        if not session.end_time:
            raise ValueError('Cannot delete active session')
        
        # Delete all time entries first
        TimeEntry.query.filter_by(session_id=session_id).delete()
        
        # Delete the session
        db.session.delete(session)
        db.session.commit()

    @staticmethod
    def get_session(session_id):
        """Get a session by ID"""
        return Session.query.get_or_404(session_id)

    @staticmethod
    def get_active_session():
        """Get the currently active session"""
        return Session.query.filter(Session.end_time == None).first()

    @staticmethod
    def list_sessions():
        """List all sessions ordered by start time"""
        return Session.query.order_by(Session.start_time.desc()).all()

    @staticmethod
    def export_session(session_id):
        """Export session data to CSV format"""
        session = Session.query.get_or_404(session_id)
        entries = TimeEntry.query.filter_by(session_id=session_id).order_by(TimeEntry.start_time).all()
        
        # Prepare CSV data
        csv_data = [['Description', 'Start Time', 'End Time', 'Duration', 'Notes']]
        for entry in entries:
            duration = ''
            if entry.end_time:
                duration = str(entry.end_time - entry.start_time)
            
            csv_data.append([
                entry.description,
                entry.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                entry.end_time.strftime('%Y-%m-%d %H:%M:%S') if entry.end_time else '',
                duration,
                entry.notes or ''
            ])
        
        # Convert to CSV string
        csv_content = '\n'.join([','.join(['"{}"'.format(cell) for cell in row]) for row in csv_data])
        filename = f'timetracker_export_{session.name}_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.csv'
        
        return filename, csv_content
