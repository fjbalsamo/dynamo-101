import json
from typing import List
from modules.products import Product
from modules.customers import Customer
from modules.tickets import Ticket
from modules.table import MyTable


def create_single_table():
    try:
        print("Creating My Single Table")
        MyTable.create_single_table()
        print("My Single Table Created")
    except Exception as e:
        print(e)


def products_seeder() -> List[Product]:
    try:
        print("Products Seeder")
        return Product.seeder()
    except Exception as e:
        print(e)
        return []


def customer_seeder() -> List[Customer]:
    try:
        print("Customer Seeder")
        return Customer.seeder()
    except Exception as e:
        print(e)
        return []


def tickets_seeder(
    products_list: List[Product], customers_list: List[Customer]
) -> List[Ticket]:
    try:
        ticket_collector: List[Ticket] = []
        print("Tickets seeder")
        for customer in customers_list:
            ticket = Ticket(customer=customer)
            for product in products_list:
                ticket.add_sale_item(product=product, product_qty=2)
            ticket.save()
            ticket_collector.append(ticket)
        return ticket_collector
    except Exception as e:
        print(e)
        return []


# Step 1/2: Create the Table
# create_single_table()

# Step 2/2: Run seedrs to populate the table
# products_list = products_seeder()
# customers_list = customer_seeder()
# ticket_list = tickets_seeder(products_list=products_list, customers_list=customers_list)
# print(
#     {
#         "products": len(products_list),
#         "customers": len(customers_list),
#         "tickets": len(ticket_list),
#     }
# )

# Customer().find_customer_by(by="name", value="m")
Ticket().find_ticket_by(by="date", value="2024")