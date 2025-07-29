from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod

class BaseStorage(ABC):
    """Base storage interface"""
    
    @abstractmethod
    def save_run(
        self,
        run_id: str,
        messages: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None,
        assistant_name: Optional[str] = None,
    ) -> None:
        """Save a conversation run"""
        pass
    
    @abstractmethod
    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get a conversation run by ID"""
        pass
    
    @abstractmethod
    def delete_run(self, run_id: str) -> None:
        """Delete a conversation run"""
        pass
    
    @abstractmethod
    def get_all_runs(self) -> List[Dict[str, Any]]:
        """Get all conversation runs"""
        pass
    
    @abstractmethod
    def get_all_run_ids(self) -> List[str]:
        """Get all run IDs"""
        pass

class Database(ABC):
    """
    Abstract database interface.
    """
    
    @abstractmethod
    async def insert_tool(self, tool_data: Dict[str, Any]) -> None:
        """
        Insert a new tool.
        
        Args:
            tool_data: Tool data
        """
        pass
    
    @abstractmethod
    async def update_tool(self, tool_id: str, tool_data: Dict[str, Any]) -> None:
        """
        Update an existing tool.
        
        Args:
            tool_id: Tool ID
            tool_data: Tool data
        """
        pass
    
    @abstractmethod
    async def get_tool(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a tool by ID.
        
        Args:
            tool_id: Tool ID
            
        Returns:
            Tool data or None if not found
        """
        pass
    
    @abstractmethod
    async def list_tools(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        List tools with optional filtering.
        
        Args:
            filters: Filters
            
        Returns:
            List of tools
        """
        pass
    
    @abstractmethod
    async def delete_tool(self, tool_id: str) -> bool:
        """
        Delete a tool.
        
        Args:
            tool_id: Tool ID
            
        Returns:
            True if deleted, False if not found
        """
        pass 