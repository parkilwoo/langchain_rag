import aioredis
from domain.query.models import QueryInput
from domain.user.models import AccessToken
from infrastructure.connector.open_ai import OpenAiConnector

class QueryService:
    _query_repository = None

    @classmethod
    async def get_query_result(cls, input_query: str, access_token: str) -> str:
        # 1. token으로 OpenAI Connector 가져오기
        api_key, use_model_name = AccessToken.decrypt(access_token)
        connector = OpenAiConnector(api_key, use_model_name)

        # 2. input값을 영어로 번역
        translated_query = QueryInput(input_query).get_input()

        # 3. vector값 구하기
        