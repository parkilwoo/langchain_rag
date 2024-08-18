from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class BaseResponse(BaseModel):
    request_time: datetime
    response_time: datetime
    elapsed_time: float
    
class SuccessResponse(BaseResponse):
    result: Dict
    
class Error(BaseModel):
    error_code: int
    error_msg: str    

class ErrorResponse(BaseResponse):
    error: Error