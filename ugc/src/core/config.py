from logging import config as logging_config
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings

from .log_config import get_logging_settings


class Settings(BaseSettings):
    kafka_host: str = Field()
    kafka_port: str = Field()
    rsa_public_path: Path = Field()

    logging_level: str = Field("INFO")
    console_logging_level: str = Field("DEBUG")


settings = Settings()

logging_config.dictConfig(
    get_logging_settings(
        settings.logging_level,
        settings.console_logging_level,
    )
)
