import asyncio
import json
import uuid
from http import HTTPStatus
from lib2to3.pytree import generate_matches

from aiokafka import AIOKafkaConsumer
from httpx import AsyncClient

from tests.enums import ApiRoute, ClickHouseTable, KafkaTopic
from tests.settings import settings

from .misc import generate_resolution_pair, generate_string


async def test_click(
    net_client: AsyncClient,
    get_kafka_consumer,
    clickhouse_execute,
):
    kafka_consumer: AIOKafkaConsumer = get_kafka_consumer(KafkaTopic.CLICK)  # type: ignore
    await kafka_consumer.start()

    element = generate_string(5)
    content = dict(element=element)
    async with net_client as client:
        response = await client.post(ApiRoute.CLICK, params=content)
        assert response.status_code == HTTPStatus.CREATED

    kafka_content = await kafka_consumer.getone()
    await kafka_consumer.stop()
    assert kafka_content.key == str(settings.test_user.id).encode()
    values = json.loads(kafka_content.value)
    assert values['element'] == element

    await asyncio.sleep(10)
    query = f'SELECT * FROM {settings.clickhouse.database}.{ClickHouseTable.CLICK}'
    res = await clickhouse_execute(query)
    assert len(res) == 1
    assert res[0]['element'] == element


async def test_page_view(
    net_client: AsyncClient,
    get_kafka_consumer,
    clickhouse_execute,
):
    kafka_consumer: AIOKafkaConsumer = get_kafka_consumer(KafkaTopic.PAGE_VIEW)  # type: ignore
    await kafka_consumer.start()

    page = generate_string(5)
    content = dict(page=page)
    async with net_client as client:
        response = await client.post(ApiRoute.PAGE_VIEW, params=content)
        assert response.status_code == HTTPStatus.CREATED

    kafka_content = await kafka_consumer.getone()
    await kafka_consumer.stop()
    assert kafka_content.key == str(settings.test_user.id).encode()
    values = json.loads(kafka_content.value)
    assert values['page'] == page

    await asyncio.sleep(10)
    query = f'SELECT * FROM {settings.clickhouse.database}.{ClickHouseTable.PAGE_VIEW}'
    res = await clickhouse_execute(query)
    assert len(res) == 1
    assert res[0]['page'] == page


async def test_video_resolution_change(
    net_client: AsyncClient,
    get_kafka_consumer,
    clickhouse_execute,
):
    kafka_consumer: AIOKafkaConsumer = get_kafka_consumer(KafkaTopic.VIDEO_RESOLUTION_CHANGE)  # type: ignore
    await kafka_consumer.start()

    from_, to_ = generate_resolution_pair()
    content = dict(from_resolution=from_, to_resolution=to_)

    async with net_client as client:
        response = await client.post(ApiRoute.VIDEO_RESOLUTION_CHANGE, params=content)
        assert response.status_code == HTTPStatus.CREATED

    kafka_content = await kafka_consumer.getone()
    await kafka_consumer.stop()
    assert kafka_content.key == str(settings.test_user.id).encode()
    values = json.loads(kafka_content.value)
    assert values['from_resolution'] == from_
    assert values['to_resolution'] == to_

    await asyncio.sleep(10)
    query = f'SELECT * FROM {settings.clickhouse.database}.{ClickHouseTable.VIDEO_RESOLUTION_CHANGE}'
    res = await clickhouse_execute(query)
    assert len(res) == 1
    assert res[0]['from_resolution'] == from_
    assert res[0]['to_resolution'] == to_


async def test_search_filter_use(
    net_client: AsyncClient,
    get_kafka_consumer,
    clickhouse_execute,
):
    kafka_consumer: AIOKafkaConsumer = get_kafka_consumer(KafkaTopic.SEARCH_FILTER_USE)  # type: ignore
    await kafka_consumer.start()

    filter_, filter_value_ = generate_string(5), generate_string(5)
    content = dict(filter=filter_, filter_value=filter_value_)

    async with net_client as client:
        response = await client.post(ApiRoute.SEARCH_FILTER_USE, params=content)
        assert response.status_code == HTTPStatus.CREATED

    kafka_content = await kafka_consumer.getone()
    await kafka_consumer.stop()
    assert kafka_content.key == str(settings.test_user.id).encode()
    values = json.loads(kafka_content.value)
    assert values['filter'] == filter_
    assert values['filter_value'] == filter_value_

    await asyncio.sleep(10)
    query = f'SELECT * FROM {settings.clickhouse.database}.{ClickHouseTable.SEARCH_FILTER_USE}'
    res = await clickhouse_execute(query)
    assert len(res) == 1
    assert res[0]['filter'] == filter_
    assert res[0]['filter_value'] == filter_value_


async def test_video_finish(
    net_client: AsyncClient,
    get_kafka_consumer,
    clickhouse_execute,
):
    kafka_consumer: AIOKafkaConsumer = get_kafka_consumer(KafkaTopic.VIDEO_FINISH)  # type: ignore
    await kafka_consumer.start()

    film_id = str(uuid.uuid4())
    content = dict(film_id=film_id)

    async with net_client as client:
        response = await client.post(ApiRoute.VIDEO_FINISH, params=content)
        assert response.status_code == HTTPStatus.CREATED

    kafka_content = await kafka_consumer.getone()
    await kafka_consumer.stop()
    assert kafka_content.key == str(settings.test_user.id).encode()
    values = json.loads(kafka_content.value)
    assert values['film_id'] == film_id

    await asyncio.sleep(10)
    query = f'SELECT * FROM {settings.clickhouse.database}.{ClickHouseTable.VIDEO_FINISH}'
    res = await clickhouse_execute(query)
    assert len(res) == 1
    assert str(res[0]['film_id']) == film_id
