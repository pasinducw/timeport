from datetime import datetime
import pytest
from models import Session, TimeEntry
from services import EntryService

def test_create_entry(db_session):
    """Test entry creation"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    entry = EntryService.create_entry(session.id, "Test Task")
    assert entry.description == "Test Task"
    assert entry.session_id == session.id
    assert entry.end_time is None

def test_create_entry_ends_active_entry(db_session):
    """Test that creating a new entry ends the active entry"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    active_entry = EntryService.create_entry(session.id, "Active Task")
    assert active_entry.end_time is None

    new_entry = EntryService.create_entry(session.id, "New Task")
    db_session.refresh(active_entry)
    
    assert active_entry.end_time is not None
    assert new_entry.end_time is None

def test_create_entry_in_ended_session_fails(db_session):
    """Test that creating an entry in an ended session raises an error"""
    session = Session(name="Test Session", end_time=datetime.utcnow())
    db_session.add(session)
    db_session.commit()

    with pytest.raises(ValueError, match="Cannot add entries to ended session"):
        EntryService.create_entry(session.id, "Test Task")

def test_stop_entry(db_session):
    """Test stopping an entry"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    entry = EntryService.create_entry(session.id, "Test Task")
    stopped_entry = EntryService.stop_entry(session.id)
    
    assert stopped_entry.id == entry.id
    assert stopped_entry.end_time is not None

def test_stop_entry_in_ended_session_fails(db_session):
    """Test that stopping an entry in an ended session raises an error"""
    session = Session(name="Test Session", end_time=datetime.utcnow())
    db_session.add(session)
    db_session.commit()

    with pytest.raises(ValueError, match="Session has ended"):
        EntryService.stop_entry(session.id)

def test_update_notes(db_session):
    """Test updating entry notes"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    entry = EntryService.create_entry(session.id, "Test Task")
    updated_entry = EntryService.update_notes(entry.id, "Test notes")
    
    assert updated_entry.notes == "Test notes"

def test_delete_entry(db_session):
    """Test entry deletion"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    entry = EntryService.create_entry(session.id, "Test Task")
    EntryService.delete_entry(entry.id)
    
    assert TimeEntry.query.count() == 0

def test_list_entries(db_session):
    """Test listing entries for a session"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    entry1 = EntryService.create_entry(session.id, "Task 1")
    entry2 = EntryService.create_entry(session.id, "Task 2")
    
    entries = EntryService.list_entries(session.id)
    assert len(entries) == 2
    assert entries[0].id == entry2.id  # Most recent first
