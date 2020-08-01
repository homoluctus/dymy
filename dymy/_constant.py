import sys

from dymy.helpers.env import get_env
from dymy.utils import get_logger


logger = get_logger(__name__)

DYNAMODB_ENDPOINT = get_env('DYNAMODB_ENDPOINT', ignore_error=True)
AWS_DEFAULT_REGION = get_env('AWS_DEFAULT_REGION', ignore_error=True)
AWS_ACCESS_KEY_ID = get_env('AWS_ACCESS_KEY_ID', ignore_error=True)
AWS_SECRET_ACCESS_KEY = get_env('AWS_SECRET_ACCESS_KEY', ignore_error=True)
AWS_SESSION_TOKEN = get_env('AWS_SESSION_TOKEN', ignore_error=True)

try:
    MYSQL_DB = get_env('MYSQL_DB')
    MYSQL_HOST = get_env('MYSQL_HOST')
    MYSQL_PORT = int(get_env('MYSQL_PORT'))  # type: ignore
    MYSQL_USER = get_env('MYSQL_USER')
    MYSQL_PASSWORD = get_env('MYSQL_PASSWORD')
except KeyError:
    logger.error(
        'Please set MYSQL_DB, MYSQL_HOST, MYSQL_PORT, '
        'MYSQL_USER and MYSQL_PASSWORD as environment variable')
    sys.exit(1)
