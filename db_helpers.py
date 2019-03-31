from initial import get_config
from source.database_connector.postgres_connector import companies, workers, goods, meta
from sqlalchemy import create_engine

DSN = "postgresql://{user}:{password}@{host}:{port}/{name}"

ADMIN_DB_URL = DSN.format(
    user='postgres', password='1211', name='notify_db',
    host='localhost', port=5432
)

admin_engine = create_engine(ADMIN_DB_URL, isolation_level='AUTOCOMMIT')

USER_CONFIG_PATH = '../example_config.ini'
USER_CONFIG = get_config(['-c', USER_CONFIG_PATH])['database_settings']
USER_DB_URL = DSN.format(**USER_CONFIG)
user_engine = create_engine(USER_DB_URL)

TEST_CONFIG_PATH = '../test_config.ini'
TEST_CONFIG = get_config(['-c', TEST_CONFIG_PATH])['database_settings']
TEST_DB_URL = DSN.format(**TEST_CONFIG)
test_engine = create_engine(TEST_DB_URL)


def teardown_db(db_settings):
    db_name = db_settings.get('name')
    with admin_engine.connect() as conn:
        conn.execute("""
                  SELECT pg_terminate_backend(pg_stat_activity.pid)
                  FROM pg_stat_activity
                  WHERE pg_stat_activity.datname = '%s'
                    AND pid <> pg_backend_pid();""" % db_name)
        conn.execute("DROP DATABASE IF EXISTS %s" % db_name)


def setup_db(db_settings):
    db_name = db_settings.get('name')

    with admin_engine.connect() as conn:
        teardown_db(db_settings)
        conn.execute("CREATE DATABASE %s" % db_name)
    print('SETUP DB')


def create_tables(engine=test_engine):
    meta.create_all(bind=engine, tables=[companies, workers, goods])
    print('CREATE TABLES')


def drop_tables(engine=test_engine):
    meta.drop_all(bind=engine, tables=[goods, workers, companies])
    print('DROP TABLES')


def create_sample_data(engine=test_engine):
    with engine.connect() as conn:
        conn.execute(companies.insert(), [{"title": "Plushki", "description": "Bread and cakes", "id": 1}])
        conn.execute(workers.insert(), [{"full_name": "Vasya Pupkin", "position": "seller",
                                                   "phone_number": "89998765432",
                                                   "company_id": 1, "id": 1}])
        conn.execute(goods.insert(), [{"title": "Pretzel", "description": "It's tasty!", "price": "30",
                                             "counts": 20, "worker_id": 1, "company_id": 1, "id": 1}])
