"""Base model configuration."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Base(db.Model):
    """Base model class that other models will inherit from."""
    
    __abstract__ = True  # This ensures SQLAlchemy won't try to create a table for this model
