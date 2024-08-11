from abc import ABC, abstractmethod
import hashlib
# from redis import StrictRedis
# from langchain.memory import ConversationBufferMemory

# class RedisUserConversationManager:
#     _client = None
    
#     def __init__(self, host: str, port: int, db: int = 0) -> None:
#         self._client = StrictRedis(host=host, port=port, db=db)
    
#     @classmethod
#     def get_user_memory(cls, hash_value: str) -> ConversationBufferMemory:
#         cache_value = cls._client.get(hash_value)

class BaseConnector(ABC):
    
    @abstractmethod
    def test_connection(self) -> bool:
        """_summary_
        Test API Connection
        Returns:
            bool: _description_
        """
    
    def _generate_hash(self, **kwargs) -> str:
        """_summary_
        Connector 입력 정보를 이용해서 hash값 만드는 Method
        Returns:
            str: _description_
        """
        combined = ":".join(kwargs.values)
        return hashlib.sha256(combined.encode()).hexdigest()