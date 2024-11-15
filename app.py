import os
import logging
from flask import Flask, jsonify
from models import db
from routes import session_bp, entry_bp
from config import config
from utils.logging_config import setup_logging
from exceptions import TimeTrackerError, ValidationError

def create_app(config_name=None):
    """Create and configure the Flask application.
    
    Args:
        config_name: Configuration to use (development, production, testing).
                    Defaults to value of FLASK_ENV environment variable.
    
    Returns:
        Configured Flask application instance.
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    # Configure logging
    setup_logging(log_level=os.getenv('LOG_LEVEL', 'INFO'))
    logger = logging.getLogger(__name__)
    logger.info(f"Creating app with configuration: {config_name}")

    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(session_bp)
    app.register_blueprint(entry_bp)

    # Register error handlers
    @app.errorhandler(TimeTrackerError)
    def handle_timetracker_error(error):
        """Handle custom application errors."""
        response = {
            'error': error.__class__.__name__,
            'message': str(error)
        }
        return jsonify(response), 400

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle validation errors."""
        response = {
            'error': 'ValidationError',
            'message': str(error)
        }
        return jsonify(response), 422

    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 errors."""
        response = {
            'error': 'NotFound',
            'message': 'The requested resource was not found'
        }
        return jsonify(response), 404

    @app.errorhandler(500)
    def handle_server_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {error}", exc_info=True)
        response = {
            'error': 'InternalServerError',
            'message': 'An internal server error occurred'
        }
        return jsonify(response), 500

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )