import pickle
from typing import Optional
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationSummaryMemory
from langchain.chains.conversation.base import ConversationChain

from infrastructure.connector.base import BaseConnector

class RedisSavingConversationChain(ConversationChain):
    def __init__(self, connector: BaseConnector, conversation_memory: ConversationSummaryMemory, redis_key: str):
        self.conversation_memory = conversation_memory
        self.key = redis_key
        super().__init__(
            llm=connector,
            memory=self.conversation_memory,
            output_parser=StrOutputParser(),
        )

    def save_to_redis(self, serialized_history: bytes):
        # TODO Redis에 저장하는 로직 구현
        pass

    async def run(self, input: str):
        response = await super().ainvoke(input)
        serialized_history = pickle.dumps(self.conversation_memory)
        self.save_to_redis(serialized_history)
        return response

class QueryInput:
    def __init__(self, input: str) -> None:
        self.translate_input = self._translate(input)
    
    def _translate(self, text: str) -> str:
        # TODO 번역 로직 구현
        return text

    def get_input(self) -> str:
        return self.translate_input
class Query:

    def __init__(self, input: QueryInput, connector: BaseConnector, conversation_memory: Optional[ConversationSummaryMemory]) -> None:
        self.input = input
        self.connector = connector
        self.conversation_memory = conversation_memory

    async def get_result(self) -> str:
        conversation = RedisSavingConversationChain(
            connector=self.connector.get_connector(),
            conversation_memory=self.conversation_memory,
            redis_key="conversation_memory"
        )
        return await conversation.run(self.input)
        