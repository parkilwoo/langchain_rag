from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from typing import List

class VectorStore:
    _embedding_model = HuggingFaceEmbeddings(
        model_name='jhgan/ko-sbert-nli',
        model_kwargs={'device':'cpu', 'clean_up_tokenization_spaces': False},
        encode_kwargs={'normalize_embeddings':True},
    )

    @classmethod
    def _initialize_vector_store(cls, documents: List[Document]) -> None:
        cls._vector_store = FAISS.from_documents(documents, cls._embedding_model)

    @classmethod
    def add_document(cls, documents: List[Document]) -> None:
        if cls._vector_store is None:
            cls._initialize_vector_store(documents)
        else:
            cls._vector_store.add_documents(documents)
    
    @classmethod
    def get_retriever(cls, **kwargs):
        return cls._vector_store.as_retriever(**kwargs)
        # retriver = cls._vector_store.as_retriever(**kwargs)
        # return retriver.invoke(query)