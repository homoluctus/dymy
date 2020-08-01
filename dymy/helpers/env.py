import os
from typing import Optional


def get_env(
        name: str,
        *,
        ignore_error: bool = False,
        default: Optional[str] = None) -> Optional[str]:
    try:
        return os.environ[name]
    except KeyError as err:
        if ignore_error is False:
            raise err
        return default
