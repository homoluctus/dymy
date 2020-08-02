from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional, Union

from dymy._constant import (
    AWS_ACCESS_KEY_ID, AWS_DEFAULT_REGION, AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN, DYNAMODB_ENDPOINT
)
from dymy.utils import snake2pascal


@dataclass
class Boto3ResourceArgs:
    """Model class for boto3.resource arguments"""

    region_name: Optional[str] = AWS_DEFAULT_REGION
    api_version: Optional[str] = None
    use_ssl: bool = True
    verify: Optional[Union[str, bool]] = None
    endpoint_url: Optional[str] = DYNAMODB_ENDPOINT
    aws_access_key_id: Optional[str] = AWS_ACCESS_KEY_ID
    aws_secret_access_key: Optional[str] = AWS_SECRET_ACCESS_KEY
    aws_session_token: Optional[str] = AWS_SESSION_TOKEN
    service_name: str = field(init=False, default='dynamodb')

    def to_dict(self) -> Dict[str, Any]:
        self_dict = {
            k: v for k, v in asdict(self).items()
            if v is not None
        }
        return self_dict


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
