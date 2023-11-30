import uuid
from typing import Any, Callable

import aiochclient
import aiokafka
import httpx
import pytest
import pytest_asyncio

from .jwt_service import get_jwt_service
from .settings import settings


@pytest_asyncio.fixture
async def access_token() -> str:
    jwt_service = get_jwt_service()
    return jwt_service.encode_access_token(
        str(settings.test_user.id),
        settings.test_user.email,
        settings.test_user.roles,
    )


@pytest_asyncio.fixture
async def net_client(access_token) -> httpx.AsyncClient:
    cookies = dict(access_token=access_token)
    return httpx.AsyncClient(
        base_url=settings.api_base_url,
        cookies=cookies,
    )


@pytest_asyncio.fixture
async def clickhouse_execute():
    async def _inner(query: str) -> list:
        async with httpx.AsyncClient() as client:
            ch_client = aiochclient.ChClient(client, url=settings.clickhouse_url)
            return await ch_client.fetch(query)

    return _inner


@pytest_asyncio.fixture
async def get_kafka_consumer() -> Callable[[str], aiokafka.AIOKafkaConsumer]:
    def _inner(topic_name: str) -> aiokafka.AIOKafkaConsumer:
        return aiokafka.AIOKafkaConsumer(
            topic_name,
            bootstrap_servers=settings.kafka_url,
            enable_auto_commit=False,
        )

    return _inner
