from pathlib import Path

# Base settings
BASE_DIR = Path(__file__).resolve().parent.parent

# AI settings
AI_MODEL_CONFIG = {
    "model_name": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1000
}

# API settings
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Application settings
DEBUG = True
ALLOWED_HOSTS = ["*"]

"""Application settings for LYRAIOS"""

class AppSettings:
    """Application settings class"""
    
    def __init__(self):
        self.app_name = "LYRAIOS"
        self.version = "1.0.0"
        self.debug = True
        self.chat_settings = {
            "max_history": 50,
            "stream_output": True
        }
    
    def get_all(self):
        """Get all settings as dict"""
        return {
            "app_name": self.app_name,
            "version": self.version,
            "debug": self.debug,
            "chat": self.chat_settings
        }

# Create singleton instance
app_settings = AppSettings()

# Chat settings for easy access
chat_settings = app_settings.chat_settings 