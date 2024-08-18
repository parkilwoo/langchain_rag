from domain.query.repository import QueryRepository
from domain.document.repository import DocumentRepository
from domain.query.models import QueryInput, Query
from domain.user.models import AccessToken
from infrastructure.connector.open_ai import OpenAiConnector
from domain.postprocessing.models import TranslatePostProcessing

class QueryService:
    _document_repository = DocumentRepository
    _query_repository = QueryRepository
        
    @classmethod
    async def get_query_result(cls, input_query: str, access_token: str) -> str:
        # 1. token으로 OpenAI Connector 가져오기
        api_key, use_model_name = AccessToken.decrypt(access_token)
        connector = OpenAiConnector(api_key, use_model_name)
        
        # 2. input값을 영어로 번역
        translated_query = QueryInput(input_query, TranslatePostProcessing, lang=1)
        
        # 3. cache 체크
        # vector_value = cls._query_repository.get_vector(translated_query.get_input())
        
        # cache_response = await cls._query_repository.get_cache(vector_value)
        # if cache_response:
        #     logger.debug("'{}' Cache hit!", input_query)
        #     return cache_response
        # logger.debug("'{}' Cahce miss.", input_query)        
        
        # 4. retreivcer 가져오기
        document_retriver = DocumentRepository.get_retriever(search_kwargs={'k': 1})
        
        # 5. gpt에 보내기
        query_obj = Query(translated_query, connector, api_key, document_retriver)
        query_obj.setting_rag_chain()
        result_text = await query_obj.get_result()
        
        # 6. cache settings
        # await cls._query_repository.set_cache(vector_bytes=vector_value, query_result=result_text)
        return result_text