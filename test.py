from extractor.document import DocumentExtractor
from langchain_text_splitters.character import RecursiveCharacterTextSplitter

document_extractor = DocumentExtractor("./test.pdf", RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200))
docs = document_extractor.docs

from store.vector import VectorStore
VectorStore.add_document(docs)

search_kwargs = {
    'search_type': "similarity_score_threshold",
    'search_kwargs': {"score_threshold": 0.5}
}

print(VectorStore.search("개인신용정보 전송은 어떻게 진행이 돼?", **search_kwargs))

