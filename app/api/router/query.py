
from fastapi import APIRouter

from domain.query.services import QueryService

router = APIRouter()


@router.post("/conversation", summary="발급된 token와 질문할 input을 입력받아 RAG를 통해서 응답합니다.")
async def conversation(token: str, input: str):
    result = await QueryService.get_query_result(input, token)
    return {'input': input, 'result': result}