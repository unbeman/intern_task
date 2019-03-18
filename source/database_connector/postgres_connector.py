import aiopg.sa
import sqlalchemy
import logging
import utils
from sqlalchemy import MetaData, Table, Column, Integer, String, Date, ForeignKey, Numeric, DateTime

logger = logging.getLogger(__name__)

meta = MetaData(schema='avito_shop')  # TODO: rename schema

companies = Table(
    'companies', meta,

    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', String)
)

workers = Table(
    'workers', meta,

    Column('id', Integer, primary_key=True),
    Column('full_name', String, nullable=False),
    Column('position', String, nullable=False),
    Column('phone_number', String, nullable=False),

    Column('fk_company_id',
           Integer,
           ForeignKey('companies.id'), key='company_id')
)

goods = Table(
    'goods', meta,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', String),
    Column('price', Numeric, nullable=False),
    Column('counts', Integer),
    Column('fk_worker_id', Integer, ForeignKey('workers.id'), key='worker_id'),
    Column('fk_company_id', Integer, ForeignKey('companies.id'), key='company_id')
)


# TODO: wrap exceptions
class AsyncPostgresqlConnector:
    def __init__(self, name: str, user: str, password: str, host: str, port: int):
        self.dsn = "dbname={} user={} password={} host={} port={}".format(name, user, password, host, port)
        self.engine = None

    async def init(self):
        self.engine = await aiopg.sa.create_engine(dsn=self.dsn, echo=True)

    async def close(self):
        self.engine.close()
        await self.engine.wait_closed()

    async def get_company_by_id(self, company_id: int) -> dict:
        answer = {}
        async with self.engine.acquire() as conn:
            result = await conn.execute(companies.select().where(companies.c.id == company_id))
            row = await result.first()
            if row:
                answer = {key: value for key, value in row.items()}
            else:
                raise utils.RecordNotFound("Worker with {} id does not exist".format(company_id))
        return answer

    async def insert_company(self, data: dict) -> dict:
        answer = {}
        async with self.engine.acquire() as conn:
            result = await conn.execute(
                companies.insert().values(**data).returning(companies.c.id))
            row = await result.first()
            if row:
                answer = {key: value for key, value in row.items()}
        return answer

    async def update_company(self, company_id, data: dict) -> bool:
        async with self.engine.acquire() as conn:
            result = await conn.execute(
                companies.update().values(**data).where(companies.c.id == company_id))
            count = result.rowcount
            if count:
                return True
        return False

    async def insert_worker(self, data: dict) -> dict:
        answer = {}
        async with self.engine.acquire() as conn:
            result = await conn.execute(
                workers.insert().values(**data).returning(workers.c.id))
            row = await result.first()
            if row:
                answer = {key: value for key, value in row.items()}
        return answer

    async def update_worker(self, worker_id, data: dict) -> bool:
        async with self.engine.acquire() as conn:
            result = await conn.execute(
                workers.update().values(**data).where(
                    workers.c.id == worker_id))
            count = result.rowcount
            if count:
                return True
        return False

    async def get_worker_by_id(self, worker_id: str) -> dict:
        answer = {}
        async with self.engine.acquire() as conn:
            result = await conn.execute(workers.select().where(workers.c.id == worker_id))
            row = await result.first()
            if row:
                answer = {key: value for key, value in row.items()}
            else:
                raise utils.RecordNotFound("Worker with {} id does not exist".format(worker_id))
        return answer

    async def __insert_item(self, conn, data: dict):
        await conn.execute(
            goods.insert().values(**data).returning(goods.c.id, goods.c.title, goods.c.fk_company_id))

    async def insert_item(self, data: dict):
        async with self.engine.acquire() as conn:
            async with conn.begin():
                try:
                    for item in data:
                        await self.__insert_item(conn, **item)
                except Exception:
                    raise utils.TransactionFailed()
        return True

    async def get_items(self):
        answer = []
        async with self.engine.acquire() as conn:
            result = await conn.execute(goods.select())
            rows = await result.fetchall
            for row in rows:
                answer.append({key: value for key, value in row.items()})
        return answer

    async def update_item(self, item_id: int, data):
        async with self.engine.acquire() as conn:
            result = await conn.execute(
                goods.update().values(**data).where(
                    goods.c.id == item_id))
            count = result.rowcount
            if count:
                return True
        return False
