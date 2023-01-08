class MallConfig(object):
    TABLE_NAME = "mall_customer"
    COLUMNS_NAME = [
        "CustomerID",
        "Gender",
        "Age",
        "Annual Income (k$)",
        "Spending Score (1-100)",
    ]

    NEW_COLUMNS_NAME = ["customer_id", "gender", "age", "annual_income", "spending_score"]

    COLUMN_MAPPING = {old: new for old, new in zip(COLUMNS_NAME, NEW_COLUMNS_NAME)}

    PANDAS_SCHEMA = {
        "customer_id": int,
        "gender": str,
        "age": int,
        "annual_income": int,
        "spending_score": int,
    }

    # column name for clustering
    TRAINING_COLUMNS = ["annual_income", "spending_score"]
    CATEGORICAL_COLUMNS = []

    # postgresql variable for create table
    POSTGRES_DEFINE = """
        customer_id INTEGER PRIMARY KEY,
        gender VARCHAR(50),
        age INTEGER,
        annual_income INTEGER,
        spending_score INTEGER,
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


mall_config = MallConfig()
