from dataclasses import asdict, dataclass, fields
from typing import Any, ClassVar, Dict, Iterable, Tuple

from dymy._constant import DYNAMODB_QUERY_OPERATION, DYNAMODB_SCAN_OPERATION
from dymy.db.dynamodb import DynamoDBClient, DynamoDBItemsType
from dymy.models.dynamodb.arg import (
    Boto3ResourceArgs, DynamoDBArgs, DynamoDBQueryArgs, DynamoDBScanArgs
)


@dataclass
class DynamoDBModel:
    """DynamoDB base model"""

    class Meta:
        # Don't touch this class
        operation: ClassVar[str]

    class Args:
        boto3: ClassVar[Boto3ResourceArgs]
        operation: ClassVar[DynamoDBArgs]

    table_name: ClassVar[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def schema(cls) -> Tuple[str, ...]:
        schema = tuple(f.name for f in fields(cls))
        return schema

    @classmethod
    def format_results(
            cls,
            results: DynamoDBItemsType) -> Iterable['DynamoDBModel']:
        return map(lambda x: cls(**x), results)  # type: ignore

    @classmethod
    def get_client(cls) -> DynamoDBClient:
        return DynamoDBClient(
            table_name=cls.table_name,
            resource_args=cls.Args.boto3)

    @classmethod
    def select(cls) -> Iterable['DynamoDBModel']:
        client = cls.get_client()
        raw_results = client.select(
            cls.Meta.operation, **cls.Args.operation.to_dict())
        results = cls.format_results(raw_results)
        return results


@dataclass
class DynamoDBQueryModel(DynamoDBModel):
    """DynamoDBModel for query operation"""

    class Meta:
        # Don't touch this class
        operation: ClassVar[str] = DYNAMODB_QUERY_OPERATION

    class Args:
        operation: ClassVar[DynamoDBQueryArgs]


@dataclass
class DynamoDBScanModel(DynamoDBModel):
    """DynamoDBModel for scan operation"""

    class Meta:
        # Don't touch this class
        operation: ClassVar[str] = DYNAMODB_SCAN_OPERATION

    class Args:
        operation: ClassVar[DynamoDBScanArgs]
