import aioredis
from abc import ABC, abstractmethod

class BaseRedisClient(ABC):

    
    @abstractmethod
    async def get(self, key):
        pass

    @abstractmethod
    async def set(self, key, value):
        pass

    @abstractmethod
    async def test_connecetion(self):
        pass

class VectorRedisClient(BaseRedisClient):
    _instance = None

    def __new__(cls, url: str, encoding: str = 'utf-8', decode_responses: bool = True, ttl: int = 600):
        if not cls._instance:
            cls._instance = aioredis.from_url(url, encoding=encoding, decode_responses=decode_responses)
            cls._ttl = ttl
        return cls._instance
    
    