
from fastapi import APIRouter

from domain.user.services import UserService
from api.model.user import UserLoginRequest

router = APIRouter()


@router.post("/login", summary="api_key와 사용할 모델명을 입력 받아 인증된 token을 발급합니다.")
async def login_user(user_login: UserLoginRequest):
    token = await UserService.generate_access_token(user_login.api_key, user_login.use_model_name)
    return {'access_token': token}

@router.post("/login/ilwoo", summary="api_key와 사용할 모델명을 입력 받아 인증된 token을 발급합니다.")
async def get_token_ilwoo():
    token = await UserService.generate_access_token('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', 'gpt-4o-2024-08-06')
    return {'access_token': token}