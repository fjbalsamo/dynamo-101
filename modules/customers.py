import json
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

    @classmethod
    def __serialize(cls, Item: Dict[str, Any]):
        SK1: str = Item.get("SK1", "#")
        SK2: str = Item.get("SK2", "#")
        SK3: str = Item.get("SK3", "#")
        return {
            "id": SK1.split("#")[1],
            "cuit": SK1.split("#")[0],
            "name": SK3.split("#")[0],
            "lastname": SK2.split("#")[0],
            "email": Item.get("email", "@"),
            "phone": Item.get("phone", "N/A"),
            "created_at": Item.get("created_at"),
            "updated_at": Item.get("updated_at"),
        }

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

    def find_customer_by(self, by: Literal["name", "lastname", "cuit"], value: str):
        """
        # Find Customers By
        @params by:str can be "name", "lastname", "cuit"
        @params value:str value to search
        """
        print(f"# find Customers when {by} begins_with {value}\n")
        response: List[Dict[str, Any]] = []
        if by == "cuit":
            response = self.get_items_when_SK1_begins_with(
                PK_VALUE=self.PK,
                SK1_VALUE=value.lower(),
                serialize=Customer.__serialize,
            )
        elif by == "lastname":
            response = self.get_items_when_SK2_begins_with(
                PK_VALUE=self.PK,
                SK2_VALUE=value.lower(),
                serialize=Customer.__serialize,
            )
        elif by == "name":
            response = self.get_items_when_SK3_begins_with(
                PK_VALUE=self.PK,
                SK3_VALUE=value.lower(),
                serialize=Customer.__serialize,
            )
        print(json.dumps(response, indent=2))

    @classmethod
    def seeder(cls):
        seeds = [
            {
                "name": "Lucila",
                "lastname": "E.",
                "cuit": "00-10000000-00",
                "phone": "+5490000000000",
                "email": "lucila.e@email.com",
            },
            {
                "name": "Ricardo",
                "lastname": "R.",
                "cuit": "00-20000000-00",
                "phone": "+5490000000000",
                "email": "ricardo.r@email.com",
            },
            {
                "name": "Alberto",
                "lastname": "H.",
                "cuit": "00-30000000-00",
                "phone": "+5490000000000",
                "email": "alberto.h@email.com",
            },
            {
                "name": "Guillermo",
                "lastname": "L.",
                "cuit": "00-40000000-00",
                "phone": "+5490000000000",
                "email": "guilleromo.l@email.com",
            },
            {
                "name": "Joaquin",
                "lastname": "S.",
                "cuit": "00-50000000-00",
                "phone": "+5490000000000",
                "email": "joaquin.s@email.com",
            },
            {
                "name": "Joaquin",
                "lastname": "M.",
                "cuit": "00-60000000-00",
                "phone": "+5490000000000",
                "email": "joaquin.m@email.com",
            },
            {
                "name": "Juan Cruz",
                "lastname": "B.",
                "cuit": "00-60000000-00",
                "phone": "+5490000000000",
                "email": "juanc.b@email.com",
            },
            {
                "name": "Laura",
                "lastname": "C.",
                "cuit": "00-70000000-00",
                "phone": "+5490000000000",
                "email": "laura.c@email.com",
            },
            {
                "name": "Lucas",
                "lastname": "P.",
                "cuit": "00-80000000-00",
                "phone": "+5490000000000",
                "email": "lucas.p@email.com",
            },
            {
                "name": "Martin",
                "lastname": "M.",
                "cuit": "00-90000000-00",
                "phone": "+5490000000000",
                "email": "martin.m@email.com",
            },
            {
                "name": "Maria Jose",
                "lastname": "N.",
                "cuit": "00-11000000-00",
                "phone": "+5490000000000",
                "email": "mariaj.n@email.com",
            },
            {
                "name": "Ramiro",
                "lastname": "R.",
                "cuit": "00-12000000-00",
                "phone": "+5490000000000",
                "email": "ramiro.r@email.com",
            },
            {
                "name": "Pablo",
                "lastname": "D.",
                "cuit": "00-13000000-00",
                "phone": "+5490000000000",
                "email": "pablo.d@email.com",
            },
            {
                "name": "Franco",
                "lastname": "B.",
                "cuit": "00-14000000-00",
                "phone": "+5490000000000",
                "email": "franco.b@email.com",
            },
        ]
        collector: List[Customer] = []
        for Data in seeds:
            customer = Customer(Data=Data)
            customer.save()
            collector.append(customer)
        return collector
