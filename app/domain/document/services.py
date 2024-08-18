
from langchain_text_splitters import RecursiveCharacterTextSplitter
from domain.document.models import DocumentExtractor
from domain.document.repository import DocumentRepository


class DocumentService:
    _repository = DocumentRepository
    
    @classmethod
    async def add_document_in_vector_store(cls, file_path: str) -> None:
        document_extractor = DocumentExtractor(file_path, RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                                                                chunk_size=1000,
                                                                chunk_overlap=200,
                                                                encoding_name='cl100k_base'
                                                            ))
        docs = document_extractor.get_docs()
        await cls._repository.add(docs)
        
    