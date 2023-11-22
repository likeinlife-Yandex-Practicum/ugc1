import logging
from dataclasses import dataclass, asdict
import random
from uuid import uuid4, UUID

from clickhouse.config import USER_AMOUNT, MOVIES_AMOUNT, BATCH_AMOUNT, BATCH_SIZE, TEST_SCHEMA, TEST_TABLE
from utils import timeit

logger = logging.getLogger(__name__)

INSERT_QUERY = f'''INSERT INTO {TEST_SCHEMA}.{TEST_TABLE} VALUES'''

user_id_list = [str(uuid4()) for _ in range(USER_AMOUNT)]
movie_id_list = [str(uuid4()) for _ in range(MOVIES_AMOUNT)]


@dataclass
class View:
    id: int
    user_id: UUID
    movie_id: UUID
    viewed_frame: int


def generate_data():
    """Генерация тестовых данных."""
    for i in range(BATCH_AMOUNT):
        yield [
            asdict(
                View(
                    i,
                    random.choice(user_id_list),
                    random.choice(movie_id_list),
                    random.randint(0, 100000)
                )
            )
            for _ in range(BATCH_SIZE)
        ]


@timeit
def load_data(client):
    """Загрузка тестовых данных."""
    for data in generate_data():
        try:
            client.execute(INSERT_QUERY, data)
            logger.info('Data uploaded successfully')
        except Exception as error:
            logger.error('Load data error: %s', str(error))
