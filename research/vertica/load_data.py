from dataclasses import dataclass, astuple
import logging
import random
from uuid import uuid4, UUID

from utils import timeit
from vertica.config import TEST_SCHEMA, USER_AMOUNT, MOVIES_AMOUNT, BATCH_AMOUNT, BATCH_SIZE, TEST_TABLE

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

QUERY = f'''INSERT INTO {TEST_SCHEMA}.{TEST_TABLE} (user_id, movie_id, viewed_frame) VALUES (?, ?, ?)'''

user_id_list = [str(uuid4()) for _ in range(USER_AMOUNT)]
movie_id_list = [str(uuid4()) for _ in range(MOVIES_AMOUNT)]


@dataclass
class View:
    user_id: UUID
    movie_id: UUID
    viewed_frame: int


def generate_data():
    """Генерация тестовых данных."""
    for i in range(BATCH_AMOUNT):
        yield [
            astuple(
                View(
                    random.choice(user_id_list),
                    random.choice(movie_id_list),
                    random.randint(0, 100000)
                )
            )
            for _ in range(BATCH_SIZE)
        ]


@timeit
def load_data(cursor):
    """Загрузка тестовых данных."""
    for data in generate_data():
        try:
            cursor.executemany(QUERY, data, use_prepared_statements=True)
            logger.info('Data uploaded successfully')
        except Exception as error:
            logger.error('Load data error: %s', str(error))
