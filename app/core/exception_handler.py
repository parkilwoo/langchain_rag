import traceback
from fastapi.encoders import jsonable_encoder
from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime

from api.model.base import ErrorResponse, Error
from core.custom_logger import logger
from shared.utils import Utils

class CoreCustomException(Exception):
    def __init__(self, error_code: int, error_msg: str = None):
        self.error_code = error_code
        self.error_msg = error_msg
    


def core_exception_handler(request: Request, cce: CoreCustomException) -> JSONResponse:
    response_time = datetime.now()
    traceback.print_exc(limit=-1)
    logger.error(
        'ERROR_CODE::{} ERROR_MESSAGE::{}',
        cce.error_code,
        cce.error_msg
    )

    error_obj = Error(
        code=cce.error_code,
        message=cce.error_msg
    )

    error_resp_obj = ErrorResponse(
        request_time=request.state.req_time,
        response_time=response_time,
        elapsed_time=Utils.cal_time_elapsed_seconds(request.state.req_time, response_time),
        error=error_obj
    )    

    return JSONResponse(
        status_code=cce.error_code,
        content=jsonable_encoder(error_resp_obj)
    )
