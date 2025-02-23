from datetime import datetime, timezone


def get_current_time() -> datetime:
    """Get current time in UTC timezone."""
    return datetime.now(timezone.utc)
