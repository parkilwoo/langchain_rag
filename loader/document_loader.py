from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader, JSONLoader, Docx2txtLoader
import mimetypes

class DocumentLoader:
    def __init__(self) -> None:
        self.document_loaders = {
            "application/pdf": PyPDFLoader,
            "text/csv": CSVLoader,
            "text/plain": TextLoader,
            "application/json": JSONLoader,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": Docx2txtLoader,
        }

    def __call__(self, file_path: str) -> str:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type not in self.document_loaders:
            raise ValueError(f"Unsupported mime type: {mime_type}")
        
        loader = self.document_loaders[mime_type](file_path)
        yield from loader.load()