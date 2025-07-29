from ai.llm.openai_chat import CustomOpenAIChat
from ai.settings import ai_settings

def create_llm() -> CustomOpenAIChat:
    """Create and configure the LLM instance"""
    return CustomOpenAIChat(
        model=ai_settings.openai_chat_model,
        api_key=ai_settings.openai_api_key,
        base_url=ai_settings.openai_base_url
    ) 