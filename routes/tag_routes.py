"""Routes for managing tags."""

from typing import Dict, Any
from flask import Blueprint, jsonify, request
from services import TagService

bp = Blueprint('tags', __name__, url_prefix='/tags')

@bp.route('/', methods=['GET'])
def list_tags():
    """List all tags."""
    tags = TagService.list_tags()
    return jsonify([tag.to_dict() for tag in tags])

@bp.route('/', methods=['POST'])
def create_tag():
    """Create a new tag."""
    data = request.get_json()
    name = data.get('name', '').strip()
    color = data.get('color', '').strip() or None

    if not name:
        return jsonify({'error': 'Tag name is required'}), 400

    try:
        tag = TagService.create_tag(name, color)
        return jsonify(tag.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:tag_id>', methods=['GET'])
def get_tag(tag_id: int):
    """Get a specific tag."""
    try:
        tag = TagService.get_tag(tag_id)
        return jsonify(tag.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id: int):
    """Update a tag."""
    data = request.get_json()
    name = data.get('name', '').strip() or None
    color = data.get('color', '').strip() or None

    try:
        tag = TagService.update_tag(tag_id, name, color)
        return jsonify(tag.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id: int):
    """Delete a tag."""
    try:
        TagService.delete_tag(tag_id)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/entries/<int:entry_id>/tags/<int:tag_id>', methods=['POST'])
def add_tag_to_entry(entry_id: int, tag_id: int):
    """Add a tag to an entry."""
    try:
        entry = TagService.add_tag_to_entry(entry_id, tag_id)
        return jsonify(entry.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/entries/<int:entry_id>/tags/<int:tag_id>', methods=['DELETE'])
def remove_tag_from_entry(entry_id: int, tag_id: int):
    """Remove a tag from an entry."""
    try:
        entry = TagService.remove_tag_from_entry(entry_id, tag_id)
        return jsonify(entry.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404
