import pytest

from initial import get_config, BASE_DIR
from source.app import init_app
from db_helpers import setup_db, teardown_db, drop_tables, create_tables, create_sample_data

TEST_CONFIG = BASE_DIR / 'TEST_CONFIG.toml'


@pytest.fixture
async def api(aiohttp_client):
    app = init_app(['-c', TEST_CONFIG.as_posix()])
    return await aiohttp_client(app)


@pytest.fixture(scope='session')
def database():
    db_settings = get_config(['-c', TEST_CONFIG.as_posix()])['database_settings']
    setup_db(db_settings)
    yield
    teardown_db(db_settings)


@pytest.fixture
def tables_and_data(database):
    create_tables()
    create_sample_data()
    yield
    drop_tables()
