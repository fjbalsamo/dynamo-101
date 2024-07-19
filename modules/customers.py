from datetime import datetime
from typing import Any, Dict, Literal, List
from uuid import uuid4
from modules.table import MyTable


class Customer(MyTable):
    PK: str = "CUSTOMER"

    def __init__(
        self,
        Data: Dict[Literal["name", "lastname", "cuit", "phone", "email"], str] = {},
    ) -> None:
        super().__init__()
        self.id = str(uuid4())
        self.name = Data.get("name", "")
        self.lastname = Data.get("lastname", "")
        self.cuit = Data.get("cuit", "")
        self.phone = Data.get("phone", "N/A")
        self.email = Data.get("email", "@")

    def save(self):
        Item = {
            "PK": self.PK,
            "SK1": "#".join([self.cuit, self.id]),
            "SK2": "#".join([self.lastname.lower().strip(), self.id]),
            "SK3": "#".join([self.name.lower().strip(), self.id]),
            "email": self.email.lower().strip(),
            "phone": self.phone.lower().strip(),
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        }
        self.add_single_table_item(Item=Item)

    @classmethod
    def seeder(cls):
        seeds = [
            {
                "name": "Lucila",
                "lastname": "E.",
                "cuit": "00-10000000-00",
                "phone": "+5490000000000",
                "email": "@",
            },
            {
                "name": "Ricardo",
                "lastname": "R.",
                "cuit": "00-20000000-00",
                "phone": "+5490000000000",
                "email": "@",
            },
            {
                "name": "Alberto",
                "lastname": "H.",
                "cuit": "00-30000000-00",
                "phone": "+5490000000000",
                "email": "@",
            },
            {
                "name": "Guillermo",
                "lastname": "L.",
                "cuit": "00-40000000-00",
                "phone": "+5490000000000",
                "email": "@",
            },
            {
                "name": "Joaquin",
                "lastname": "S.",
                "cuit": "00-50000000-00",
                "phone": "+5490000000000",
                "email": "@",
            },
            {
                "name": "Joaquin",
                "lastname": "M.",
                "cuit": "00-60000000-00",
                "phone": "+5490000000000",
                "email": "@",
            },
            {
                "name": "Juan Cruz",
                "lastname": "B.",
                "cuit": "00-60000000-00",
                "phone": "+5490000000000",
                "email": "@",
            },
            {
                "name": "Laura",
                "lastname": "L.",
                "cuit": "00-70000000-00",
                "phone": "+5490000000000",
                "email": "@",
            },
            {
                "name": "Lucas",
                "lastname": "P.",
                "cuit": "00-80000000-00",
                "phone": "+5490000000000",
                "email": "@",
            },
            {
                "name": "Martin",
                "lastname": "M.",
                "cuit": "00-90000000-00",
                "phone": "+5490000000000",
                "email": "@",
            },
            {
                "name": "Maria Jose",
                "lastname": "N.",
                "cuit": "00-11000000-00",
                "phone": "+5490000000000",
                "email": "@",
            },
            {
                "name": "Ramiro",
                "lastname": "R.",
                "cuit": "00-12000000-00",
                "phone": "+5490000000000",
                "email": "@",
            },
            {
                "name": "Pablo",
                "lastname": "D.",
                "cuit": "00-13000000-00",
                "phone": "+5490000000000",
                "email": "@",
            },
        ]
        collector: List[Customer] = []
        for Data in seeds:
            customer = Customer(Data=Data)
            customer.save()
            collector.append(customer)
        return collector
