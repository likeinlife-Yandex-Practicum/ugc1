from pathlib import Path
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    host: str = Field()
    port: int = Field()
    max_block_size: int = Field(2**20)

    class Config:
        env_prefix = "kafka_"


class ClickHouseSettings(BaseSettings):
    host: str = Field()
    database_name: str = Field()

    class Config:
        env_prefix = "clickhouse_"


class Settings(BaseSettings):
    kafka: ClassVar = KafkaSettings()
    clickhouse: ClassVar = ClickHouseSettings()
    root: Path = Path(__file__).parent.parent
    json_config_path: Path = root / "data/clickhouse_tables.json"

    debug: bool = Field(False)

    class Config:
        env_prefix = ""


settings = Settings()
