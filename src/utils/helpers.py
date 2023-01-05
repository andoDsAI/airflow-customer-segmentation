import gc
import os
import traceback

import pandas as pd
import psycopg2
import psycopg2.extras

from .db import get_postgres_connection


def truncate_table(table_name: str, conn=None):
    if not conn:
        conn = get_postgres_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"TRUNCATE TABLE {table_name}")
        conn.commit()
    except Exception as e:
        print(traceback.format_exc())
        conn.rollback()
        clean_garbage()
        raise e
    cur.close()
    conn.close()


def create_db_table(table_name: str, variable_define: str, conn=None, drop_table: bool = False):
    if not conn:
        conn = get_postgres_connection()
    cur = conn.cursor()
    try:
        if drop_table:
            cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            conn.commit()
        create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({variable_define})"
        cur.execute(create_query)
        conn.commit()
    except Exception as e:
        print(traceback.format_exc())
        conn.rollback()
        clean_garbage()
        raise e
    cur.close()
    conn.close()


def get_data_from_db(query: str, out_type="dict", columns=None, conn=None):
    """Get data from database using query

    Args:
            query (str): SQL query
            out_type (str, optional): Output type. Defaults to 'dict'.
            columns (list[str], optional): Define DataFrame columns if output type is 'df'. Defaults to None.
            conn (optional): Database connection. Defaults to None.
    """
    if not conn:
        conn = get_postgres_connection()
    cur = conn.cursor()
    try:
        cur.execute(query)
        records = cur.fetchall()
        if out_type == "dict":
            return records
        elif out_type == "df":
            if not columns:
                columns = [desc[0] for desc in cur.description]
                df = pd.DataFrame(records, columns=columns)
                return df
            else:
                df = pd.DataFrame(records, columns=columns)
                return df
    except Exception as e:
        print(traceback.format_exc())
        conn.rollback()
        clean_garbage()
        raise e
    cur.close()
    conn.close()


def clean_garbage():
    print("Cleaning garbage")
    gc.collect()
    print("Garbage cleaned")
