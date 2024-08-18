import os
from langchain_text_splitters import __all__ as text_splitters
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader, JSONLoader, Docx2txtLoader
from langchain.document_loaders.base import BaseLoader
import mimetypes

class DocumentExtractor:
    
    def __init__(self, file_path: str, splitter = None) -> None:
        self._check_file(file_path)
        self.document_loader = DocumentLoader()
        self.document_loader(file_path)
        if splitter:
            self._validate_splitter(splitter)
        self.splitter = splitter
        
    def _check_file(self, file_path):
        assert os.path.isfile(file_path), f"{file_path} is Not Exsits"
        
    def _validate_splitter(self, splitter):
        spliter_cls_name = type(splitter).__name__
        assert spliter_cls_name in text_splitters, f"{spliter_cls_name} is Not valide splitter"
    
    def get_docs(self):
        return self.document_loader.get_docs(self.splitter)

class DocumentLoader:
    _document_loaders = {
        "application/pdf": PyPDFLoader,
        "text/csv": CSVLoader,
        "text/plain": TextLoader,
        "application/json": JSONLoader,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": Docx2txtLoader,
    }

    def __setattr__(self, name, value):
        if name == "_document_loaders":
            raise AttributeError(f"Cannot modify {name}")
        super().__setattr__(name, value)
            
    def __init__(self) -> None:
        self.loader = None

    def __call__(self, file_path: str) -> None:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type not in self._document_loaders:
            raise ValueError(f"Unsupported mime type: {mime_type}")

        self.loader: BaseLoader = self._document_loaders[mime_type](file_path)
    
    def get_docs(self, splitters=None):
        return self.loader.load_and_split(splitters) if splitters else self.loader.load()
        