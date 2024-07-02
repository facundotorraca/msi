from datetime import datetime, timedelta


def n_days_ago(n: int) -> datetime:
    """
    Returns the date n days ago from today.
    """
    return datetime.now() - timedelta(days=n)


def n_days_from_now(n: int) -> datetime:
    """
    Returns the date n days from today.
    """
    return datetime.now() + timedelta(days=n)
