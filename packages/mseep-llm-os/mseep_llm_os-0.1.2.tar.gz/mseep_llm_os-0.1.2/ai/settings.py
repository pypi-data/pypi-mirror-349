from typing import Optional
from pydantic_settings import BaseSettings

class AISettings(BaseSettings):
    """Lyraios settings that can be set using environment variables.

    Reference: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    # OpenAI Model settings
    openai_chat_model: str = "gpt-4-turbo-preview"
    openai_vision_model: str = "gpt-4-vision-preview"
    openai_embedding_model: str = "text-embedding-3-small"
    
    # OpenAI API settings
    openai_api_key: str
    openai_base_url: Optional[str] = "https://api.openai.com/v1"
    
    # Default parameters
    default_max_tokens: int = 4096
    default_temperature: float = 0

    # External API Keys
    exa_api_key: Optional[str] = None
    google_api_key: Optional[str] = None

    # Server Configuration
    streamlit_server_port: Optional[int] = 8501
    api_server_port: Optional[int] = 8000

    class Config:
        env_file = ".env"
        env_prefix = ""
        extra = "ignore"


# Create AISettings object
ai_settings = AISettings()
