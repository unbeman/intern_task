from source.app import init_app
import pytest

test_config = 'example_config.ini'


@pytest.fixture
def loop(event_loop):
    return event_loop


@pytest.fixture
def api(loop, aiohttp_client):
    app = init_app(['-c', test_config])
    yield loop.run_until_complete(aiohttp_client(app))
    loop.run_until_complete(app.shutdown())
