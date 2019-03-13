import aiopg
import logging

logger = logging.getLogger(__name__)


# TODO: wrap exceptions
class AsyncPostgresqlConnector:
    def __init__(self, name: str, user: str, password: str, host: str, port: int):
        self.dsn = "dbname={} user={} password={} host={} port={}".format(name, user, password, host, port)
        self.pool = None

    async def create_pool(self):
        self.pool = await aiopg.create_pool(self.dsn)

    async def close_pool(self):
        self.pool.close()

    async def get_company_by_id(self, company_id: int) -> dict:
        answer = {}
        sql = "SELECT id, title, description " \
              "FROM avito_shop.companies " \
              "WHERE id=%s;"
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, (company_id,))
                rows = await cur.fetchall()
                for row in rows:
                    answer["id"] = row[0]
                    answer["title"] = row[1]
                    answer["description"] = row[2]
        return answer

    async def insert_company(self, title: str, description: int) -> dict:
        sql = "INSERT INTO avito_shop.companies (title, description)" \
              "VALUES (%s, %s)" \
              "RETURNING id;"
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, (title, description,))
                row = await cur.fetchone()
                if row:
                    return {"id": row[0]}
        return {}

    async def update_company(self, company_id, title: str = None, description: int = None) -> bool:
        sql = "UPDATE avito_shop.companies " \
              "SET title=%s, description=%s " \
              "WHERE id=%s;"
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, (title, description, company_id))
                count = cur.rowcount
                if count:
                    return True
        return False

    async def insert_worker(self, full_name: str, position: str, company_id: int, phone_number: str = "") -> dict:
        sql = "INSERT INTO avito_shop.workers (full_name, position, fk_company_id, phone_number)" \
              "VALUES (%s, %s, %s, %s)" \
              "RETURNING id;"
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, (full_name, position, company_id, phone_number))
                row = await cur.fetchone()
                if row:
                    return {"id": row[0]}
        return {}

    async def update_worker(self, worker_id, full_name: str = None, position: str = None, company_id: int = None,
                            phone_number: str = None) -> bool:
        sql = "UPDATE avito_shop.workers " \
              "SET full_name=%s, position=%s, fk_company_id=%s, phone_number=%s " \
              "WHERE id=%s;"
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, (full_name, position, company_id, phone_number, worker_id,))
                count = cur.rowcount
                if count:
                    return True
        return False

    async def get_worker_by_id(self, worker_id: str) -> dict:
        sql = "SELECT id, full_name, position, fk_company_id, phone_number " \
              "FROM avito_shop.workers " \
              "WHERE id=%s;"
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, (worker_id,))
                row = await cur.fetchone()
                if row:
                    return {"id": row[0],
                            "full_name": row[1],
                            "position": row[2],
                            "company_id": row[3],
                            "phone_number": row[4]}
        return {}
