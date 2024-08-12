import aioredis
from app.domain.query.models import QueryInput
from app.domain.user.models import AccessToken
from app.infrastructure.connector.open_ai import OpenAiConnector

class QueryService:
    _query_repository = None

    @classmethod
    async def get_query_result(cls, input_query: str, access_token: str) -> str:
        # 1. token으로 OpenAI Connector 가져오기
        api_key, use_model_name = AccessToken.decrypt(access_token)
        connector = OpenAiConnector(api_key, use_model_name)

        # 2. redis에서 이미 질문에 대한 답변이 있는지 확인
        input_query_vector = QueryInput(input_query).get_vector()