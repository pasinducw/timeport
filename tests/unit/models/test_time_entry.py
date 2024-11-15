from datetime import datetime
import pytest
from models import Session, TimeEntry

def test_time_entry_creation(db_session):
    """Test basic time entry creation"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    entry = TimeEntry(
        session_id=session.id,
        description="Test Task"
    )
    db_session.add(entry)
    db_session.commit()

    assert entry.id is not None
    assert entry.description == "Test Task"
    assert isinstance(entry.start_time, datetime)
    assert entry.end_time is None
    assert entry.notes is None

def test_time_entry_to_dict(db_session):
    """Test time entry serialization"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    entry = TimeEntry(
        session_id=session.id,
        description="Test Task",
        notes="Test notes"
    )
    db_session.add(entry)
    db_session.commit()

    entry_dict = entry.to_dict()
    assert entry_dict['id'] == entry.id
    assert entry_dict['session_id'] == session.id
    assert entry_dict['description'] == "Test Task"
    assert entry_dict['start_time'] is not None
    assert entry_dict['end_time'] is None
    assert entry_dict['notes'] == "Test notes"

def test_time_entry_with_end_time(db_session):
    """Test time entry with end time"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    entry = TimeEntry(
        session_id=session.id,
        description="Test Task"
    )
    db_session.add(entry)
    db_session.commit()

    entry.end_time = datetime.utcnow()
    db_session.commit()

    entry_dict = entry.to_dict()
    assert entry_dict['end_time'] is not None

def test_time_entry_session_relationship(db_session):
    """Test relationship between time entry and session"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    entry = TimeEntry(
        session_id=session.id,
        description="Test Task"
    )
    db_session.add(entry)
    db_session.commit()

    assert entry.session == session
    assert entry in session.entries
