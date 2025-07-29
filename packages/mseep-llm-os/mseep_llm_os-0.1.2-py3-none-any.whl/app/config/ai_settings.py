"""AI model settings for LYRAIOS application"""

class ModelSettings:
    """Model settings class"""
    
    def __init__(self):
        self.openai_chat_model = "gpt-4o"
    
    def get_default_model(self):
        """Get default model name"""
        return self.openai_chat_model

# Create singleton instance
model_settings = ModelSettings() 