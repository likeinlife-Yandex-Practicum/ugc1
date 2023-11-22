from clickhouse_driver import Client

from clickhouse.config import TEST_SCHEMA, TEST_TABLE
from clickhouse.load_data import load_data

if __name__ == '__main__':
    client = Client(host="localhost")
    client.execute(f'CREATE DATABASE IF NOT EXISTS {TEST_SCHEMA} ON CLUSTER company_cluster')
    client.execute(f'''
        CREATE TABLE IF NOT EXISTS {TEST_SCHEMA}.{TEST_TABLE} (
            id Int64,
            user_id UUID,
            movie_id UUID,
            viewed_frame UInt32,            
        ) Engine=MergeTree() ORDER BY id
        '''
                   )

    load_data(client)
