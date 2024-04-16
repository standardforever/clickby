import aioredis
from typing import Dict
import asyncio


class RedisClient:
    def __init__(self, redis_url: str) -> None:
        self.url = redis_url
        self.client = None

    async def connect(self):
        """ connection To Redis """
        self.client = await aioredis.from_url(self.url, decode_responses=True)

    async def test_connection(self):
        """ Test connection """
        if not self.client:
            raise RuntimeError("Redis connection not established")
        print(f"Ping successful: {await self.client.ping()}")

    async def get(self, key: str) -> Dict:
        """ Get dict data from redis """
        if not self.client:
            raise RuntimeError("Redis connection not established")
        return await self.client.hgetall(key)

    async def create(self, key: str, value: Dict, expire_time: int = 0) -> bool:
        """ Add dict data to redis """
        if not self.client:
            raise RuntimeError("Redis connection not established")
        if await self.client.hset(key, mapping=value):
            if expire_time:
                await self.client.expire(key, expire_time)
            return True
        return False
    
    async def update(self, key: str, value: Dict, expire_time: int = 0) -> bool:
        """ Update dict data in redis if exist or create if dosen't exit """
        if not self.client:
            raise RuntimeError("Redis connection not established")
        if await self.client.exists(key):
            await self.client.hset(key, mapping=value)
            if expire_time:
                await self.client.expire(expire_time)
            return True
        return await self.create(key=key, value=value, expire_time=expire_time)
    
    async def delete(self, key: str) -> bool:
        """ Delete key from redis """
        if not self.client:
            raise RuntimeError("Redis connection not established")
        if await self.client.exists(key):
            await self.client.delete(key)
            return True
        return False
    
    async def close_connection(self):
        """ Close the redis connection """
        if self.client:
            await self.client.close()