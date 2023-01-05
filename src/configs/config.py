import os

import dotenv

# load environment variables from .env file
dotenv.load_dotenv()


class Config(object):
    # postgresql configuration
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_AIRFLOW_DB = os.getenv("POSTGRES_DB")

    POSTGRES_APP_DB = os.getenv("POSTGRES_APP_DB")


config = Config()
