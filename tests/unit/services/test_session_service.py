import pytest
from datetime import datetime
from models import Session, TimeEntry
from services import SessionService

def test_create_session(db_session):
    """Test session creation"""
    session = SessionService.create_session("Test Session")
    assert session.name == "Test Session"
    assert session.end_time is None

def test_create_session_ends_active_session(db_session):
    """Test that creating a new session ends the active session"""
    active_session = SessionService.create_session("Active Session")
    assert active_session.end_time is None

    new_session = SessionService.create_session("New Session")
    db_session.refresh(active_session)
    
    assert active_session.end_time is not None
    assert new_session.end_time is None

def test_end_session(db_session):
    """Test ending a session"""
    session = SessionService.create_session("Test Session")
    SessionService.end_session(session.id)
    
    db_session.refresh(session)
    assert session.end_time is not None

def test_end_session_with_active_entry(db_session):
    """Test that ending a session also ends active entries"""
    session = SessionService.create_session("Test Session")
    entry = TimeEntry(session_id=session.id, description="Test Task")
    db_session.add(entry)
    db_session.commit()

    SessionService.end_session(session.id)
    db_session.refresh(entry)
    
    assert entry.end_time is not None
    assert session.end_time is not None

def test_delete_session(db_session):
    """Test session deletion"""
    session = SessionService.create_session("Test Session")
    session.end_time = datetime.utcnow()  # End session first
    db_session.commit()

    SessionService.delete_session(session.id)
    assert Session.query.count() == 0

def test_delete_active_session_fails(db_session):
    """Test that deleting an active session raises an error"""
    session = SessionService.create_session("Test Session")
    
    with pytest.raises(ValueError, match="Cannot delete active session"):
        SessionService.delete_session(session.id)

def test_get_session(db_session):
    """Test retrieving a session"""
    session = SessionService.create_session("Test Session")
    retrieved = SessionService.get_session(session.id)
    assert retrieved.id == session.id

def test_get_active_session(db_session):
    """Test retrieving active session"""
    # Create and end first session
    ended_session = SessionService.create_session("Ended Session")
    ended_session.end_time = datetime.utcnow()
    db_session.commit()

    # Create active session last
    active_session = SessionService.create_session("Active Session")
    db_session.commit()

    current = SessionService.get_active_session()
    assert current is not None
    assert current.id == active_session.id

def test_list_sessions(db_session):
    """Test listing all sessions"""
    session1 = SessionService.create_session("Session 1")
    session2 = SessionService.create_session("Session 2")
    
    sessions = SessionService.list_sessions()
    assert len(sessions) == 2
    assert sessions[0].id == session2.id  # Most recent first
