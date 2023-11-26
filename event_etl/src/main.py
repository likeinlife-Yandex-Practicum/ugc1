import logging

import backoff
from clickhouse_driver import Client

from .config import settings
from .helper import get_tables
from .table_create import (
    create_clickhouse_table,
    create_kafka_engine_table,
    create_materialized_view,
)

logging.basicConfig(level=logging.INFO)


@backoff.on_exception(
    backoff.expo,
    ConnectionError,
    max_tries=20,
)
def get_clickhouse_connection() -> Client:
    return Client(host=settings.clickhouse.host)


def initialize_clickhouse_database(client: Client):
    client.execute(
        f"CREATE DATABASE IF NOT EXISTS {settings.clickhouse.database_name}",
    )


def configure_kafka_etl():
    tables = get_tables(settings.json_config_path)
    client = get_clickhouse_connection()
    initialize_clickhouse_database(client)

    for table in tables:
        create_clickhouse_table(client, table)
        logging.info("created Clickhouse analytics table")
        create_kafka_engine_table(client, table)
        logging.info("created kafka queue table")
        create_materialized_view(client, table)
        logging.info("created materialized view")
