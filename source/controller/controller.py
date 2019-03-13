from database_connector.postgres_connector import AsyncPostgresqlConnector


class Controller:
    def __init__(self, db_connector: AsyncPostgresqlConnector):
        self.db_connector = db_connector

    async def create_company(self, data):
        company_id = await self.db_connector.insert_company(**data)
        return company_id
    
    async def update_company(self, company_id, data):
        update_status = await self.db_connector.update_company(company_id, **data)
        return update_status
        
    async def get_company(self, company_id):
        company_info = await self.db_connector.get_company_by_id(company_id)
        return company_info

    async def create_worker(self, data):
        worker_id = await self.db_connector.insert_worker(**data)
        return worker_id

    async def update_worker(self, worker_id, data):
        update_status = await self.db_connector.update_worker(worker_id, **data)
        return update_status

    async def get_worker(self, worker_id):
        worker_info = await self.db_connector.get_worker_by_id(worker_id)
        return worker_info
