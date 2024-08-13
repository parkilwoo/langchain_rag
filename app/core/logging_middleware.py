import os

from datetime import datetime
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send, Message
from starlette.datastructures import Headers
from starlette.responses import JSONResponse as starlette_JSONResponse
from fastapi.encoders import jsonable_encoder

from core.custom_logger import logger
from api.model.base import ErrorResponse, Error
from shared.utils import Utils

class PureASGILoggingMiddleware:

    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        # Wokrer마다 PID와 PPID를 가져와서 로깅에 사용
        self.PID = os.getpid()
        self.PPID = os.getppid()        

    def log_send(self, request: Request, response: dict):
        response_headers = Headers(raw=response["headers"])
        response_time = datetime.now()
        elapsed_time = Utils.cal_time_elapsed_seconds(request.state.req_time, response_time)
        logger.info(
            "[PPID::{}] [PID::{}] [REQ_ID::{}] (ip::{}, method::{}, path::{}, status::{}, length::{}) (Req::{}, Res::{}, Dur::{})", 
            self.PPID,
            self.PID,
            request.state.req_id,
            request.state.ip,
            request.method,
            request.url.path,
            response['status'],
            response_headers.get('content-length', 0),
            request.state.req_time,
            response_time,
            elapsed_time
        )

    def log_receive(self, request: Request):
        """_summary_
        요청에 관한 Logging
        Args:
            request (Request): _description_
        """
        logger.info(
            "[PPID::{}] [PID::{}] [REQ_ID::{}] (ip::{}, method::{}, path::{}) (Req::{})",
            self.PPID,
            self.PID,
            request.state.req_id,
            request.state.ip,
            request.method,
            request.url.path,
            request.state.req_time
        )
        
        # Header 정보 Debug logging
        logger.debug(
            "[PPID::{}] [PID::{}] (headers::{})",
            self.PPID,
            self.PID,
            request.scope.get("headers") or "This request has no headers"
        )
    
    def get_request(self, scope: Scope, receive: Receive) -> Request:

        request = Request(scope, receive=receive)
        headers = request.headers
        request.state.req_id = str(id(request))

        request.state.req_time = datetime.now()

        request.state.x_real_ip = (
            headers["x-real-ip"] if "x-real-ip" in request.headers else None
        )
        request.state.x_forwarded_for = (
            headers["x-forwarded-ip"] if "x-forwarded-ip" in request.headers else None
        )        

        if request.state.x_real_ip:
            request.state.ip = request.state.x_real_ip

        elif request.state.x_forwarded_for:
            request.state.ip = request.state.x_forwarded_for.split(",")[0]

        else:
            request.state.ip = request.client.host

        return request

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        # http 요청에 대해서만 미들웨어 적용. (http, websocket, lifespan)
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # 받은 요청 로깅
        request = self.get_request(scope, receive)
        self.log_receive(request)

        response = dict()
        async def send_wrapper(message: Message):
            nonlocal response

            if message["type"] == "http.response.start":  # 먼저 호출됨
                response["status"] = message["status"]
                response["headers"] = message["headers"]

            elif message["type"] == "http.response.body":
                response["body"] = message["body"]

            await send(message)        

        try:
            # 클라이언트에게 응답하는 부분
            await self.app(scope, receive, send_wrapper)

        except Exception as exc:
            response_time = datetime.now()
            error_obj = Error(error_code="500", error_msg="Internal Server Error")
            error_resp_obj = ErrorResponse(
                request_time=request.state.req_time,
                response_time=response_time,
                elapsed_time=Utils.cal_time_elapsed_seconds(request.state.req_time, response_time),
                error=error_obj
            )
            error_response = starlette_JSONResponse(
                status_code=500,
                content=jsonable_encoder(error_resp_obj),
            )
            await error_response(scope, receive, send_wrapper)

            logger.exception(exc)

        finally:
            self.log_send(request, response)