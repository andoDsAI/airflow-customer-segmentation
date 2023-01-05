import datetime


class ECommerceConfig(object):
    TABLE_NAME = "e_commerce_customer"
    PANDAS_SCHEMA = {
        "CustomerID": int,
        "InvoiceNo": int,
        "StockCode": str,
        "Description": str,
        "Quantity": int,
        "InvoiceDate": datetime.datetime,
        "UnitPrice": float,
        "Country": str,
    }

    # column name for insert to postgresql
    COLUMNs_NAME = [
        "customer_id",
        "invoice_no",
        "stock_code",
        "description",
        "quantity",
        "invoice_date",
        "unit_price",
        "country",
    ]

    # postgresql variable for create table
    POSTGRES_DEFINE = """
        customer_id INTEGER PRIMARY KEY,
        invoice_no INTEGER,
        stock_code VARCHAR(50),
        description VARCHAR(50),
        quantity INTEGER,
        invoice_date TIMESTAMP,
        unit_price FLOAT,
        country VARCHAR(50)
    """


e_commerce_config = ECommerceConfig()
