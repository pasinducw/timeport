import os
import pytest
from app import app as flask_app
from models import db

@pytest.fixture
def app():
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with flask_app.app_context():
        db.create_all()  # Create tables before tests
        yield flask_app
        db.session.remove()
        db.drop_all()  # Clean up after tests

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session
