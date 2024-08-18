import aioredis
from abc import ABC, abstractmethod
import uuid
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from typing import List
from core.custom_logger import logger


class BaseRedisClient(ABC):
    
    def __new__(cls, url: str, encoding: str = 'utf-8', decode_responses: bool = True, ttl: int = 600):
        if not cls._instance:
            logger.debug("{} redis connecting..", url)
            cls._instance = aioredis.from_url(url, encoding=encoding, decode_responses=decode_responses)
            cls._ttl = ttl
            logger.debug("{} connect successed", url)
        return cls._instance

    @classmethod
    @abstractmethod    
    async def get(cls, key):
        pass
    
    @classmethod
    @abstractmethod    
    async def set(cls, key, value):
        pass

class RedisClient(BaseRedisClient):
    _instance = None
    _ttl = None
    
    def __new__(cls, url: str, encoding: str = 'utf-8', decode_responses: bool = True, ttl: int = 600):
        cls._instance = super().__new__(cls, url, encoding, decode_responses, ttl)
     
    @classmethod   
    async def get(cls, key):
        return await cls._instance.get(key)
    
    @classmethod
    async def set(cls, key, value):
        await cls._instance.set(key, value, cls._ttl)

class VectorRedisClient(BaseRedisClient):
    _instance = None
    _ttl = None
    _index_name = 'query_index'
    _is_generated = False
    
    def __new__(cls, url: str, encoding: str = 'utf-8', decode_responses: bool = True, ttl: int = 600):
        cls._instance = super().__new__(cls, url, encoding, decode_responses, ttl)

    
    @classmethod
    async def generate_index(cls, reset: bool = False):
        try:
            await cls._instance.execute_command('FT.CREATE', cls._index_name, 
                            'ON', 'HASH', 
                            'PREFIX', '1', 'question:', 
                            'SCHEMA', 
                            'embedding', 'VECTOR', 'FLAT', '6', 'TYPE', 'FLOAT32', 'DIM', '384', 'DISTANCE_METRIC', 'COSINE')            
            logger.debug("Redis search index generate successed :: {}", cls._index_name)
        except Exception:
            logger.warning("Redis Index is already..")
            if reset:
                logger.debug("Redis start reset")
                await cls._instance.execute_command("FT.DROPINDEX", cls._index_name)
                await cls.generate_index(False)
                      
    
    @classmethod   
    async def get(cls, key):
        logger.debug(key)
        search_query = '* => [KNN 1 @embedding $BLOB AS score]'
        return await cls._instance.execute_command('FT.SEARCH', cls._index_name, search_query, 'PARAMS', '2', 'BLOB', key, 'SORTBY', 'score', 'ASC', 'RETURN', '0')
    
    @classmethod
    async def set(cls, key, value):
        random_uuid = uuid.uuid4().bytes
        await cls._instance.hset(random_uuid, mapping={'vector_field': key, 'text': value})
    

class VectorDatabase:
    _embedding_model = HuggingFaceEmbeddings(
        model_name='jhgan/ko-sbert-nli',
        model_kwargs={'device':'cpu'},
        encode_kwargs={'normalize_embeddings':True},
    )
    _vector_db = None

    @classmethod
    async def _initialize_vector_db(cls, documents: List[Document]) -> None:
        cls._vector_db = await FAISS.afrom_documents(documents, cls._embedding_model)
        logger.debug("VectorDatabase Init Successed")

    @classmethod
    async def add_document(cls, documents: List[Document]) -> None:
        if cls._vector_db is None:
            await cls._initialize_vector_db(documents)
        else:
            await cls._vector_db.aadd_documents(documents)
            logger.debug("VectorDatabase add document success")
    
    @classmethod
    def get_retriever(cls, **kwargs):
        return cls._vector_db.as_retriever(**kwargs)