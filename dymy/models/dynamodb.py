from dataclasses import asdict, dataclass, fields
from typing import Any, ClassVar, Dict, Optional, Tuple

from dymy.utils import snake2pascal


@dataclass
class DynamoDBModel:
    """DynamoDB base model"""

    mode: ClassVar[str]
    table_name: ClassVar[str]

    @property
    def item(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def schema(cls) -> Tuple[str, ...]:
        schema = tuple(f.name for f in fields(cls))
        return schema


@dataclass
class DynamoDBQueryModel(DynamoDBModel):
    """DynamoDBModel for query operation"""

    mode: ClassVar[str] = 'query'


@dataclass
class DynamoDBScanModel(DynamoDBModel):
    """DynamoDBModel for scan operation"""

    mode: ClassVar[str] = 'scan'


@dataclass
class DynamoDBArgs:
    """Base model for DynamoDB API parameter"""

    index_name: Optional[str] = None
    select: Optional[str] = None
    limit: Optional[str] = None
    exclusive_start_key: Optional[Dict[str, Dict[str, Any]]] = None
    return_consumed_capacity: str = 'NONE'
    projection_expression: Optional[str] = None
    filter_expression: Optional[Any] = None
    expression_attribute_names: Optional[Dict[str, str]] = None
    expression_attribute_values: Optional[Dict[str, Dict[str, str]]] = None
    consistent_read: bool = False

    def to_dict(self) -> Dict[str, Any]:
        self_dict = {
            snake2pascal(k): v
            for k, v in asdict(self).items()
            if v is not None
        }
        return self_dict


@dataclass
class DynamoDBQueryArgs(DynamoDBArgs):
    """Model for Table.query() arguments"""

    scan_index_forward: bool = True
    key_condition_expression: Optional[Any] = None


@dataclass
class DynamoDBScanArgs(DynamoDBArgs):
    """Model for Table.scan() arguments"""

    total_segments: Optional[int] = None
    segment: Optional[int] = None
