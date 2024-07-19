from datetime import datetime
from typing import Any, Dict, List, Literal, Union
from uuid import uuid4
from modules.table import MyTable
from modules.products import Product
from modules.customers import Customer


class Ticket(MyTable):
    TKT_PK = "TICKET"
    SALE_PK = "SALE_ITEM"
    sale_items: List[Dict[str, Any]] = []

    def __init__(self, customer: Customer) -> None:
        super().__init__()
        self.id: str = str(uuid4())
        self.customer_id: str = (customer.id,)
        self.ticket_name: str = (
            f"{customer.lastname} {customer.name} | CUIT: {customer.cuit}"
        )
        self.date: str = datetime.now().strftime("%Y-%m-%d")
        self.products_qty: int = 0
        self.total_price: float = 0.0

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
