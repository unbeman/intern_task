import utils
from database_connector.postgres_connector import AsyncPostgresqlConnector
import logging

loger = logging.getLogger(__name__)


class Controller:
    def __init__(self, db_connector: AsyncPostgresqlConnector):
        self.db_connector = db_connector

    async def create_company(self, data: dict) -> dict:
        async with self.db_connector.engine.acquire() as conn:
            return await self.db_connector.insert_company(conn, data)

    async def update_company(self, company_id, data) -> bool:
        async with self.db_connector.engine.acquire() as conn:
            await self.get_company(company_id)
            return await self.db_connector.update_company(conn, company_id, data)

    async def get_company(self, company_id) -> dict:
        async with self.db_connector.engine.acquire() as conn:
            company_info = await self.db_connector.get_company_by_id(conn, company_id)
            if not company_info:
                raise utils.NotFound("Company with id {} does not exist".format(company_id))
        return company_info

    async def create_worker(self, data: dict) -> dict:
        async with self.db_connector.engine.acquire() as conn:
            await self.get_company(data['company_id'])
            return await self.db_connector.insert_worker(conn, data)

    async def update_worker(self, worker_id: int, data: dict) -> bool:
        async with self.db_connector.engine.acquire() as conn:
            await self.get_worker(worker_id)
            if 'company_id' in data:
                await self.get_company(data['company_id'])
            return await self.db_connector.update_worker(conn, worker_id, data)

    async def get_worker(self, worker_id: int) -> dict:
        async with self.db_connector.engine.acquire() as conn:
            worker_info = await self.db_connector.get_worker_by_id(conn, worker_id)
            if not worker_info:
                raise utils.NotFound("Worker with id {} does not exist".format(worker_id))
        return worker_info

    async def add_goods(self, data: list) -> list:
        answer = []
        async with self.db_connector.engine.acquire() as conn:
            async with conn.begin():
                for item in data:
                    tags = item.pop('tags', [])
                    await self.get_company(item['company_id'])
                    if 'worker_id' in data:
                        await self.get_worker(item['worker_id'])
                    goods = await self.db_connector.insert_goods(conn, item)
                    answer.append(goods)
                    for tag in tags:
                        tag_info = await self.db_connector.get_tag_by_title(conn, tag)
                        if not tag_info:
                            tag_info = await self.db_connector.insert_tag(conn, tag)
                        await self.db_connector.insert_tags_to_goods(conn, tag_info['id'], goods['id'])
        return answer

    async def update_goods(self, goods_id, data):
        async with self.db_connector.engine.acquire() as conn:
            async with conn.begin():
                tags = set(data.pop('tags', []))
                if 'company_id' in data:
                    await self.get_company(data['company_id'])
                if 'worker_id' in data:
                    await self.get_worker(data['worker_id'])
                await self.db_connector.update_goods(conn, goods_id, data)
                goods_tags = await self.db_connector.get_tags_of_goods(conn, goods_id)
                for tag in tags:
                    if tag not in goods_tags:
                        tag_info = await self.db_connector.get_tag_by_title(conn, tag)
                        if not tag_info:
                            tag_info = await self.db_connector.insert_tag(conn, tag)
                        await self.db_connector.insert_tags_to_goods(conn, tag_info['id'], goods_id)

    async def get_goods(self, goods_id):
        async with self.db_connector.engine.acquire() as conn:
            goods_info = await self.db_connector.get_goods_by_id(conn, goods_id)
            if not goods_info:
                raise utils.NotFound("Goods with id {} does not exist".format(goods_id))
        return goods_info

    async def get_goods_list(self) -> list:
        async with self.db_connector.engine.acquire() as conn:
            goods_list = await self.db_connector.get_goods(conn)
            for goods in goods_list:
                tags = await self.db_connector.get_tags_of_goods(conn, goods['id'])
                goods['tags'] = [tag['title'] for tag in tags]
        return goods_list

    async def get_goods_of_company_id(self, company_id):
        async with self.db_connector.engine.acquire() as conn:
            await self.get_company(company_id)
            return await self.db_connector.get_goods(conn, company_id)

    async def get_workers_by_company_id(self, company_id):
        async with self.db_connector.engine.acquire() as conn:
            await self.get_company(company_id)
            return await self.db_connector.get_workers_by_company_id(conn, company_id)

    async def assign_worker_to_goods(self, goods_id: int, data: dict) -> bool:
        async with self.db_connector.engine.acquire() as conn:
            await self.get_goods(goods_id)
            await self.get_worker(data['worker_id'])
            return await self.db_connector.update_goods(conn, goods_id, data)
