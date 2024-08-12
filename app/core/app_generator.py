from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.const import settings
from app.api.router import user

def generate_app() -> FastAPI:

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
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # INCLUDE ROUTER
    app.include_router(user.router, tags=["User"], prefix=settings.API_VERSION, include_in_schema=True)

    @app.on_event("startup")
    def startup_event():
        pass

    return app
