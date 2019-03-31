from database_connector.postgres_connector import AsyncPostgresqlConnector
import logging

loger = logging.getLogger(__name__)


class Controller:
    def __init__(self, db_connector: AsyncPostgresqlConnector):
        self.db_connector = db_connector

    async def create_company(self, data: dict) -> dict:
        return await self.db_connector.insert_company(data)

    async def update_company(self, company_id, data) -> bool:
        update_status = await self.db_connector.update_company(company_id, data)
        return update_status

    async def get_company(self, company_id) -> dict:
        company_info = await self.db_connector.get_company_by_id(company_id)
        return company_info

    async def create_worker(self, data: dict) -> dict:
        worker_id = await self.db_connector.insert_worker(data)
        return worker_id

    async def update_worker(self, worker_id: int, data: dict) -> bool:
        update_status = await self.db_connector.update_worker(worker_id, data)
        return update_status

    async def get_worker(self, worker_id: int) -> dict:
        worker_info = await self.db_connector.get_worker_by_id(worker_id)
        return worker_info

    async def add_goods(self, data: list) -> list:
        answer = []
        for item in data:
            tags = item.pop('tags', [])
            goods = await self.db_connector.insert_goods(item)
            answer.append(goods)
            for tag in tags:
                tag_info = await self.db_connector.get_tag_by_title(tag)
                if not tag_info:
                    tag_info = await self.db_connector.insert_tag(tag)
                await self.db_connector.insert_tags_to_goods(tag_info['id'], goods['id'])
        return answer

    async def get_goods_list(self) -> list:
        goods_list = await self.db_connector.get_goods()
        for goods in goods_list:
            tags = await self.db_connector.get_tags_of_goods(goods['id'])
            goods['tags'] = [tag['title'] for tag in tags]
        return goods_list

    async def assign_worker_to_goods(self, goods_id: int, data: dict) -> bool:
        return await self.db_connector.update_goods(goods_id, data)
