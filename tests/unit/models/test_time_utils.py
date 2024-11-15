from datetime import datetime
import pytz
from models.time_utils import get_utc_now, format_to_iso8601

def test_get_utc_now():
    """Test that get_utc_now returns UTC time"""
    now = get_utc_now()
    assert isinstance(now, datetime)
    assert now.tzinfo is None  # Should be naive UTC time

def test_format_to_iso8601_with_naive_datetime():
    """Test ISO 8601 formatting with naive datetime"""
    dt = datetime(2024, 1, 1, 12, 0, 0)
    formatted = format_to_iso8601(dt)
    assert formatted.endswith('+00:00')
    assert formatted.startswith('2024-01-01T12:00:00')

def test_format_to_iso8601_with_aware_datetime():
    """Test ISO 8601 formatting with timezone-aware datetime"""
    dt = datetime(2024, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
    formatted = format_to_iso8601(dt)
    assert formatted.endswith('+00:00')
    assert formatted.startswith('2024-01-01T12:00:00')

def test_format_to_iso8601_with_none():
    """Test ISO 8601 formatting with None input"""
    assert format_to_iso8601(None) is None
