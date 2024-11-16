"""Routes package for time tracker application."""

from .session_routes import bp as session_bp
from .entry_routes import bp as entry_bp
from .project_routes import bp as project_bp
from .client_routes import bp as client_bp
from .tag_routes import bp as tag_bp

__all__ = ['session_bp', 'entry_bp', 'project_bp', 'client_bp', 'tag_bp']
