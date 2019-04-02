import aioredis


class RedisConnector:
    def __init__(self, host, port, loop):
        self.host = host
        self.port = port
        self.pool = None
        self.loop = loop

    async def init(self):
        self.pool = await aioredis.create_redis_pool((self.host, self.port), loop=self.loop)

    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()
