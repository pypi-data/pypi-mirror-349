"""Database factory for LYRAIOS application"""

from typing import Optional
from app.db.storage import AssistantStorage

def get_storage() -> Optional[AssistantStorage]:
    """Get storage implementation"""
    try:
        return AssistantStorage()
    except Exception as e:
        print(f"Error creating storage: {e}")
        return None 