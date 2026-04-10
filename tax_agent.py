from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

from app.core.config import settings
from app.agents.prompts.prompts import TAX_AGENT_PROMPT, REACT_SYSTEM_PROMPT
from app.agents.tools.rag_tools import search_tax_database, get_compliance_calendar

class CAAgent:
    """
    Agent that specializes in Indian Taxation and Compliances.
    """
    
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile",
            temperature=0.1
        )
        
        # Tax agent has access to tax laws and the active calendar
        self.tools = [search_tax_database, get_compliance_calendar]
        
        full_prompt_text = TAX_AGENT_PROMPT.format(react_base=REACT_SYSTEM_PROMPT) + "\n\nUser Request: {input}\n{agent_scratchpad}"
        self.prompt = PromptTemplate.from_template(full_prompt_text)
        
        agent = create_react_agent(self.llm, self.tools, self.prompt)
        
        self.agent_executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            verbose=True, 
            handle_parsing_errors=True
        )
        
    def invoke(self, query: str) -> str:
        """Process the tax query constraints."""
        try:
            response = self.agent_executor.invoke({"input": query})
            return response.get("output", "I could not formulate a complete tax response.")
        except Exception as e:
            return f"Error executing CA Agent: {str(e)}"
