from langchain_community.embeddings import HuggingFaceEmbeddings

class EmbeddingProvider:
    """Wrapper for generating embeddings using local SentenceTransformers."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initializes the embedding model.
        all-MiniLM-L6-v2 is fast and efficient for general text.
        For specifically Indian Legal text, custom models could be swapped here later.
        """
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'}, # Use 'cuda' or 'mps' if GPU is available
            encode_kwargs={'normalize_embeddings': True} # Better for cosine similarity
        )
        
    def get_embeddings(self) -> HuggingFaceEmbeddings:
        """Returns the initialized HuggingFaceEmbeddings object."""
        return self.embeddings
