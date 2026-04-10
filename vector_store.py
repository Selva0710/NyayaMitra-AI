import os
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from app.rag.embeddings import EmbeddingProvider
import logging

logger = logging.getLogger(__name__)

class VectorStoreManager:
    """Manages the FAISS vector database for different knowledge bases."""
    
    def __init__(self, index_name: str, base_dir: str = "app/rag/data/faiss_index"):
        """
        Args:
            index_name: The namespace for the index (e.g., 'legal', 'tax')
            base_dir: Directory to save the FAISS indexes locally
        """
        self.index_name = index_name
        self.index_path = os.path.join(base_dir, index_name)
        self.embeddings = EmbeddingProvider().get_embeddings()
        self.vector_store: Optional[FAISS] = None
        
        # Auto-load if exists
        self.load_index()

    def create_index(self, documents: List[Document]) -> bool:
        """Create a new FAISS index from documents."""
        if not documents:
            logger.warning("No documents provided to create index.")
            return False
            
        try:
            logger.info(f"Creating FAISS index '{self.index_name}' with {len(documents)} document chunks...")
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
            self.save_index()
            return True
        except Exception as e:
            logger.error(f"Error creating index: {e}")
            return False

    def add_documents(self, documents: List[Document]) -> bool:
        """Add new documents to an existing index."""
        if not self.vector_store:
            return self.create_index(documents)
            
        try:
            logger.info(f"Adding {len(documents)} chunks to existing index '{self.index_name}'...")
            self.vector_store.add_documents(documents)
            self.save_index()
            return True
        except Exception as e:
            logger.error(f"Error adding documents to index: {e}")
            return False

    def save_index(self) -> None:
        """Persist the index to disk."""
        if self.vector_store:
            os.makedirs(self.index_path, exist_ok=True)
            self.vector_store.save_local(self.index_path)
            logger.info(f"Index '{self.index_name}' saved to {self.index_path}")

    def load_index(self) -> bool:
        """Load an existing index from disk."""
        if os.path.exists(os.path.join(self.index_path, "index.faiss")):
            try:
                self.vector_store = FAISS.load_local(
                    self.index_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True # Required by LangChain 0.1.0+ for local FAISS loads
                )
                logger.info(f"Loaded existing index '{self.index_name}'.")
                return True
            except Exception as e:
                logger.error(f"Error loading index '{self.index_name}': {e}")
                return False
        return False
        
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search the vector database for the most relevant chunks."""
        if not self.vector_store:
            logger.warning(f"Index '{self.index_name}' is not loaded. Cannot perform search.")
            return []
            
        return self.vector_store.similarity_search(query, k=k)
