"""Routes for managing time entries."""

from typing import Dict, Any
from flask import Blueprint, jsonify, request
from services import EntryService

bp = Blueprint('entries', __name__)

@bp.route('/log/<int:session_id>', methods=['POST'])
def log_time(session_id: int):
    """Log a new time entry or stop the current one."""
    data = request.get_json()
    description = data.get('description', '').strip()
    
    try:
        if description.lower() == 'stop' or not description:
            entry = EntryService.stop_entry(session_id)
            return jsonify({'status': 'stopped'})
            
        entry = EntryService.create_entry(session_id, description)
        return jsonify(entry.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/stop/<int:session_id>', methods=['POST'])
def stop_time(session_id: int):
    try:
        entry = EntryService.stop_entry(session_id)
        return jsonify(entry.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/entries/<int:entry_id>/notes', methods=['POST'])
def update_entry_notes(entry_id: int):
    notes = request.json.get('notes', '').strip()
    try:
        entry = EntryService.update_notes(entry_id, notes)
        return jsonify(entry.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/entries/<int:entry_id>/tags/<int:tag_id>', methods=['POST'])
def add_tag_to_entry(entry_id: int, tag_id: int):
    """Add a tag to an entry."""
    try:
        entry = EntryService.add_tag_to_entry(entry_id, tag_id)
        return jsonify(entry.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/entries/<int:entry_id>/tags/<int:tag_id>', methods=['DELETE'])
def remove_tag_from_entry(entry_id: int, tag_id: int):
    """Remove a tag from an entry."""
    try:
        entry = EntryService.remove_tag_from_entry(entry_id, tag_id)
        return jsonify(entry.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id: int):
    """Update an entry."""
    data = request.get_json()
    project_id = data.get('project_id')
    client_id = data.get('client_id')
    notes = data.get('notes')

    try:
        entry = EntryService.update_entry(entry_id, project_id=project_id, client_id=client_id)
        if notes is not None:
            entry = EntryService.update_notes(entry_id, notes)
        return jsonify(entry.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id: int):
    try:
        EntryService.delete_entry(entry_id)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/sessions/<int:session_id>/entries', methods=['GET'])
def get_session_entries(session_id: int):
    """Get all entries for a session."""
    entries = EntryService.list_entries(session_id)
    return jsonify([entry.to_dict() for entry in entries])
