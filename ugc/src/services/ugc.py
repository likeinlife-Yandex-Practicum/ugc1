import json
from time import time
from uuid import UUID

from aiokafka import AIOKafkaProducer
from fastapi import Depends
from pydantic import BaseModel
from src.db.kafka import get_kafka_producer


class UGCService:
    def __init__(self, kafka_producer):
        self.kafka_producer = kafka_producer

    async def add_event_to_kafka(
        self, topic: str, user_id: UUID, event_schema: BaseModel
    ) -> None:
        """Send created payload to kafka"""
        value = self.create_payload(user_id, event_schema)
        await self.kafka_producer.send_and_wait(
            topic=topic,
            key=str(user_id).encode("utf-8"),
            value=json.dumps(value).encode("utf-8"),
        )

    @staticmethod
    def create_payload(user_id: UUID, event_schema: BaseModel) -> dict:
        """Create payload by schema and common fields"""
        payload = event_schema.model_dump()
        payload["user_id"] = user_id
        payload["timestamp"] = int(time())
        return payload


def get_ugc_service(
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer)
) -> UGCService:
    return UGCService(kafka_producer)
