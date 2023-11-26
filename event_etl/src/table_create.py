from clickhouse_driver import Client

from .config import settings
from .models import Table


def create_clickhouse_table(
    client: Client,
    table: Table,
):
    """Create clickhouse table.

    Used directly to retrieve data.
    """
    client.execute(
        f"""CREATE TABLE IF NOT EXISTS {settings.clickhouse.database_name}.{table.name}(
            {table.get_fields_in_str()}
        )
        Engine=MergeTree()
        PARTITION BY toYYYYMMDD(timestamp)
        ORDER BY timestamp"""
    )


def create_kafka_engine_table(
    client: Client,
    table: Table,
):
    """Create a streaming table that pulls data from Kafka into it."""
    client.execute(
        f"""CREATE TABLE IF NOT EXISTS {settings.clickhouse.database_name}.kafka_{table.name}(
                {table.get_fields_in_str()}
            )
            ENGINE = Kafka
            SETTINGS
            kafka_broker_list = '{settings.kafka.host}:{settings.kafka.port}',
            kafka_topic_list = '{table.topic}',
            kafka_group_name = 'clickhouse_reader',
            kafka_format = 'JSONEachRow',
            kafka_num_consumers = 1,
            kafka_max_block_size = {settings.kafka.max_block_size};"""
    )


def create_materialized_view(
    client: Client,
    table: Table,
):
    """Materialized view transport content from kafka_engine_table stream to clickhouse table."""
    client.execute(
        f"""CREATE MATERIALIZED VIEW IF NOT EXISTS {settings.clickhouse.database_name}.mv_kafka_{table.name}
        TO {settings.clickhouse.database_name}.{table.name} AS
        SELECT * FROM {settings.clickhouse.database_name}.kafka_{table.name};"""
    )
