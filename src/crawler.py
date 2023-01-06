import argparse
import pandas as pd

from utils.helpers import create_db_table, insert_data_to_db


def crawl_customer_data(customer_type: str, config):
    df = pd.read_csv(f"../data/{customer_type.lower()}_customers.csv")
    df = df.astype(config.PANDAS_SCHEMA)
    # rename columns
    df.rename(mapper=config.COLUMN_MAPPING, axis=1, inplace=True)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_type", type=str, help="Type of customer", required=True)
    args = parser.parse_args()
    
    exec(f"from config import {args.customer_type.lower()}_config")
    
    config = eval(f"{args.customer_type.lower()}_config")
    # crawl data
    customer_data = crawl_customer_data(args.customer_type, config)
    
    # insert data to database
    table_name = config.TABLE_NAME
    create_db_table(
        table_name=table_name,
        variable_define=config.POSTGRES_DEFINE,
        drop_table=False,
    )
    
    insert_data_to_db(
        table_name=table_name,
        data=customer_data,
    )
    
    print(f"Data for {args.customer_type} customer has been inserted to database")
