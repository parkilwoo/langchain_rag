from celery import Celery
from celery.result import AsyncResult
from typing import Any
import msgpack

from core.custom_logger import logger

class CeleryClient:
    _instance = None
        
    @classmethod
    def connect(cls, broker: str, backend: str):
        if isinstance(cls._instance, Celery):
            logger.info("Celery is already connected {}", cls._instance.conf)
            return
        logger.info("Connecting to Celery :: {}, {}", broker, backend)
        cls._instance = Celery(broker=broker, backend=backend)
    
    @classmethod
    def sync_send_task(cls, plain_data: Any):
        serialized_data = msgpack.packb(plain_data)
        result = cls._instance.send_task('embedding_inference', args=(serialized_data, ))
        async_result = AsyncResult(result.id, app=cls._instance)

        # 동기적으로 결과를 기다림
        task_result = async_result.get(timeout=10)
        if not task_result[0] == 200:
            raise ConnectionError(f"Celery Result Error :: {plain_data}")
        numpy_bytes = task_result[1].get('data')
        return numpy_bytes
        
        
