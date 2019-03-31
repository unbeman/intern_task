from source.initial import get_config, BASE_DIR
from source.database_connector.postgres_connector import companies, workers, goods, meta
from sqlalchemy import create_engine

DSN = "postgresql://{user}:{password}@{host}:{port}/{name}"

ADMIN_CONFIG_PATH = BASE_DIR / 'admin_config.toml'
ADMIN_CONFIG = get_config(['-c', ADMIN_CONFIG_PATH.as_posix()])['database_settings']
ADMIN_DB_URL = DSN.format(**ADMIN_CONFIG)
admin_engine = create_engine(ADMIN_DB_URL, isolation_level='AUTOCOMMIT')


USER_CONFIG_PATH = BASE_DIR / 'example_config.toml'
USER_CONFIG = get_config(['-c', USER_CONFIG_PATH.as_posix()])['database_settings']
USER_DB_URL = DSN.format(**USER_CONFIG)
user_engine = create_engine(USER_DB_URL, isolation_level='AUTOCOMMIT')

TEST_CONFIG_PATH = BASE_DIR / 'test_config.toml'
TEST_CONFIG = get_config(['-c', TEST_CONFIG_PATH.as_posix()])['database_settings']
TEST_DB_URL = DSN.format(**TEST_CONFIG)
test_engine = create_engine(TEST_DB_URL, isolation_level='AUTOCOMMIT')


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


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='DB related shortcuts')
    parser.add_argument("-c", "--create",
                        help="Create empty database",
                        action='store_true')
    parser.add_argument("-d", "--drop",
                        help="Drop database",
                        action='store_true')
    parser.add_argument("-r", "--recreate",
                        help="Drop and recreate database",
                        action='store_true')
    parser.add_argument("-a", "--all",
                        help="Create sample data",
                        action='store_true')
    args = parser.parse_args()

    if args.create:
        setup_db(USER_CONFIG)
    elif args.drop:
        teardown_db(USER_CONFIG)
    elif args.recreate:
        teardown_db(USER_CONFIG)
        setup_db(USER_CONFIG)
    elif args.all:
        teardown_db(USER_CONFIG)
        setup_db(USER_CONFIG)
        create_tables(user_engine)
        # create_sample_data()
    else:
        parser.print_help()
