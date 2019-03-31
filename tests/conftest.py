import pytest

from initial import get_config
from source.app import init_app
from db_helpers import setup_db, teardown_db, drop_tables, create_tables, create_sample_data

test_config = '../test_config.ini'

admin_database_settings = {
    'name': 'notify_db',
    'user': 'postgres',
    'password': '1211',
    'host': '127.0.0.1',
    'port': 5432,
}


@pytest.fixture
async def api(aiohttp_client):
    app = init_app(['-c', test_config])
    return await aiohttp_client(app)


@pytest.fixture(scope='session')
def database():
    db_settings = get_config(['-c', test_config])['database_settings']
    setup_db(db_settings)
    yield
    teardown_db(db_settings)


@pytest.fixture
def tables_and_data(database):
    create_tables()
    create_sample_data()
    yield
    drop_tables()
