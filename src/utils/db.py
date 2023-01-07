import os
import sys

src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_path)
import psycopg2

from configs import config


def get_postgres_connection():
    try:
        conn = psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            database=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            options="-c statement_timeout=30000",
        )
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
