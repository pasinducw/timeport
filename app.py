from flask import Flask
from models import db
from routes import session_bp, entry_bp

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

# Register blueprints
app.register_blueprint(session_bp)
app.register_blueprint(entry_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)