from infrastructure.celery_client import CeleryClient
from infrastructure.database import VectorRedisClient

class QueryRepository:
    _vector_redis_client = VectorRedisClient
    _celery_client = CeleryClient
    
    @classmethod
    def get_vector(cls, plain_query: str):
        return CeleryClient.sync_send_task(plain_query)
    
    @classmethod
    async def get_cache(cls, vector_bytes: bytes):
        response = await cls._vector_redis_client.get(vector_bytes)
        return response[0]
    
    @classmethod
    async def set_cache(cls, vector_bytes: bytes, query_result: str):
        return await cls._vector_redis_client.set(vector_bytes, query_result)