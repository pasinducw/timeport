"""Routes for managing projects."""

from typing import Dict, Any
from flask import Blueprint, jsonify, request
from services import ProjectService

bp = Blueprint('projects', __name__, url_prefix='/projects')

@bp.route('/', methods=['GET'])
def list_projects():
    """List all projects."""
    projects = ProjectService.list_projects()
    return jsonify([project.to_dict() for project in projects])

@bp.route('/', methods=['POST'])
def create_project():
    """Create a new project."""
    data = request.get_json()
    name = data.get('name', '').strip()
    description = data.get('description', '').strip() or None

    if not name:
        return jsonify({'error': 'Project name is required'}), 400

    try:
        project = ProjectService.create_project(name, description)
        return jsonify(project.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id: int):
    """Get a specific project."""
    try:
        project = ProjectService.get_project(project_id)
        return jsonify(project.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id: int):
    """Update a project."""
    data = request.get_json()
    name = data.get('name', '').strip() or None
    description = data.get('description', '').strip() or None

    try:
        project = ProjectService.update_project(project_id, name, description)
        return jsonify(project.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id: int):
    """Delete a project."""
    try:
        ProjectService.delete_project(project_id)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 404
