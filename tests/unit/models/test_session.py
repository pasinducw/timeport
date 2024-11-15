from datetime import datetime
import pytest
from models import Session, TimeEntry

def test_session_creation(db_session):
    """Test basic session creation"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    assert session.id is not None
    assert session.name == "Test Session"
    assert isinstance(session.start_time, datetime)
    assert session.end_time is None

def test_session_to_dict(db_session):
    """Test session serialization"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    session_dict = session.to_dict()
    assert session_dict['id'] == session.id
    assert session_dict['name'] == "Test Session"
    assert session_dict['start_time'] is not None
    assert session_dict['end_time'] is None
    assert session_dict['entry_count'] == 0

def test_session_with_entries(db_session):
    """Test session with time entries"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    entry1 = TimeEntry(
        session_id=session.id,
        description="Task 1"
    )
    entry2 = TimeEntry(
        session_id=session.id,
        description="Task 2"
    )
    db_session.add_all([entry1, entry2])
    db_session.commit()

    session_dict = session.to_dict()
    assert session_dict['entry_count'] == 2

def test_session_cascade_delete(db_session):
    """Test that deleting a session deletes its entries"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    entry = TimeEntry(
        session_id=session.id,
        description="Task 1"
    )
    db_session.add(entry)
    db_session.commit()

    db_session.delete(session)
    db_session.commit()

    assert TimeEntry.query.count() == 0
