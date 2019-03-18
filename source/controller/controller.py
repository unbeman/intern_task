from database_connector.postgres_connector import AsyncPostgresqlConnector


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

    async def update_worker(self, worker_id, data) -> bool:
        update_status = await self.db_connector.update_worker(worker_id, data)
        return update_status

    async def get_worker(self, worker_id) -> dict:
        worker_info = await self.db_connector.get_worker_by_id(worker_id)
        return worker_info

    async def add_items(self, data: dict) -> dict:
        return await self.db_connector.insert_item(data)

    async def get_items_list(self):
        return await self.db_connector.get_items()

    async def assign_worker_to_item(self, item_id: int, data: dict):
        return await self.db_connector.update_item(item_id, data)
