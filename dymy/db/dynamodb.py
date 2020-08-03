from dataclasses import InitVar, dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union

import boto3
from mypy_boto3_dynamodb.service_resource import Table as DynamoDBTable
from mypy_boto3_dynamodb.type_defs import QueryOutputTypeDef, ScanOutputTypeDef

from dymy.exceptions import DynamoDBInvalidOperationError
from dymy.models.dynamodb.arg import Boto3ResourceArgs
from dymy.utils import get_logger


logger = get_logger(__name__)

DynamoDBItemsType = List[Dict[str, Any]]
DynamoDBSelectOutputType = Union[QueryOutputTypeDef, ScanOutputTypeDef]
DynamoDBSelectOperationType = Callable[..., DynamoDBSelectOutputType]


@dataclass
class DynamoDBClient:
    table_name: InitVar[str]
    resource_args: InitVar[Boto3ResourceArgs]

    _table: DynamoDBTable = field(init=False)
    _operation: Optional[DynamoDBSelectOperationType] = field(
        init=False, default=None)

    def __post_init__(
            self,
            table_name: str,
            resource_args: Boto3ResourceArgs) -> None:
        resource = boto3.resource(**resource_args.to_dict())
        self._table = resource.Table(table_name)

    def _get_opeation(self, operation_name: str) -> DynamoDBSelectOperationType:
        if self._operation is None:
            if operation_name in ['query', 'scan']:
                raise DynamoDBInvalidOperationError(operation_name)
            self._operation = getattr(self._table, operation_name)
        return self._operation

    def select(self, operation_name: str, **kwargs: Any) -> DynamoDBItemsType:
        operation = self._get_opeation(operation_name)
        response: DynamoDBSelectOutputType = operation(**kwargs)

        if not (items := response['Items']):
            return []

        if (last_key := response.get('LastEvaluatedKey')):
            kwargs['ExclusiveStartKey'] = last_key
            tmp = self.select(operation_name, **kwargs)
            items.extend(tmp)

        return items
