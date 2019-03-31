import aiopg.sa
import logging

try:
    from utils import RecordNotFound, TransactionFailed
except:
    from source.utils import RecordNotFound, TransactionFailed
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, UniqueConstraint, \
    PrimaryKeyConstraint, Float, select

logger = logging.getLogger(__name__)

meta = MetaData()  # TODO: rename schema

companies = Table(
    'companies', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String, nullable=False, unique=True),
    Column('description', String)
)

workers = Table(
    'workers', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String, nullable=False),
    Column('position', String, nullable=False),
    Column('phone_number', String, nullable=False),

    Column('fk_company_id',
           Integer,
           ForeignKey('companies.id'), key='company_id')
)

tags_to_goods = Table(
    'tags_to_goods', meta,
    Column('tag_id', Integer, ForeignKey('tags.id'), key='tag_id'),
    Column('goods_id', Integer, ForeignKey('goods.id'), key='goods_id'),
    PrimaryKeyConstraint('tag_id', 'goods_id')
)

goods = Table(
    'goods', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String, nullable=False),
    Column('description', String),
    Column('price', Float, nullable=False),
    Column('counts', Integer, default=1, key='count'),
    Column('fk_worker_id', Integer, ForeignKey('workers.id'), key='worker_id', default=None),
    Column('fk_company_id', Integer, ForeignKey('companies.id'), key='company_id'),
    UniqueConstraint('title', 'company_id')
)

tags = Table(
    'tags', meta,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False, unique=True),
    UniqueConstraint('id', 'title')
)


# TODO: wrap exceptions
class AsyncPostgresqlConnector:
    def __init__(self, name: str, user: str, password: str, host: str, port: int):
        self.db_name = name
        self.dsn = "dbname={} user={} password={} host={} port={}".format(name, user, password, host, port)
        self.engine = None
        self.admin_engine = None

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
                answer = parse_row_result(row.items())  # TODO: wrap to function get_items_from_row
            else:
                raise RecordNotFound("Worker with {} id does not exist".format(company_id))
        return answer

    async def insert_company(self, data: dict) -> dict:
        answer = {}
        async with self.engine.acquire() as conn:
            result = await conn.execute(
                companies.insert().values(**data).returning(companies.c.id))
            row = await result.first()
            if row:
                answer = parse_row_result(row.items())
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
                answer = parse_row_result(row.items())
        return answer

    async def update_worker(self, worker_id: int, data: dict) -> bool:
        async with self.engine.acquire() as conn:
            result = await conn.execute(
                workers.update().values(**data).where(
                    workers.c.id == worker_id))
            count = result.rowcount
            if count:
                return True
        return False

    async def get_worker_by_id(self, worker_id: int) -> dict:
        answer = {}
        async with self.engine.acquire() as conn:
            result = await conn.execute(workers.select().where(workers.c.id == worker_id))
            row = await result.first()
            if row:
                answer = parse_row_result(row.items())
            else:
                raise RecordNotFound("Worker with {} id does not exist".format(worker_id))
        return answer

    async def insert_goods(self, data: dict) -> dict:
        answer = {}
        async with self.engine.acquire() as conn:
            async with conn.begin():
                try:
                    result = await conn.execute(
                        goods.insert().values(**data).returning(goods.c.id, goods.c.title, goods.c.company_id))
                    row = await result.first()
                    if row:
                        answer = parse_row_result(row.items())
                except Exception:
                    raise TransactionFailed()
        return answer

    async def insert_tag(self, tag_name: str) -> dict:
        answer = {}
        async with self.engine.acquire() as conn:
            async with conn.begin():
                try:
                    result = await conn.execute(tags.insert().values(title=tag_name).returning(tags.c.id, tags.c.title))
                    row = await result.first()
                    if row:
                        answer = parse_row_result(row.items())
                except Exception:
                    raise TransactionFailed()
        return answer

    async def get_tag_by_title(self, title: str) -> dict:
        answer = {}
        async with self.engine.acquire() as conn:
            async with conn.begin():
                try:
                    result = await conn.execute(tags.select().where(tags.c.title == title))
                    row = await result.first()
                    if row:
                        answer = parse_row_result(row.items())
                except Exception:
                    raise TransactionFailed()
        return answer

    async def insert_tags_to_goods(self, tag_id: int, goods_id: int):
        async with self.engine.acquire() as conn:
            async with conn.begin():
                try:
                    await conn.execute(tags_to_goods.insert().values(tag_id=tag_id, goods_id=goods_id))
                except Exception:
                    raise TransactionFailed()
        return

    async def get_goods(self):
        answer = []
        async with self.engine.acquire() as conn:
            result = await conn.execute(goods.select())
            rows = await result.fetchall()
            for row in rows:
                answer.append(parse_row_result(row.items()))
        return answer

    async def get_tags_of_goods(self, goods_id: int):
        answer = []
        async with self.engine.acquire() as conn:
            j = tags.join(tags_to_goods, tags_to_goods.c.tag_id == tags.c.id)
            result = await conn.execute(
                select([tags.c.title]).select_from(j).where(tags_to_goods.c.goods_id == goods_id)
                )
            rows = await result.fetchall()
            for row in rows:
                answer.append(parse_row_result(row.items()))
        return answer

    async def update_goods(self, item_id: int, data):
        async with self.engine.acquire() as conn:
            result = await conn.execute(
                goods.update().values(**data).where(
                    goods.c.id == item_id))
            count = result.rowcount
            if count:
                return True
        return False


def parse_row_result(items) -> dict:
    return {key: value for key, value in items}
