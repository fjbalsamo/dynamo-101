# Dynamo 101

Introduction to the concept STD (Single Table Design) It is an advanced strategy for modeling data in DynamoDB that involves storing multiple types of entities in a single table instead of using a separate table for each type of entity. This approach may seem unintuitive at first, especially if you come from a relational database background, but it can offer several significant benefits in terms of performance and scalability.

## Installations

This Demo uses `Python=3.11` and a virtual environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

First of all, download and install **NoSQL Workbench for DynamoDB**. Then activate `DDB local` option.

> Check this [link](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html)

## Run

Step 1: Comment all step 2 and run `python ./app.py`

```python
# ./app.py
. . .
. . .
# Step 1/2: Create the Table using once:
create_single_table()

# Step 2/2: Run seedrs to populate the table
# products_list = products_seeder()
# customers_list = customer_seeder()
# tickets_seeder(products_list=products_list, customers_list=customers_list)
```

Step 2: Comment all step 1 and run `python ./app.py`

```python
# ./app.py
. . .
. . .
# Step 1/2: Create the Table using once:
# create_single_table()

# Step 2/2: Run seedrs to populate the table
products_list = products_seeder()
customers_list = customer_seeder()
tickets_seeder(products_list=products_list, customers_list=customers_list)
```

## Go Ahead! Take a look at your data 🥰
Go back to the NoSQL application.