import vertica_python

from vertica.config import CONNECTION_INFO, TEST_SCHEMA, TEST_TABLE
from vertica.load_data import load_data

if __name__ == '__main__':
    with vertica_python.connect(**CONNECTION_INFO) as connection:
        cursor = connection.cursor()

        # создаем схему и таблицу
        cursor.execute(f'''CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA};''')
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TEST_SCHEMA}.{TEST_TABLE} (
        id IDENTITY,
        user_id UUID NOT NULL,
        movie_id UUID NOT NULL,
        viewed_frame INTEGER NOT NULL
    );
        ''')

        # загружаем тестовые данные
        load_data(cursor)
