from dataclasses import dataclass, field
from time import sleep
from typing import Any, Dict, List

import boto3
from mypy_boto3_dynamodb.service_resource import Table as DynamoDBTable
from mypy_boto3_dynamodb.type_defs import ScanOutputTypeDef

from dymy.utils import get_logger


logger = get_logger(__name__)


@dataclass
class DynamoDBClient:
    table: DynamoDBTable = field(init=False)

    def __post_init__(self):
        resource = boto3.resource(
            service_name=self.service_name,
            region_name=self.region,
            endpoint_url=self.endpoint,
        )
        self.table = resource.Table(self.table.table_name)

    def scan(self, **kwargs: Any) -> List[Dict[str, Any]]:
        response: ScanOutputTypeDef = self.table.scan(**kwargs)

        items: List[Dict[str, Any]] = []
        if not (raw_items := response['Items']):
            return items

        items.extend(raw_items)

        if (v := response.get('LastEvaluatedKey')):
            # prevent to throttle
            sleep(0.5)

            kwargs.pop('ExclusiveStartKey', None)
            tmp = self.scan(
                ExclusiveStartKey=v, **kwargs)
            items.extend(tmp)

        return items
