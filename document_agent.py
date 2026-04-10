from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.core.config import settings

DOCUMENT_AGENT_PROMPT = """You are the NyayaMitra Document Analysis Agent.
You will be provided with the extracted text from a user's uploaded document (e.g., a Legal Notice, Contract, or Tax Form).
Your job is to answer the user's question based strictly on the provided document text.
If the answer is not in the text, clearly state that you cannot find the answer in the provided document.

--- Document Text Start ---
{document_context}
--- Document Text End ---

User Question: {query}
Answer:"""

class DocumentAgent:
    """Answers queries specifically context-bound to a user's uploaded document."""
    
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile", # Good for longer documents
            temperature=0
        )
        self.prompt = PromptTemplate.from_template(DOCUMENT_AGENT_PROMPT)
        self.chain = self.prompt | self.llm | StrOutputParser()
        
    def invoke(self, query: str, document_context: str) -> str:
        """Process queries against specific document content."""
        if not document_context:
            return "No document context was provided. Please upload a document to analyze."
            
        try:
            return self.chain.invoke({
                "query": query,
                "document_context": document_context
            })
        except Exception as e:
            return f"Error executing Document Agent: {str(e)}"
