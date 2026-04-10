from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.core.config import settings
from app.agents.prompts.prompts import RISK_AGENT_PROMPT
from app.agents.tools.rag_tools import search_legal_database, search_tax_database

class RiskAnalysisAgent:
    """Calculates risk levels and financial penalties based on user scenarios."""
    
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile",
            temperature=0
        )
        self.prompt = PromptTemplate.from_template(RISK_AGENT_PROMPT)
        self.chain = self.prompt | self.llm | StrOutputParser()
        
    def _gather_context(self, domain_hint: str, query: str) -> str:
        """Attempt to fetch some relevant laws before analyzing risk."""
        if domain_hint == "TAX":
            return search_tax_database.invoke({"query": query})
        elif domain_hint == "LEGAL":
            return search_legal_database.invoke({"query": query})
        else:
            return ""
            
    def invoke(self, query: str, domain_hint: str = "auto") -> str:
        """Analyze the scenario and output a formatted risk assessment."""
        context = self._gather_context(domain_hint, query)
        
        try:
            return self.chain.invoke({
                "query": query,
                "context": context
            })
        except Exception as e:
            return f"Error executing Risk Analysis Agent: {str(e)}"
