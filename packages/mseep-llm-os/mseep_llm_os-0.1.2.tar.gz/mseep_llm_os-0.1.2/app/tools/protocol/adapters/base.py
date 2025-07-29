"""
Tool Integration Protocol - Base Adapter

This module defines the base adapter interface for the Tool Integration Protocol.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from app.tools.protocol.models import ToolManifest, ValidationResult


class ToolAdapter(ABC):
    """
    Base class for tool adapters.
    
    Tool adapters provide a unified interface for different types of tools.
    """
    
    def __init__(self, manifest: ToolManifest):
        """
        Initialize the adapter.
        
        Args:
            manifest: Tool manifest
        """
        self.manifest = manifest
    
    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """
        Initialize the adapter with configuration.
        
        Args:
            config: Adapter configuration
            
        Returns:
            True if initialization succeeded, False otherwise
        """
        pass
    
    @abstractmethod
    async def validate(self) -> ValidationResult:
        """
        Validate the tool implementation.
        
        Returns:
            Validation result
        """
        pass
    
    @abstractmethod
    async def execute(
        self,
        capability_id: str,
        parameters: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool capability.
        
        Args:
            capability_id: Capability ID
            parameters: Input parameters
            context: Execution context
            
        Returns:
            Execution result
        """
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """
        Shutdown the adapter and release resources.
        """
        pass 