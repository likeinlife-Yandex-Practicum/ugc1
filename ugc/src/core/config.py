from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path


class Settings(BaseSettings):
    kafka_host: str = Field(env="KAFKA_HOST")
    kafka_port: str = Field(env="KAFKA_PORT")
    rsa_public_path: Path = Field()


settings = Settings()
