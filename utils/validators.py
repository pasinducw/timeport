"""Validation utilities for the time tracker application."""

from typing import TypeVar, Callable, Any
from functools import wraps
from exceptions import ValidationError

T = TypeVar('T')

def validate_input(validator: Callable[..., bool], error_message: str):
    """Decorator for validating function inputs.
    
    Args:
        validator: Function that takes the same arguments as the decorated function
                 and returns True if validation passes, False otherwise.
        error_message: Message to include in the ValidationError if validation fails.
    
    Returns:
        Decorator function that validates inputs before calling the decorated function.
    
    Raises:
        ValidationError: If validation fails.
    """
    def decorator(f: Callable[..., T]) -> Callable[..., T]:
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not validator(*args, **kwargs):
                raise ValidationError(error_message)
            return f(*args, **kwargs)
        return wrapper
    return decorator

def validate_string_length(value: str, max_length: int) -> bool:
    """Validate string length is within limit and not empty.
    
    Args:
        value: String to validate.
        max_length: Maximum allowed length.
    
    Returns:
        bool: True if validation passes, False otherwise.
    """
    return bool(value and len(value.strip()) <= max_length)

def validate_session_name(name: str) -> bool:
    """Validate session name length.
    
    Args:
        name: Session name to validate.
    
    Returns:
        bool: True if validation passes, False otherwise.
    """
    from constants import MAX_SESSION_NAME_LENGTH
    return validate_string_length(name, MAX_SESSION_NAME_LENGTH)

def validate_entry_description(description: str) -> bool:
    """Validate entry description length.
    
    Args:
        description: Entry description to validate.
    
    Returns:
        bool: True if validation passes, False otherwise.
    """
    from constants import MAX_ENTRY_DESCRIPTION_LENGTH
    return validate_string_length(description, MAX_ENTRY_DESCRIPTION_LENGTH)
