from datetime import datetime
import json
import pytest
from models import Session

def test_index_redirect_without_active_session(client):
    """Test index redirects to sessions page when no active session"""
    response = client.get('/')
    assert response.status_code == 302
    assert '/sessions' in response.location

def test_index_with_active_session(client, db_session):
    """Test index with active session"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    response = client.get('/')
    assert response.status_code == 200

def test_create_session(client):
    """Test session creation endpoint"""
    response = client.post('/sessions/new', 
                         json={'name': 'Test Session'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Test Session'

def test_end_session(client, db_session):
    """Test session ending endpoint"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    response = client.post(f'/sessions/{session.id}/end')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['end_time'] is not None

def test_list_sessions(client, db_session):
    """Test sessions listing endpoint"""
    session1 = Session(name="Session 1")
    session2 = Session(name="Session 2")
    db_session.add_all([session1, session2])
    db_session.commit()

    response = client.get('/sessions/list')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2

def test_delete_session(client, db_session):
    """Test session deletion endpoint"""
    session = Session(name="Test Session", end_time=datetime.utcnow())
    db_session.add(session)
    db_session.commit()

    response = client.delete(f'/sessions/{session.id}')
    assert response.status_code == 200
    assert Session.query.count() == 0

def test_delete_active_session_fails(client, db_session):
    """Test that deleting active session fails"""
    session = Session(name="Test Session")
    db_session.add(session)
    db_session.commit()

    response = client.delete(f'/sessions/{session.id}')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Cannot delete active session" in data['error']
