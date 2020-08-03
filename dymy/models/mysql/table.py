from dataclasses import dataclass
from tempfile import NamedTemporaryFile
from typing import Any, ClassVar, Dict, List, Tuple, Union

from dymy.db.mysql import Connection
from dymy.db.sql import INSERT_DYNAMODB_RECORD_TO_MYSQL
from dymy.utils import output_dict2csv


MySQLRecordType = Dict[str, Any]
MySQLRecordsType = Union[List[MySQLRecordType], MySQLRecordType]


@dataclass
class MySQLTable:
    table_name: ClassVar[str]
    raw_sql: ClassVar[str] = INSERT_DYNAMODB_RECORD_TO_MYSQL

    @classmethod
    def migrate(cls, schema: Tuple[str, ...], records: MySQLRecordsType) -> int:
        """Migrate data from DynamoDB to MySQL

        Args:
            schema (Tuple[str, ...])
            records (MySQLRecordsType)

        Returns:
            int: Affected row count
        """

        with NamedTemporaryFile(mode='w+t', encoding='utf-8') as fd:
            output_dict2csv(fd, records)
            sql = cls.synthesize_sql(fd.name, schema)
            rowcount = cls.load(sql)
        return rowcount

    @staticmethod
    def load(sql: str) -> int:
        with Connection() as conn:
            rowcount = conn.insert(sql)
            conn.commit()
        return rowcount

    @classmethod
    def synthesize_sql(cls, filename: str, schema: Tuple[str, ...]) -> str:
        columns_clause = ', '.join(schema)
        return cls.raw_sql.format(
            filepath=filename,
            table=cls.table_name,
            columns=columns_clause)
