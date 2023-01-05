class MallConfig(object):
    TABLE_NAME = "mall_customer"
    PANDAS_SCHEMA = {
        "CustomerID": int,
        "Gender": str,
        "Age": int,
        "Annual Income (k$)": int,
        "Spending Score (1-100)": int,
    }

    # column name for insert to postgresql
    COLUMNs_NAME = [
        "customer_id",
        "gender",
        "age",
        "annual_income",
        "spending_score",
    ]

    # postgresql variable for create table
    POSTGRES_DEFINE = """
        customer_id INTEGER PRIMARY KEY,
        gender VARCHAR(50),
        Age INTEGER,
        annual_income INTEGER,
        spending_score INTEGER
    """


mall_config = MallConfig()
