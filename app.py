import os
from flask import Flask
from models import db
from routes import session_bp, entry_bp
from config import config

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(session_bp)
    app.register_blueprint(entry_bp)

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