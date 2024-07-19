from decimal import Decimal
from typing import Any, Dict, List
import json
import boto3
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table


class MyTable:
    MY_SINGLE_TABLE_NAME: str = "MY_SINGLE_TABLE"

    def __init__(self) -> None:
        client: DynamoDBServiceResource = boto3.resource(
            "dynamodb",
            endpoint_url="http://localhost:8000",  # DynamoDB Local address
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
            region_name="us-west-2",
        )

        self.client: DynamoDBServiceResource = client
        self.single_table: Table = client.Table(self.MY_SINGLE_TABLE_NAME)

    @classmethod
    def create_single_table(cls):
        _self = MyTable()
        _self.client.create_table(
            TableName=_self.MY_SINGLE_TABLE_NAME,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK1", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK1", "AttributeType": "S"},
                {"AttributeName": "SK2", "AttributeType": "S"},
                {"AttributeName": "SK3", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "SK2_GSI",
                    "KeySchema": [
                        {"AttributeName": "PK", "KeyType": "HASH"},
                        {"AttributeName": "SK2", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                },
                {
                    "IndexName": "SK3_GSI",
                    "KeySchema": [
                        {"AttributeName": "PK", "KeyType": "HASH"},
                        {"AttributeName": "SK3", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                },
            ],
        )

    def __sanitize(self, Data: Dict[str, Any]):
        Item = json.loads(json.dumps(Data), parse_float=Decimal)
        return Item

    def add_single_table_item(self, Item: Dict[str, Any]):
        self.single_table.put_item(Item=self.__sanitize(Item))

    def add_single_table_batch(self, Batch: List[Dict[str, Any]]):
        with self.single_table.batch_writer() as batch_writer:
            for Item in Batch:
                batch_writer.put_item(Item=self.__sanitize(Item))
