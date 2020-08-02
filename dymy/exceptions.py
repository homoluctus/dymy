class DyMyError(Exception):
    """Base class for DyMy exceptions"""


class DynamoDBInvalidOperationError(Exception):
    """Raised when specified invalid DynamoDB operation"""

    msg = '{operation} is invalid DynamoDB operation'

    def __init__(self, operation_name: str) -> None:
        super().__init__(self.msg.format(operation=operation_name))
