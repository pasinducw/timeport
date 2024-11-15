from flask import Blueprint, jsonify, request
from services import EntryService

bp = Blueprint('entries', __name__)

@bp.route('/log/<int:session_id>', methods=['POST'])
def log_time(session_id):
    description = request.json.get('description', '').strip()
    try:
        if description.lower() == 'stop' or not description:
            entry = EntryService.stop_entry(session_id)
            return jsonify({'status': 'stopped'})
        entry = EntryService.create_entry(session_id, description)
        return jsonify(entry.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/stop/<int:session_id>', methods=['POST'])
def stop_time(session_id):
    try:
        entry = EntryService.stop_entry(session_id)
        return jsonify(entry.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/entries/<int:entry_id>/notes', methods=['POST'])
def update_entry_notes(entry_id):
    notes = request.json.get('notes', '').strip()
    try:
        entry = EntryService.update_notes(entry_id, notes)
        return jsonify(entry.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    try:
        EntryService.delete_entry(entry_id)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/sessions/<int:session_id>/entries')
def get_session_entries(session_id):
    entries = EntryService.list_entries(session_id)
    return jsonify([entry.to_dict() for entry in entries])
