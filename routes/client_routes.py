"""Routes for managing clients."""

from typing import Dict, Any
from flask import Blueprint, jsonify, request
from services import ClientService

bp = Blueprint('clients', __name__, url_prefix='/clients')

@bp.route('/', methods=['GET'])
def list_clients():
    """List all clients."""
    clients = ClientService.list_clients()
    return jsonify([client.to_dict() for client in clients])

@bp.route('/', methods=['POST'])
def create_client():
    """Create a new client."""
    data = request.get_json()
    name = data.get('name', '').strip()
    email = data.get('email', '').strip() or None
    notes = data.get('notes', '').strip() or None

    if not name:
        return jsonify({'error': 'Client name is required'}), 400

    try:
        client = ClientService.create_client(name, email, notes)
        return jsonify(client.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:client_id>', methods=['GET'])
def get_client(client_id: int):
    """Get a specific client."""
    try:
        client = ClientService.get_client(client_id)
        return jsonify(client.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/<int:client_id>', methods=['PUT'])
def update_client(client_id: int):
    """Update a client."""
    data = request.get_json()
    name = data.get('name', '').strip() or None
    email = data.get('email', '').strip() or None
    notes = data.get('notes', '').strip() or None

    try:
        client = ClientService.update_client(client_id, name, email, notes)
        return jsonify(client.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/<int:client_id>', methods=['DELETE'])
def delete_client(client_id: int):
    """Delete a client."""
    try:
        ClientService.delete_client(client_id)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 404
