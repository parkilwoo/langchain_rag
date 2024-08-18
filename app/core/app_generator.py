from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

from infrastructure.celery_client import CeleryClient
from domain.document.models import DocumentExtractor
from infrastructure.database import VectorDatabase, VectorRedisClient
from core.exception_handler import CustomException, core_exception_handler
from core.const import settings
from api.router import user, query
from core.logging_middleware import PureASGILoggingMiddleware
from core.custom_logger import logger

def generate_app() -> FastAPI:
    
    def get_static_files():
        files = []
        for root, _, filenames in os.walk("app/static"):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                files.append(full_path)
        return files    

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        files = get_static_files()
        print(files)
        for file in files:
            logger.debug("{} vector db insert start", file)
            document_extractor = DocumentExtractor(file, RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                                                                    chunk_size=1000,
                                                                    chunk_overlap=200,
                                                                    encoding_name='cl100k_base'
                                                                ))
            
            await VectorDatabase.add_document(document_extractor.get_docs())
        VectorRedisClient(url=settings.INDEX_SEARCH_REDIS_URL, ttl=settings.INDEX_SEARCH_REDIS_TTL)
        await VectorRedisClient.generate_index(reset=True)
        CeleryClient.connect(settings.CELERY_BROKER_URL, settings.CELERY_BROKER_BACKEND)
        yield
        # TODO 셧다운

    app = FastAPI(
        title=settings.SWAGGER_TITLE,
        version=settings.VERSION,
        lifespan=lifespan
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
    app.add_exception_handler(CustomException, core_exception_handler)    

    # INCLUDE ROUTER
    app.include_router(user.router, tags=["User"], prefix=settings.API_VERSION, include_in_schema=True)
    app.include_router(query.router, tags=["Query"], prefix=settings.API_VERSION, include_in_schema=True)

    return app
