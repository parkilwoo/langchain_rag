import os
from loader.document import DocumentLoader
from langchain_text_splitters import __all__ as text_splitters

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
    
    @property
    def docs(self):
        return self.document_loader.get_docs(self.splitter)