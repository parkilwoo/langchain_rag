from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class BaseResponse(BaseModel):
    request_time: datetime
    response_time: datetime
    elapsed_time: datetime
    
class SuccessResponse(BaseResponse):
    result: Dict
    
class Error(BaseModel):
    error_code: str
    error_msg: str    

class ErrorReponse(BaseResponse):
    error: Error