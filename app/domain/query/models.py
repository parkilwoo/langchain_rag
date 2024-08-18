from typing import Optional, Tuple, List
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from infrastructure.connector.base import BaseConnector
from domain.postprocessing.models import BasePostProcessing
from domain.prompter.models import ChatPrompt
from core.const import settings

class QueryInput:
    
    def __init__(self, input: str, postprcessing: Optional[BasePostProcessing], **kwargs) -> None:
        self.input = postprcessing.do_process(input, **kwargs) if postprcessing else input
    
    def get_input(self):
        return self.input
    
class Query:
    _OUTPUT_MESSAGE_KEY = 'answer'
    def __init__(self, query_input: QueryInput, connector: BaseConnector, key: str, retriever: Optional[VectorStoreRetriever]) -> None:
        self.query_input = query_input
        self.connector = connector.get_connector()
        self.key = key
        self.retriever = retriever
        self.rag_history_chain = None

    async def get_result(self) -> Tuple[str, List[str]]:
        
        if self.rag_history_chain is None:
            raise ConnectionError("Don't settings Rag chain")
        
        input_query = {ChatPrompt.INPUT_MESSAGE_KEY: self.query_input.get_input()}
        response = await self.rag_history_chain.ainvoke(input_query, config={"configurable": {"session_id": self.key}})
        if not response:
            raise ConnectionError("Connection failed")
        
        return response['answer']
        
    def setting_rag_chain(self) -> None:
        history_aware_retriever = create_history_aware_retriever(
            self.connector, self.retriever, ChatPrompt.get_contextualize_q_prompt()
        )
        question_answer_chain = create_stuff_documents_chain(self.connector, ChatPrompt.get_qa_prompt())
        rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )
        
        self.rag_history_chain = RunnableWithMessageHistory(
            rag_chain,
            lambda session_id: RedisChatMessageHistory(
                session_id, url=settings.HISTORY_REDIS_URL, ttl=settings.HISTORY_REIDS_TTL
            ),
            input_messages_key=ChatPrompt.INPUT_MESSAGE_KEY,
            history_messages_key=ChatPrompt.HISTORY_MESSAGE_KEY,
            output_messages_key=self._OUTPUT_MESSAGE_KEY
        )
                