from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

import pymysql
from pymysql.connections import Connection as PyMySQLConnection

from dymy._constant import (
    MYSQL_DB, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER
)
from dymy.utils import get_logger


logger = get_logger(__name__)


def connect() -> PyMySQLConnection:
    """Connect to MySQL

    Returns:
        PyMySQLConnection
    """

    try:
        conn = pymysql.connect(
            db=MYSQL_DB,
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=120,
            write_timeout=120,
            local_infile=True
        )
    except Exception as err:
        logger.error('Failed to connect to MySQL')
        raise err
    else:
        logger.info('Connected to MySQL')
        return conn


@dataclass
class Connection:
    conn: Optional[PyMySQLConnection] = None

    def __enter__(self) -> 'Connection':
        self.get_connection()
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def close(self) -> None:
        if self.conn:
            self.conn.close()

    def get_connection(self) -> PyMySQLConnection:
        if self.conn is None:
            self.conn = connect()

        return self.conn

    def rollback(self) -> None:
        if self.conn:
            self.conn.rollback()

    def commit(self) -> None:
        if self.conn:
            self.conn.commit()

    def insert(
            self,
            sql: str,
            params: Optional[Union[Dict[str, Any], List[Any]]] = None,
            *,
            rollback: bool = True) -> int:
        rowcount = 0
        conn = self.get_connection()

        with conn.cursor() as cursor:
            try:
                rowcount = cursor.execute(sql, params)
            except Exception as err:
                if rollback is True:
                    self.rollback()
                raise err

        return rowcount
