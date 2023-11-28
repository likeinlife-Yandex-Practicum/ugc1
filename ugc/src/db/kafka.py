from typing import Optional

from aiokafka import AIOKafkaProducer


kafka_producer: Optional[AIOKafkaProducer] = None


async def get_kafka_producer() -> AIOKafkaProducer:
    return kafka_producer
