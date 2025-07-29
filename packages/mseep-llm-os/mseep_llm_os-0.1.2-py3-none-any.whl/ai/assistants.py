from textwrap import dedent
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

from phi.assistant import Assistant as PhiAssistant
from phi.assistant.python import PythonAssistant
from phi.embedder.openai import OpenAIEmbedder
from phi.knowledge import AssistantKnowledge
from phi.llm.openai import OpenAIChat
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.tools import Toolkit
from phi.tools.calculator import Calculator
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.exa import ExaTools
from phi.tools.file import FileTools
from phi.tools.yfinance import YFinanceTools
from phi.vectordb.pgvector import PgVector2

# Use SQLite storage
from app.db.sqlite_adapter import SQLiteAssistantAdapter
from app.config.ai_settings import model_settings
from workspace.settings import ws_settings
from ai.llm.factory import create_llm
from app.config.settings import app_settings


scratch_dir = ws_settings.ws_root.joinpath("scratch")
if not scratch_dir.exists():
    scratch_dir.mkdir(exist_ok=True, parents=True)

logger = logging.getLogger(__name__)

# Define LYRAIOS instructions
LYRAIOS_INSTRUCTIONS = [
    "You are the most advanced AI system in the world called `LYRAIOS`.",
    "When the user sends a message, first **think** and determine if:\n"
    " - You can answer by using a tool available to you\n"
    " - You need to search the knowledge base\n"
    " - You need to search the internet\n"
    " - You need to delegate the task to a team member\n"
    " - You need to ask a clarifying question",
    "If the user asks about a topic, first ALWAYS search your knowledge base using the `search_knowledge_base` tool.",
    "If you dont find relevant information in your knowledge base, use the `duckduckgo_search` tool to search the internet.",
    "If the user asks to summarize the conversation, use the `get_chat_history` tool with None as the argument.",
    "If the users message is unclear, ask clarifying questions to get more information.",
    "Carefully read the information you have gathered and provide a clear and concise answer to the user.",
    "Do not use phrases like 'based on my knowledge' or 'depending on the information'.",
    "You can delegate tasks to an AI Assistant in your team depending of their role and the tools available to them.",
]

class Assistant:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize AI assistant with configuration
        """
        self.config = config
        self.model = config.get("model_name")
        self.context = []
    
    async def process_message(self, message: str) -> str:
        """
        Process user message and return response
        """
        try:
            # Add message to context
            self.context.append({"role": "user", "content": message})
            
            # Process message here
            response = await self._generate_response()
            
            # Add response to context
            self.context.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise
    
    async def _generate_response(self) -> str:
        """
        Generate response based on context
        """
        # Implement actual response generation logic here
        pass

def get_lyraios(
    calculator: bool = False,
    ddg_search: bool = False,
    file_tools: bool = False,
    finance_tools: bool = False,
    python_assistant: bool = False,
    research_assistant: bool = False,
    run_id: Optional[str] = None,
    user_id: Optional[str] = None,
    debug_mode: bool = True,
    model: Optional[str] = None,
    temperature: float = 0.7,
    streaming: bool = True,
) -> PhiAssistant:
    """Get the LYRAIOS assistant"""
    try:
        # Use custom model or default from settings
        model = model or model_settings.get_default_model()
        
    # LLM to use for the Assistant
        llm = create_llm()
        
        # Tools to add to the Assistant
        tools = []
        
    # Extra instructions for using tools
        extra_instructions = []
        
        # Team members to add to the Assistant
        team = []
        
        # Add calculator tool
    if calculator:
            tools.append(Calculator())
            extra_instructions.append(
                "To perform calculations, use the `calculate` tool. "
                "For example, to calculate 2 + 2, use `calculate(2 + 2)`."
            )
        
        # Add DuckDuckGo search tool
    if ddg_search:
            tools.append(DuckDuckGo())
            extra_instructions.append(
                "To search the internet, use the `duckduckgo_search` tool. "
                "For example, to search for 'latest AI news', use `duckduckgo_search('latest AI news')`."
            )
        
        # Add file tools
        if file_tools:
            # Skip FileTools initialization
            logger.warning("FileTools is temporarily disabled")
            # But still add relevant instructions
            extra_instructions.append(
                "To work with files, use the `read_file`, `write_file`, and `list_files` tools."
            )
        
        # Add finance tools
        if finance_tools:
            tools.append(YFinanceTools())
        extra_instructions.append(
                "To get financial data, use the `get_stock_price`, `get_stock_history`, and `get_stock_info` tools."
        )

        # Add Python assistant to the team
    if python_assistant:
        _python_assistant = PythonAssistant(
            name="Python Assistant",
                description="A Python expert that can help with coding tasks.",
                instructions=[
                    "You are a Python expert that can help with coding tasks.",
                    "When asked to write code, provide well-documented, efficient, and correct Python code.",
                    "Always explain your code and provide examples of how to use it.",
                ],
                scratch_dir=scratch_dir,
                model=model,
                temperature=temperature,
                streaming=streaming,
        )
        team.append(_python_assistant)
        extra_instructions.append(
                "To get help with Python coding tasks, delegate the task to the `Python Assistant`."
        )
        
        # Add research assistant to the team
    if research_assistant:
            # Add Exa tools for research
            tools.append(ExaTools())
            extra_instructions.append(
                "To search for academic papers and research, use the `exa_search` tool."
            )
            
            _research_assistant = PhiAssistant(
            name="Research Assistant",
            instructions=[
                    "You are a research assistant that can help with finding and summarizing information.",
                    "When asked to research a topic, use the `exa_search` tool to find relevant information.",
                    "Provide comprehensive, well-structured reports with citations.",
                ],
                model=model,
                temperature=temperature,
                streaming=streaming,
        )
        team.append(_research_assistant)
        extra_instructions.append(
            "To write a research report, delegate the task to the `Research Assistant`. "
            "Return the report in the <report_format> to the user as is, without any additional text like 'here is the report'."
        )

        # Use SQLite storage
        try:
            # Initialize SQLite adapter
            storage = SQLiteAssistantAdapter()
            # Verify storage is available
            storage.get_all_run_ids()  # If storage is not available, this will raise an exception
        except Exception as e:
            logger.error(f"SQLite storage initialization error: {e}")
            # Use None as fallback
            logger.warning("Using no storage as fallback")
            storage = None
        
        # Create assistant instance
        assistant = PhiAssistant(
        llm=llm,
        name="LYRAIOS",
        run_id=run_id,
        user_id=user_id,
            storage=storage,
            instructions=LYRAIOS_INSTRUCTIONS,
        tools=tools,
        team=team,
        markdown=True,
        debug_mode=debug_mode,
    )
        
        return assistant
        
    except Exception as e:
        logger.error(f"Failed to create assistant: {e}")
        raise

# Ensure the function is exported correctly
__all__ = ['get_lyraios']
