from decimal import Decimal
from typing import Any, Callable, Dict, List, Literal, Union
import json
import boto3
import boto3.dynamodb
import boto3.dynamodb.conditions
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table


class MyTable:
    MY_SINGLE_TABLE_NAME: str = "MY_SINGLE_TABLE"
    _CUSTOMER_PK_NAME: str = "CUSTOMER"
    _PRODUCT_PK_NAME: str = "PRODUCT"
    _TICKET_PK_NAME: str = "TICKET"
    _SALE_PK_NAME: str = "SALE_ITEM"

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

    def get_item(self, PK: str, SK1: str):
        item_ref = self.single_table.get_item(Key={"PK": PK, "SK1": SK1})
        if item_ref.get("Item") is None:
            return None
        else:
            return item_ref.get("Item")

    def get_items_when_SK1_begins_with(
        self,
        PK_VALUE: str,
        SK1_VALUE: str,
        serialize: Callable[[Dict[str, Any]], Dict[str, Any]],
    ):
        query_ref = self.single_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key("PK").eq(PK_VALUE)
            & boto3.dynamodb.conditions.Key("SK1").begins_with(SK1_VALUE),
        )

        if query_ref.get("Items") is None:
            return []
        else:
            Items = query_ref.get("Items")
            print("Original Data Base Items:\n", Items, "\n")
            return list(map(lambda Item: serialize(Item), Items))

    def get_items_when_SK2_begins_with(
        self,
        PK_VALUE: str,
        SK2_VALUE: str,
        serialize: Callable[[Dict[str, Any]], Dict[str, Any]],
    ):
        query_ref = self.single_table.query(
            IndexName="SK2_GSI",
            KeyConditionExpression=boto3.dynamodb.conditions.Key("PK").eq(PK_VALUE)
            & boto3.dynamodb.conditions.Key("SK2").begins_with(SK2_VALUE),
        )

        if query_ref.get("Items") is None:
            return []
        else:
            Items = query_ref.get("Items")
            print("Original Data Base Items:\n", Items, "\n")
            return list(map(lambda Item: serialize(Item), Items))

    def get_items_when_SK3_begins_with(
        self,
        PK_VALUE: str,
        SK3_VALUE: str,
        serialize: Callable[[Dict[str, Any]], Dict[str, Any]],
    ):
        query_ref = self.single_table.query(
            IndexName="SK3_GSI",
            KeyConditionExpression=boto3.dynamodb.conditions.Key("PK").eq(PK_VALUE)
            & boto3.dynamodb.conditions.Key("SK3").begins_with(SK3_VALUE),
        )

        if query_ref.get("Items") is None:
            return []
        else:
            Items = query_ref.get("Items")
            print("Original Data Base Items:\n", Items, "\n")
            return list(map(lambda Item: serialize(Item), Items))
