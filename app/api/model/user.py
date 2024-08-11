from pydantic import BaseModel, Field

class UserLoginRequest(BaseModel):
    api_key: str = Field(..., description="발급받은 api key")
    model_name: str = Field(..., description="사용할 모델명")