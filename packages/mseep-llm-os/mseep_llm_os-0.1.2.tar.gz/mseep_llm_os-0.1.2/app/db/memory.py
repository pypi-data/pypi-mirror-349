"""
In-memory database implementation for testing.
"""

import copy
from typing import Any, Dict, List, Optional

from app.db.base import Database


class MemoryDatabase(Database):
    """
    In-memory database implementation for testing.
    """
    
    def __init__(self):
        """Initialize the in-memory database."""
        self.tools: Dict[str, Dict[str, Any]] = {}
    
    async def insert_tool(self, tool_data: Dict[str, Any]) -> None:
        """
        Insert a new tool.
        
        Args:
            tool_data: Tool data
        """
        tool_id = tool_data.get("tool_id")
        if not tool_id:
            raise ValueError("Tool ID is required")
        
        self.tools[tool_id] = copy.deepcopy(tool_data)
    
    async def update_tool(self, tool_id: str, tool_data: Dict[str, Any]) -> None:
        """
        Update an existing tool.
        
        Args:
            tool_id: Tool ID
            tool_data: Tool data
        """
        if tool_id not in self.tools:
            raise ValueError(f"Tool not found: {tool_id}")
        
        self.tools[tool_id].update(copy.deepcopy(tool_data))
    
    async def get_tool(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a tool by ID.
        
        Args:
            tool_id: Tool ID
            
        Returns:
            Tool data or None if not found
        """
        return copy.deepcopy(self.tools.get(tool_id))
    
    async def list_tools(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        List tools with optional filtering.
        
        Args:
            filters: Filters
            
        Returns:
            List of tools
        """
        result = []
        
        for tool_id, tool_data in self.tools.items():
            # Apply filters
            match = True
            for key, value in filters.items():
                if key not in tool_data or tool_data[key] != value:
                    match = False
                    break
            
            if match:
                result.append(copy.deepcopy(tool_data))
        
        return result
    
    async def delete_tool(self, tool_id: str) -> bool:
        """
        Delete a tool.
        
        Args:
            tool_id: Tool ID
            
        Returns:
            True if deleted, False if not found
        """
        if tool_id in self.tools:
            del self.tools[tool_id]
            return True
        return False 