import os
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.docstore.document import Document
import logging

logger = logging.getLogger(__name__)

class DocumentIngestor:
    """Handles loading various document types from a directory."""
    
    SUPPORTED_FORMATS = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".txt": TextLoader
    }

    @staticmethod
    def load_document(file_path: str) -> Optional[List[Document]]:
        """Loads a single document if the format is supported."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext in DocumentIngestor.SUPPORTED_FORMATS:
            loader_cls = DocumentIngestor.SUPPORTED_FORMATS[ext]
            try:
                loader = loader_cls(file_path)
                docs = loader.load()
                # Add metadata about source type
                for doc in docs:
                    doc.metadata["source_file"] = os.path.basename(file_path)
                return docs
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
                return None
        else:
            logger.warning(f"Unsupported file format: {ext} for file {file_path}")
            return None

    @staticmethod
    def load_directory(directory_path: str) -> List[Document]:
        """Loads all supported documents from a directory recursively."""
        all_documents = []
        if not os.path.exists(directory_path):
            logger.warning(f"Directory not found: {directory_path}")
            return all_documents

        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                docs = DocumentIngestor.load_document(file_path)
                if docs:
                    all_documents.extend(docs)
                    
        return all_documents
