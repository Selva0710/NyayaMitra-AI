from typing import List, Dict, Any
from langchain.docstore.document import Document
from app.rag.vector_store import VectorStoreManager

class RetrieverModule:
    """High-level interface for fetching context across multiple knowledge bases."""
    
    def __init__(self):
        # Initialize connections to both persistent databases
        self.legal_db = VectorStoreManager(index_name="legal")
        self.tax_db = VectorStoreManager(index_name="tax")
        
    def retrieve_context(self, query: str, domain: str = "auto", top_k: int = 5) -> str:
        """
        Fetch relevant chunks based on domain.
        Args:
            query: The user's question.
            domain: "legal", "tax", or "auto" to search both.
        Returns:
            A formatted string of context ready for the LLM.
        """
        documents: List[Document] = []
        
        if domain in ["legal", "auto"]:
            docs = self.legal_db.similarity_search(query, k=top_k)
            documents.extend(docs)
            
        if domain in ["tax", "auto"]:
            # If auto, we might want fewer from each to not overwhelm the context window
            docs = self.tax_db.similarity_search(query, k=top_k if domain == "tax" else top_k // 2)
            documents.extend(docs)
            
        if not documents:
            return "No relevant context found in the database."
            
        # Format the context for the LLM prompt
        formatted_context = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get("source_file", "Unknown Document")
            domain_label = "LEGAL" if "legal" in source.lower() else "TAX" if "tax" in source.lower() else "GENERAL"
            formatted_context.append(f"--- [Source {i}: {source} | Domain: {domain_label}] ---\n{doc.page_content}\n")
            
        return "\n".join(formatted_context)
