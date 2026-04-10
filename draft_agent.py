from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.core.config import settings
from app.agents.prompts.prompts import DRAFT_AGENT_PROMPT

class DraftAgent:
    """Generates legal notices, tax replies, or consumer complaints."""
    
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile", # Drafting needs high-quality formatting
            temperature=0.4 # A bit more creative for formatting
        )
        self.prompt = PromptTemplate.from_template(DRAFT_AGENT_PROMPT)
        self.chain = self.prompt | self.llm | StrOutputParser()
        
    def invoke(self, query: str, context: str = "") -> str:
        """Generate a draft based on user constraints and optional retrieved context."""
        try:
            return self.chain.invoke({
                "query": query,
                "context": context if context else "No additional prior knowledge provided. Rely on standard formats."
            })
        except Exception as e:
            return f"Error executing Draft Agent: {str(e)}"
