import logging
from csv import DictWriter
from typing import Any, Dict, List, Union


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


ContentForCSVType = Dict[str, Any]
ContentsForCSVType = Union[ContentForCSVType, List[ContentForCSVType]]


def output_dict2csv(fd: Any, contents: ContentsForCSVType) -> None:
    if isinstance(contents, dict):
        contents = [contents]
    keys = contents[0].keys()
    writer = DictWriter(fd, fieldnames=list(keys))
    writer.writerows(contents)
