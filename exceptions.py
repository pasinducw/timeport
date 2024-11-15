"""Custom exceptions for the time tracker application."""

class TimeTrackerError(Exception):
    """Base exception for all time tracker errors."""
    pass

class SessionError(TimeTrackerError):
    """Base exception for session-related errors."""
    pass

class ActiveSessionError(SessionError):
    """Raised when attempting invalid operations on active sessions."""
    pass

class EndedSessionError(SessionError):
    """Raised when attempting invalid operations on ended sessions."""
    pass

class EntryError(TimeTrackerError):
    """Base exception for time entry-related errors."""
    pass

class ValidationError(TimeTrackerError):
    """Raised when input validation fails."""
    pass
