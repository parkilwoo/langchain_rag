from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager


from app.core.exception_handler import CoreCustomException, core_exception_handler
from core.const import settings
from api.router import user
from core.logging_middleware import PureASGILoggingMiddleware

def generate_app() -> FastAPI:

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # TODO 스타트업
        yield
        # TODO 셧다운

    app = FastAPI(
        title=settings.SWAGGER_TITLE,
        version=settings.VERSION,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ADD_MIDDLEWARE
    app.add_middleware(GZipMiddleware, minimum_size=500)
    app.add_middleware(PureASGILoggingMiddleware)

    # ADD Exception Handler
    app.add_exception_handler(CoreCustomException, core_exception_handler)    

    # INCLUDE ROUTER
    app.include_router(user.router, tags=["User"], prefix=settings.API_VERSION, include_in_schema=True)

    return app
