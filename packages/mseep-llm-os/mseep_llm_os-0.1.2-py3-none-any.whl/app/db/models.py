"""Database models for LYRAIOS application"""

from datetime import datetime
from typing import Optional, Dict, Any

class ChatMessage:
    """Chat message model"""
    
    def __init__(self, content: str, timestamp: datetime, role: str = "user", metadata: Optional[Dict[str, Any]] = None):
        self.content = content
        self.timestamp = timestamp
        self.role = role
        self.metadata = metadata or {}
    
    def save(self):
        """Save message to database"""
        # This is a placeholder for actual database saving logic
        # In a real application, this would connect to a database
        print(f"Saving message: {self.content[:30]}...")
        return True
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "role": self.role,
            "metadata": self.metadata
        } 