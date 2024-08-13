from celery import Celery
import msgpack

from core.custom_logger import logger

class CeleryClient:
    _instance = None

    def __init__(self, *args, **kwargs) -> None:
        pass
        
    @classmethod
    def connect(cls, broker: str, backend: str):
        if isinstance(cls._instance, Celery):
            logger.info("Celery is already connected %s", cls._instance.conf)
            return
        logger.info("Connecting to Celery :: %s, %s", broker, backend)
        cls._instance = Celery(broker=broker, backend=backend)
