import json
from datetime import datetime
from typing import Any, Dict, List, Literal, Union
from uuid import uuid4
from modules.table import MyTable
from modules.products import Product
from modules.customers import Customer


class Ticket(MyTable):
    TKT_PK: str = "TICKET"
    SALE_PK: str = "SALE_ITEM"
    sale_items: List[Dict[str, Any]] = []

    def __init__(self, customer: Union[Customer, None] = None) -> None:
        super().__init__()
        if not customer is None:
            self.id: str = str(uuid4())

            self.customer_id: str = customer.id
            self.ticket_name: str = (
                f"{customer.lastname} {customer.name} | CUIT: {customer.cuit}"
            )
            self.date: str = datetime.now().strftime("%Y-%m-%d")
            self.products_qty: int = 0
            self.total_price: float = 0.0

    @classmethod
    def __serialize_sale_item(cls, Item: Dict[str, Any]):
        SK1: str = Item.get("SK1", "#")
        SK2: str = Item.get("SK2", "#")
        SK3: str = Item.get("SK3", "#")
        product_qty = int(Item.get("product_qty"))
        unit_price = float(Item.get("unit_price"))
        return {
            "id": SK1.split("#")[1],
            "ticket_id": SK1.split("#")[0],
            "product_id": SK2.split("#")[0],
            "sold_in_promotion": True if SK3.split("#")[0] == "PROMMO" else False,
            "product_name": Item.get("product_name"),
            "product_qty": product_qty,
            "unit_price": unit_price,
            "sub_total": product_qty * unit_price,
        }

    @classmethod
    def __serialize_ticket(cls, Item: Dict[str, Any]):
        SK1: str = Item.get("SK1", "#")
        SK2: str = Item.get("SK2", "#")
        SK3: str = Item.get("SK3", "#")
        return {
            "id": SK1,
            "customer_id": SK2.split("#")[0],
            "date": SK3.split("#")[0],
            "total_price": float(Item.get("total_price")),
            "ticket_name": str(Item.get("ticket_name")),
            "products_qty": int(Item.get("products_qty")),
            "created_at": Item.get("created_at"),
            "updated_at": Item.get("updated_at"),
        }

    def add_sale_item(self, product: Product, product_qty: int = 1):
        sale_uuid = str(uuid4())
        self.sale_items.append(
            {
                "PK": self.SALE_PK,
                "SK1": "#".join([self.id, sale_uuid]),
                "SK2": "#".join([product.id, sale_uuid]),
                "SK3": "#".join(
                    [
                        "PROMO" if product.in_promotion else "NORMAL",
                        product.id,
                        sale_uuid,
                    ]
                ),
                "product_name": product.name,
                "product_qty": product_qty,
                "unit_price": product.unit_price,
                "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
                "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
            }
        )
        self.products_qty += product_qty
        self.total_price += product_qty * product.unit_price

    def find_ticket_by(self, by: Literal["customer_id", "date"], value: str):
        """
        # Find tickets by
        @params by:str can by "customer_id" or "date"
        @params value:str value to search
        """
        print(f"# find Tickets when {by} begins_with {value}\n")
        response = []
        if by == "customer_id":
            response = self.get_items_when_SK2_begins_with(
                PK_VALUE=self.TKT_PK, SK2_VALUE=value, serialize=self.__serialize_ticket
            )
        elif by == "date":
            response = self.get_items_when_SK3_begins_with(
                PK_VALUE=self.TKT_PK, SK3_VALUE=value, serialize=self.__serialize_ticket
            )
        print(json.dumps(response, indent=2))

    def get_ticket_by_id(self, ticket_id: str):
        Item = self.get_item(PK=self.TKT_PK, SK1=ticket_id)
        if Item is None:
            print(json.dumps({"error": f"ticket_id {ticket_id} not found"}, indent=2))
        else:
            details = self.get_items_when_SK1_begins_with(
                PK_VALUE=self.SALE_PK,
                SK1_VALUE=ticket_id,
                serialize=self.__serialize_sale_item,
            )
            tkt = Ticket.__serialize_ticket(Item=Item)
            print(json.dumps({**tkt, "details": details}, indent=2))

    def save(self):
        tkt_item = {
            "PK": self.TKT_PK,
            "SK1": self.id,
            "SK2": "#".join([self.customer_id, self.id]),
            "SK3": "#".join([self.date, self.id]),
            "total_price": self.total_price,
            "ticket_name": self.ticket_name.lower(),
            "products_qty": self.products_qty,
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        }
        self.add_single_table_item(tkt_item)
        self.add_single_table_batch(self.sale_items)
