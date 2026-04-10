import logging
from app.agents.router_agent import QueryRouter
from app.agents.legal_agent import LegalAgent
from app.agents.tax_agent import CAAgent
from app.agents.document_agent import DocumentAgent
from app.agents.draft_agent import DraftAgent
from app.agents.risk_agent import RiskAnalysisAgent

logger = logging.getLogger(__name__)

class AgentSupervisor:
    """
    The orchestrator that receives user requests, determines intent,
    and routes to the specialized ReAct agent.
    """
    
    def __init__(self):
        self.router = QueryRouter()
        self.legal_agent = LegalAgent()
        self.tax_agent = CAAgent()
        self.doc_agent = DocumentAgent()
        self.draft_agent = DraftAgent()
        self.risk_agent = RiskAnalysisAgent()
        
    def process_query(self, query: str, document_context: str = None) -> dict:
        """
        Main entry point for all queries.
        Returns a dict with the chosen route and the final response.
        """
        logger.info(f"Supervisor received query: {query}")
        
        # 1. If document context is explicitly provided and the user just wants answers from it
        if document_context and "DOCUMENT" in self.router.route_query(query):
            response = self.doc_agent.invoke(query, document_context)
            return {"route": "DOCUMENT", "response": response}
            
        # 2. Route the generic query
        route = self.router.route_query(query)
        logger.info(f"Query routed to: {route}")
        
        response = ""
        
        if route == "LEGAL":
            response = self.legal_agent.invoke(query)
            
        elif route == "TAX":
            response = self.tax_agent.invoke(query)
            
        elif route == "BOTH":
            # Pass to both and combine, or just use a generic agent
            # For now, pass to Legal first, then Tax
            req = f"Regarding this query: {query}\n"
            legal_ans = self.legal_agent.invoke(req + "Focus on the legal Indian Penal Code or Constitutional aspects.")
            tax_ans = self.tax_agent.invoke(req + "Focus on the GST, Income Tax, or CBDT financial aspects.")
            
            response = f"**⚖️ Legal Perspective:**\n{legal_ans}\n\n**📊 Tax/CA Perspective:**\n{tax_ans}"
            
        elif route == "DRAFT":
            response = self.draft_agent.invoke(query)
            
        elif route == "RISK":
            # The Risk agent uses an internal auto-router for hints
            hint = self.router.route_query(query + " Is this a tax risk or a criminal risk?")
            response = self.risk_agent.invoke(query, domain_hint="TAX" if "TAX" in hint else "LEGAL")
            
        else:
            # Fallback
            response = "I did not understand the intent. Please ask a specific Legal or Taxation question."
            
        return {
            "route": route,
            "response": response
        }
