from source.database_connector.postgres_connector import AsyncPostgresqlConnector, companies, workers, goods, meta
from sqlalchemy.schema import CreateTable, DropTable


async def teardown_db(db_connector: AsyncPostgresqlConnector):
    async with db_connector.admin_engine.acquire() as conn:
        await conn.execute("""
                  SELECT pg_terminate_backend(pg_stat_activity.pid)
                  FROM pg_stat_activity
                  WHERE pg_stat_activity.datname = '%s'
                    AND pid <> pg_backend_pid();""" % db_connector.db_name)
        print('CLOSE CONN TO DB')
        await conn.execute("DROP DATABASE IF EXISTS %s" % db_connector.db_name)
        print('TEARDOWN DB')


async def setup_db(db_connector: AsyncPostgresqlConnector):
    async with db_connector.admin_engine.acquire() as conn:
        await teardown_db(db_connector)
        await conn.execute("CREATE DATABASE %s" % db_connector.db_name)
        print('SETUP DB')


async def create_tables(db_connector: AsyncPostgresqlConnector):
    async with db_connector.engine.acquire() as conn:
        for table in [companies, workers, goods]:
            create_expr = CreateTable(table)
            await conn.execute(create_expr)
        print('CREATE TABLES')


async def drop_tables(db_connector: AsyncPostgresqlConnector):
    async with db_connector.engine.acquire() as conn:
        for table in [goods, workers,companies]:
            create_expr = DropTable(table)
            await conn.execute(create_expr)
        print('DROP TABLES')


async def create_sample_data(db_connector: AsyncPostgresqlConnector):
    async with db_connector.engine.acquire() as conn:
        await conn.execute(companies.insert(), [{"title": "Plushki", "description": "Bread and cakes", "id": 1}])
        await conn.execute(workers.insert(), [{"full_name": "Vasya Pupkin", "position": "seller",
                                         "phone_number": "89998765432",
                                         "company_id": 1, "id": 1}])
        await conn.execute(goods.insert(), [{"title": "Pretzel", "description": "It's tasty!", "price": "30",
                                       "counts": 20, "worker_id": 1, "company_id": 1, "id": 1}])
