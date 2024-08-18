from typing import List
from langchain_core.documents import Document

from infrastructure.database import VectorDatabase

class DocumentRepository:
    _vector_db = VectorDatabase
    
    @classmethod
    async def add(cls, docs: List[Document]):
        await cls._vector_db.add_document(docs)
    
    @classmethod
    def get_retriever(cls, **kwargs):
        return cls._vector_db.get_retriever(**kwargs)    