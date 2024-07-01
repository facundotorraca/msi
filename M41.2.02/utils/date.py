def n_days_ago(n):
    """
    Returns the date n days ago from today.
    """
    from datetime import datetime, timedelta

    return (datetime.now() - timedelta(days=n)).strftime("%Y-%m-%d")


def n_days_from_now(n):
    """
    Returns the date n days from today.
    """
    from datetime import datetime, timedelta

    return (datetime.now() + timedelta(days=n)).strftime("%Y-%m-%d")
