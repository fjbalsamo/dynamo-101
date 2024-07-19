from datetime import datetime
from typing import Any, Dict, Literal, List, Union
from uuid import uuid4
from modules.table import MyTable


class Product(MyTable):
    PK: str = "PRODUCT"

    def __init__(
        self,
        Data: Dict[
            Literal["name", "kind", "unit_price", "in_promotion"],
            Union[str, float, bool],
        ] = {},
    ) -> None:
        super().__init__()
        self.id = str(uuid4())
        self.name: str = Data.get("name", "")
        self.kind: str = Data.get("kind", "")
        self.unit_price: float = Data.get("unit_price", 0.0)
        self.in_promotion: bool = Data.get("in_promotion", False)

    @classmethod
    def __serialize(cls, Item: Dict[str, Any]):
        SK1: str = Item.get("SK1", "#")
        SK2: str = Item.get("SK2", "#")
        SK3: str = Item.get("SK3", "#")
        return {
            "id": SK1,
            "name": SK2.split("#")[0],
            "kind": SK3.split("#")[0],
            "unit_price": float(Item.get("unit_price")),
            "in_promotion": bool(Item.get("in_promotion")),
            "created_at": Item.get("created_at"),
            "updated_at": Item.get("updated_at"),
        }

    def save(self):
        Item = {
            "PK": self.PK,
            "SK1": self.id,
            "SK2": "#".join([self.name.lower(), self.id]),
            "SK3": "#".join([self.kind.lower(), self.id]),
            "unit_price": self.unit_price,
            "in_promotion": self.in_promotion,
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        }
        self.add_single_table_item(Item=Item)

    def find_products_by(self, by: Literal["name", "kind"], value: str):
        return self.query(
            PK=self.PK,
            SK_NAME="SK2" if by == "name" else "SK3",
            SK_VALUE=value.lower(),
            serialize=Product.__serialize,
        )

    @classmethod
    def seeder(cls):
        seeds = [
            {
                "name": "MacBook Pro",
                "kind": "laptops",
                "unit_price": 1800.00,
                "in_promotion": False,
            },
            {
                "name": "Dell Inspiron",
                "kind": "laptops",
                "unit_price": 300.00,
                "in_promotion": True,
            },
            {
                "name": "Play Station 5",
                "kind": "consoles",
                "unit_price": 1000.00,
                "in_promotion": True,
            },
            {
                "name": "X-Box One",
                "kind": "consoles",
                "unit_price": 1100.00,
                "in_promotion": False,
            },
            {
                "name": "Apple Vision Pro",
                "kind": "accesories",
                "unit_price": 2100.00,
                "in_promotion": False,
            },
            {
                "name": "Apple Studio Display",
                "kind": "screens",
                "unit_price": 5900.00,
                "in_promotion": False,
            },
            {
                "name": "JBL Speaker Boombox 3",
                "kind": "speakears",
                "unit_price": 800.00,
                "in_promotion": False,
            },
            {
                "name": "Silla Gamer Ergonomica NicTom",
                "kind": "accesories",
                "unit_price": 200.00,
                "in_promotion": True,
            },
            {
                "name": "Auricular Logitech G435",
                "kind": "accesories",
                "unit_price": 300.00,
                "in_promotion": True,
            },
        ]
        collector: List[Product] = []
        for Data in seeds:
            product = Product(Data=Data)
            product.save()
            collector.append(product)
        return collector
