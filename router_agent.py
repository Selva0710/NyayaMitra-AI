import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.core.config import settings
from app.agents.prompts.prompts import ROUTER_PROMPT

class QueryRouter:
    """
    A lightweight LLM chain to categorize the incoming query so the Supervisor
    knows which specialized agent to invoke.
    """
    
    def __init__(self):
        # We use a faster, cheaper model for routing like GPT-3.5-Turbo
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY, 
            model_name="llama-3.1-8b-instant", 
            temperature=0
        )
        
        prompt = PromptTemplate.from_template(ROUTER_PROMPT)
        
        # Build the chain using LCEL (LangChain Expression Language)
        self.chain = prompt | self.llm | StrOutputParser()
        
    def route_query(self, query: str) -> str:
        """
        Takes the user message and returns one of:
        LEGAL, TAX, BOTH, DOCUMENT, DRAFT, RISK
        """
        # If API key is missing (local dev), fallback to basic keyword matching
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY.startswith("sk-"):
            return self._fallback_routing(query)
            
        try:
            result = self.chain.invoke({"query": query})
            # Clean up potential whitespace or punctuation
            return result.strip().upper()
        except Exception as e:
            # Fallback if API fails
            print(f"Router error: {e}")
            return self._fallback_routing(query)
            
    def _fallback_routing(self, query: str) -> str:
        """Basic keyword routing if LLM is unavailable."""
        q = query.lower()
        if any(w in q for w in ["draft", "notice", "template", "write"]):
            return "DRAFT"
        if any(w in q for w in ["risk", "penalty", "chance", "probability"]):
            return "RISK"
        if any(w in q for w in ["tax", "gst", "itr", "audit", "ca "]):
            if any(w in q for w in ["court", "law", "ipc", "criminal"]):
                return "BOTH"
            return "TAX"
        return "LEGAL"
