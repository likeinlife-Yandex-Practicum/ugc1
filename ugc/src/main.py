from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from aiokafka import AIOKafkaProducer

from src.db import kafka
from src.core.config import settings
from src.core.exceptions import CustomException
from src.api.v1 import ugc


@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka.kafka_producer = AIOKafkaProducer(
        bootstrap_servers=[
            f"{settings.kafka_host}:{settings.kafka_port}"
        ]
    )
    await kafka.kafka_producer.start()
    yield
    await kafka.kafka_producer.stop()


app = FastAPI(
    title='UGC сервис',
    description='Сервис для отправки пользовательских данных',
    version='0.0.1',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


@app.exception_handler(CustomException)
async def exception_handler(request: Request, exc: CustomException):
    return ORJSONResponse(status_code=exc.status_code, content={'message': exc.message})


app.include_router(ugc.router, prefix='/api/v1/ugc', tags=['ugc'])
