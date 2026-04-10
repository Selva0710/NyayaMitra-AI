from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

from app.core.config import settings
from app.agents.prompts.prompts import LEGAL_AGENT_PROMPT, REACT_SYSTEM_PROMPT
from app.agents.tools.rag_tools import search_legal_database

class LegalAgent:
    """
    Agent that specializes in Indian Law.
    Uses a ReAct prompt to Think -> Search KB -> Output Answer.
    """
    
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile", # Stronger reasoning for legal text
            temperature=0.1 # Keep it factual
        )
        
        # Tools this agent is allowed to use
        self.tools = [search_legal_database]
        
        # Build the full prompt
        full_prompt_text = LEGAL_AGENT_PROMPT.format(react_base=REACT_SYSTEM_PROMPT) + "\n\nUser Request: {input}\n{agent_scratchpad}"
        self.prompt = PromptTemplate.from_template(full_prompt_text)
        
        # Create the underlying generic ReAct agent
        agent = create_react_agent(self.llm, self.tools, self.prompt)
        
        # The Executor handles the parsing of the Thought/Action/Observation loop
        self.agent_executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            verbose=True, 
            handle_parsing_errors=True
        )
        
    def invoke(self, query: str) -> str:
        """Process the legal query constraints."""
        try:
            response = self.agent_executor.invoke({"input": query})
            return response.get("output", "I could not formulate a complete legal response.")
        except Exception as e:
            return f"Error executing Legal Agent: {str(e)}"
