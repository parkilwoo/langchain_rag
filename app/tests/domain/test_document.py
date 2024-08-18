import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from domain.document.models import DocumentExtractor, DocumentLoader
from domain.document.services import DocumentService
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

@pytest.mark.asyncio
class TestDocumentExtractor:

    @patch('domain.document.models.DocumentLoader')
    def test_document_extractor_initialization(self, MockDocumentLoader):
        # Given
        file_path = 'sample.pdf'
        
        # When
        extractor = DocumentExtractor(file_path)
        
        # Then
        MockDocumentLoader.assert_called_once_with()
        MockDocumentLoader().assert_called_once_with(file_path)
        assert extractor.splitter is None

    @patch('domain.document.models.DocumentLoader')
    def test_document_extractor_with_splitter(self, MockDocumentLoader):
        # Given
        file_path = 'sample.pdf'
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        # When
        extractor = DocumentExtractor(file_path, splitter)
        
        # Then
        MockDocumentLoader.assert_called_once_with()
        MockDocumentLoader().assert_called_once_with(file_path)
        assert extractor.splitter is not None
        
    def test_check_file(self):
        # Given
        invalid_file_path = 'non_existent.pdf'
        
        # When / Then
        with pytest.raises(AssertionError):
            DocumentExtractor(invalid_file_path)


@pytest.mark.asyncio
class TestDocumentLoader:

    def test_document_loader_initialization(self):
        # Given / When
        loader = DocumentLoader()
        
        # Then
        assert loader.loader is None
        
    def test_document_loader_call_valid_mime_type(self):
        # Given
        file_path = 'sample.pdf'
        
        # When
        loader = DocumentLoader()
        loader(file_path)
        
        # Then
        assert isinstance(loader.loader, MagicMock)

    def test_document_loader_call_invalid_mime_type(self):
        # Given
        file_path = 'sample.invalid'
        
        # When
        loader = DocumentLoader()
        
        # Then
        with pytest.raises(ValueError):
            loader(file_path)

    @patch.object(DocumentLoader, 'loader')
    def test_document_loader_get_docs_without_splitter(self, mock_loader):
        # Given
        mock_loader.load.return_value = ["doc1", "doc2"]
        loader = DocumentLoader()
        loader.loader = mock_loader
        
        # When
        docs = loader.get_docs()
        
        # Then
        mock_loader.load.assert_called_once()
        assert docs == ["doc1", "doc2"]

    @patch.object(DocumentLoader, 'loader')
    def test_document_loader_get_docs_with_splitter(self, mock_loader):
        # Given
        mock_loader.load_and_split.return_value = ["doc1", "doc2"]
        loader = DocumentLoader()
        loader.loader = mock_loader
        splitter = MagicMock()
        
        # When
        docs = loader.get_docs(splitter)
        
        # Then
        mock_loader.load_and_split.assert_called_once_with(splitter)
        assert docs == ["doc1", "doc2"]

@pytest.mark.asyncio
class TestDocumentService:

    @patch('domain.document.services.DocumentRepository.add', new_callable=AsyncMock)
    @patch('domain.document.services.DocumentExtractor')
    async def test_add_document_in_vector_store(self, MockDocumentExtractor, mock_add):
        # Given
        file_path = 'sample.pdf'
        mock_docs = [Document()]
        MockDocumentExtractor().get_docs.return_value = mock_docs
        
        # When
        await DocumentService.add_document_in_vector_store(file_path)
        
        # Then
        MockDocumentExtractor.assert_called_once_with(
            file_path,
            RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=200, encoding_name='cl100k_base')
        )
        MockDocumentExtractor().get_docs.assert_called_once_with()
        mock_add.assert_awaited_once_with(mock_docs)

