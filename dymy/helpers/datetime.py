from datetime import datetime, timedelta


def get_specific_datetime_based_on_now(
        *,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        fmt: str = '%Y%m%d%H%M%S%f') -> str:
    """Get specific datetime based on current time

    Args:
        days (int, optional)
        hours (int, optional)
        minutes (int, optional)
        seconds (int, optional)
        fmt (str, optional): datetime format to convert

    Returns:
        str: formatted datetime
    """

    specific_datetime = datetime.now() + \
        timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return specific_datetime.strftime(fmt)
