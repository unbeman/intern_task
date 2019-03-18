import pytest
from source.app import init_app

test_config = '../example_config.ini'

@pytest.fixture
def api(loop, test_client):
    app = init_app(['-c', test_config])
    yield loop.run_until_complete(test_client(app))
    loop.run_until_complete(app.shutdown())
