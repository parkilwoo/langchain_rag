
from fastapi import APIRouter

from app.domain.user.services import UserService
from app.api.model.user import UserLoginRequest

router = APIRouter()


@router.post("/login", summary="api_key와 사용할 모델명을 입력 받아 인증된 token을 발급합니다.")
async def login_user(user_login: UserLoginRequest):
    token = await UserService.generate_access_token(user_login.api_key, user_login.use_model_name)
    return {'access_token': token}