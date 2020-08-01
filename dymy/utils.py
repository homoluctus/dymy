import logging


def get_logger(name: str = __name__, level: str = 'info') -> logging.Logger:
    logger = logging.getLogger(name)
    normalized_level = level.upper()
    logger.setLevel(normalized_level)

    return logger


def snake2pascal(target: str) -> str:
    """Convert snake case to pascal case

    Args:
        target (str)

    Returns:
        str
    """

    return ''.join(map(lambda x: x.title(), target.split('_')))
