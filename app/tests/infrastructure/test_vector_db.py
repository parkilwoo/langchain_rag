import pytest
from unittest.mock import patch, AsyncMock
from infrastructure.database import VectorDatabase
from langchain_core.documents import Document

@pytest.mark.asyncio
class TestVectorDatabase:

    @patch('infrastructure.database.FAISS.afrom_documents', new_callable=AsyncMock)
    async def test_initialize_vector_db(self, mock_afrom_documents):
        # Given
        documents = [Document()]
        mock_afrom_documents.return_value = "vector_db_instance"

        # When
        await VectorDatabase._initialize_vector_db(documents)

        # Then
        mock_afrom_documents.assert_awaited_once_with(documents, VectorDatabase._embedding_model)
        assert VectorDatabase._vector_db == "vector_db_instance"

    @patch('infrastructure.database.FAISS.aadd_documents', new_callable=AsyncMock)
    async def test_add_document_to_vector_db(self, mock_aadd_documents):
        # Given
        documents = [Document()]
        VectorDatabase._vector_db = AsyncMock()

        # When
        await VectorDatabase.add_document(documents)

        # Then
        mock_aadd_documents.assert_awaited_once_with(documents)

    def test_get_retriever(self):
        # Given
        VectorDatabase._vector_db = AsyncMock()

        # When
        retriever = VectorDatabase.get_retriever()

        # Then
        assert retriever == VectorDatabase._vector_db.as_retriever.return_value
