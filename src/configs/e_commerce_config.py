class ECommerceConfig(object):
    TABLE_NAME = "e_commerce_customer"
    COLUMNS_NAME = [
        "CustomerID",
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "Country",
    ]

    NEW_COLUMNS_NAME = [
        "customer_id",
        "invoice_no",
        "stock_code",
        "description",
        "quantity",
        "invoice_date",
        "unit_price",
        "country",
    ]

    COLUMN_MAPPING = {old: new for old, new in zip(COLUMNS_NAME, NEW_COLUMNS_NAME)}

    PANDAS_SCHEMA = {
        "customer_id": int,
        "amount": float,
        "country": str,
    }

    # column name for clustering
    TRAINING_COLUMNS = ["amount", "country"]
    CATEGORICAL_COLUMNS = ["country"]

    # postgresql variable for create table
    POSTGRES_DEFINE = """
        customer_id INTEGER PRIMARY KEY,
        amount FLOAT,
        country VARCHAR(50),
        k_means_cluster INTEGER,
        gaussian_mixture_cluster INTEGER
    """

    MODEL_CONFIG = {
        "k_means": {
            "n_clusters": 5,
            "random_state": 42,
        },
        "gaussian_mixture": {
            "n_components": 5,
            "random_state": 42,
        },
    }


e_commerce_config = ECommerceConfig()
