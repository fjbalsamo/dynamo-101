import json
from modules.table import MyTable
from modules.tickets import Ticket


class Report(MyTable):

    def __init__(self) -> None:
        super().__init__()

    # TODO: make some reports and learn by playing
    def products_sold_on(self, promotion: bool):
        query_list = self.query(
            PK=self._SALE_PK_NAME,
            SK_NAME="SK3",
            SK_VALUE="PROMO" if promotion else "NORMAL",
            serialize=Ticket.__serialize_sale_item,
        )
        print(json.dumps(query_list, indent=2))
