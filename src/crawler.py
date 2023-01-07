import argparse
import os

import pandas as pd

from utils.helpers import create_db_table, insert_data_to_db, truncate_table


def crawl_customer_data(customer_type: str, config):
    # get current path of this file
    current_path = os.path.dirname(os.path.abspath(__file__))
    if customer_type == "e_commerce":
        df = pd.read_csv(
            os.path.join(current_path, f"data/{customer_type.lower()}_customers.csv"),
            encoding="unicode_escape",
        )
    else:
        df = pd.read_csv(os.path.join(current_path, f"data/{customer_type.lower()}_customers.csv"))
    # rename columns
    df.rename(mapper=config.COLUMN_MAPPING, axis=1, inplace=True)
    df = df[config.NEW_COLUMNS_NAME]
    # drop all rows with null customer_id
    df.dropna(subset=["customer_id"], inplace=True)
    # reset index
    df.reset_index(drop=True, inplace=True)

    if customer_type == "e_commerce":
        grouper = df.groupby("customer_id")

        amount = grouper["unit_price", "quantity"].apply(
            lambda x: (x["unit_price"] * x["quantity"]).sum()
        )
        country = grouper["country"].apply(lambda x: x.value_counts().index[0])

        df = pd.concat([amount, country], axis=1)
        df.reset_index(inplace=True)
        df = df.rename(columns={"customer_id": "customer_id", 0: "amount", "country": "country"})

    df = df.astype(config.PANDAS_SCHEMA)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer_type", type=str, help="Type of customer", required=True)
    args = parser.parse_args()

    exec(f"from configs import {args.customer_type.lower()}_config")

    config = eval(f"{args.customer_type.lower()}_config")
    # crawl data
    customer_data = crawl_customer_data(args.customer_type, config)

    # insert data to database
    table_name = config.TABLE_NAME
    create_db_table(
        table_name=table_name,
        variable_define=config.POSTGRES_DEFINE,
        drop_table=True,
    )
    truncate_table(table_name=table_name)
    insert_data_to_db(
        table_name=table_name,
        data=customer_data,
    )

    print(f"Data for {args.customer_type} customer has been inserted to database")
