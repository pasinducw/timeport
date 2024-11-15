"""Application-wide constants."""

# Model Constraints
MAX_SESSION_NAME_LENGTH = 100
MAX_ENTRY_DESCRIPTION_LENGTH = 200

# Time Formats
DEFAULT_SESSION_NAME_FORMAT = "%Y-%m-%d %H:%M"
ISO_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

# Database
DEFAULT_DATABASE_URL = "sqlite:///timetracker.db"

# API Response Messages
ERROR_ACTIVE_SESSION = "Cannot perform operation on active session"
ERROR_ENDED_SESSION = "Cannot create entry in ended session"
ERROR_INVALID_SESSION = "Invalid session ID"
ERROR_INVALID_ENTRY = "Invalid entry ID"
ERROR_MISSING_DESCRIPTION = "Description is required"
