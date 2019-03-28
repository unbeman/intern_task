import asyncio

import pytest

from initial import get_config
from source.app import init_app
from source.database_connector.postgres_connector import AsyncPostgresqlConnector
from db_helpers import setup_db, teardown_db, drop_tables, create_tables, create_sample_data

test_config = '../example_config.ini'

@pytest.yield_fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)

    yield loop

    if not loop.is_closed():
        loop.call_soon(loop.stop)
        loop.run_forever()
        loop.close()


@pytest.fixture(scope='session')
def loop(event_loop):
    return event_loop

@pytest.fixture
async def api(aiohttp_client):
    app = init_app(['-c', test_config])
    return await aiohttp_client(app)


@pytest.fixture(scope='session')
async def db_connector(loop):
    db_settings = get_config(['-c', test_config])['database_settings']
    db_conn = AsyncPostgresqlConnector(**db_settings)
    await db_conn.init_admin_db()
    return db_conn


@pytest.fixture(scope='session')
async def database(db_connector, loop):
    await setup_db(db_connector)
    yield
    await teardown_db(db_connector)


@pytest.fixture
async def tables_and_data(db_connector, database):
    print("DB NAME", db_connector.db_name)
    await db_connector.init()
    await create_tables(db_connector)
    await create_sample_data(db_connector)

    yield

    await drop_tables(db_connector)
