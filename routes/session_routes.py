from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from services import SessionService

bp = Blueprint('sessions', __name__)

@bp.route('/')
def index():
    active_session = SessionService.get_active_session()
    if not active_session:
        return redirect(url_for('sessions.sessions'))
    return render_template('index.html', session_id=active_session.id)

@bp.route('/sessions')
def sessions():
    return render_template('sessions.html')

@bp.route('/sessions/new', methods=['POST'])
def new_session():
    name = request.json.get('name')
    try:
        session = SessionService.create_session(name)
        return jsonify(session.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/sessions/<int:session_id>/end', methods=['POST'])
def end_session(session_id):
    try:
        session = SessionService.end_session(session_id)
        return jsonify(session.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/sessions/list')
def list_sessions():
    sessions = SessionService.list_sessions()
    return jsonify([session.to_dict() for session in sessions])

@bp.route('/sessions/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    try:
        SessionService.delete_session(session_id)
        return jsonify({'status': 'success'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/sessions/<int:session_id>/export', methods=['POST'])
def export_session(session_id):
    try:
        filename, content = SessionService.export_session(session_id)
        return jsonify({
            'filename': filename,
            'content': content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/sessions/<int:session_id>/info')
def get_session_info(session_id):
    try:
        session = SessionService.get_session(session_id)
        return jsonify(session.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400
