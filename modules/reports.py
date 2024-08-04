import json
from modules.table import MyTable
from modules.tickets import Ticket


class Report(MyTable):

    def __init__(self) -> None:
        super().__init__()

    # TODO: make some reports and learn by playing
    def products_sold_on(self, promotion: bool):
        pass
