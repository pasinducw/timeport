from datetime import datetime
import pytz

def get_utc_now():
    """Get current time in UTC"""
    return datetime.utcnow()

def format_to_iso8601(dt):
    """Format datetime to ISO 8601 format"""
    if not dt:
        return None
    if not dt.tzinfo:
        dt = pytz.UTC.localize(dt)
    return dt.isoformat()
