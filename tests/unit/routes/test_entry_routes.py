import json
import pytest
from models import Session, TimeEntry

def test_log_time(client, db_session):
    """Test time logging endpoint"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    response = client.post(f'/log/{session.id}',
                         json={'description': 'Test Task'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['description'] == 'Test Task'

def test_log_time_ends_active_entry(client, db_session):
    """Test that logging time ends active entry"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    # Create first entry
    response1 = client.post(f'/log/{session.id}',
                          json={'description': 'Task 1'})
    data1 = json.loads(response1.data)
    
    # Create second entry
    response2 = client.post(f'/log/{session.id}',
                          json={'description': 'Task 2'})
    
    # Check first entry was ended
    entry1 = TimeEntry.query.get(data1['id'])
    assert entry1.end_time is not None

def test_stop_time(client, db_session):
    """Test time stopping endpoint"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    # Create an entry
    entry = TimeEntry(session_id=session.id, description="Test Task")
    db_session.add(entry)
    db_session.commit()

    response = client.post(f'/stop/{session.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['end_time'] is not None

def test_update_notes(client, db_session):
    """Test notes update endpoint"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()  # Commit to get session.id

    entry = TimeEntry(
        session_id=session.id,
        description="Test Task"
    )
    db_session.add(entry)
    db_session.commit()

    response = client.post(f'/entries/{entry.id}/notes',
                         json={'notes': 'Test notes'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['notes'] == 'Test notes'

def test_delete_entry(client, db_session):
    """Test entry deletion endpoint"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()  # Commit to get session.id

    entry = TimeEntry(
        session_id=session.id,
        description="Test Task"
    )
    db_session.add(entry)
    db_session.commit()

    response = client.delete(f'/entries/{entry.id}')
    assert response.status_code == 200
    assert TimeEntry.query.count() == 0

def test_list_entries(client, db_session):
    """Test entries listing endpoint"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()  # Commit to get session.id

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

    response = client.get(f'/sessions/{session.id}/entries')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
