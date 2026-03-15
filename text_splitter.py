from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

class ChunkingManager:
    """Handles splitting large documents into smaller, context-aware chunks."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        # Using recursive splitting to respect paragraphs, then sentences, then words
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""],
            length_function=len,
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Splits a list of standard LangChain Document objects."""
        return self.text_splitter.split_documents(documents)
    
    def split_text(self, text: str) -> List[str]:
        """Splits a raw string of text."""
        return self.text_splitter.split_text(text)
