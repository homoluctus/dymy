from datetime import datetime
from decimal import Decimal


def decimal2int(target: Decimal) -> int:
    if isinstance(target, Decimal):
        return int(target)
    elif isinstance(target, int):
        return target

    error_msg = 'Expected argument type is Decimal, ' \
        f'but actually {type(target)}'
    raise TypeError(error_msg)


def str2datetime(target: str, fmt: str = '%Y%m%d%H%M%S') -> datetime:
    """Convert string to datetime object

    Args:
        target (str): target to convert
        fmt (str, optional): target format. Defaults to '%Y%m%d%H%M%S'.

    Returns:
        datetime
    """

    return datetime.strptime(target, fmt)
