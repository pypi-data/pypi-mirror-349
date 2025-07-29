"""
Tool Integration Protocol - Tool Executor

This module implements the Tool Execution Environment component of the Tool Integration Protocol.
"""

import asyncio
import logging
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Type

from app.tools.protocol.adapters.base import ToolAdapter
from app.tools.protocol.adapters.python_plugin import PythonPluginAdapter
from app.tools.protocol.adapters.rest_api import RestApiAdapter
from app.tools.protocol.models import ToolManifest, ValidationResult
from app.tools.protocol.registry import ToolRegistry

logger = logging.getLogger(__name__)


class ToolExecutionError(Exception):
    """Exception raised when tool execution fails."""
    pass


class ToolExecutor:
    """
    Tool Execution Environment manages tool execution.
    """
    
    def __init__(self, registry: ToolRegistry):
        """
        Initialize the Tool Executor.
        
        Args:
            registry: Tool Registry
        """
        self.registry = registry
        self.adapters: Dict[str, ToolAdapter] = {}
        self.adapter_classes: Dict[str, Type[ToolAdapter]] = {
            "rest_api": RestApiAdapter,
            "python_plugin": PythonPluginAdapter,
        }
    
    async def execute(
        self,
        tool_id: str,
        capability_id: str,
        parameters: Dict[str, Any],
        context: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a tool capability.
        
        Args:
            tool_id: Tool ID
            capability_id: Capability ID
            parameters: Input parameters
            context: Execution context
            user_id: User ID
            
        Returns:
            Execution result
        """
        execution_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            # Get tool
            tool_data = await self.registry.get_tool(tool_id)
            if not tool_data:
                raise ToolExecutionError(f"Tool not found: {tool_id}")
            
            # Get adapter
            adapter = await self._get_adapter(tool_id, tool_data)
            
            # Execute capability
            logger.info(f"Executing capability {capability_id} of tool {tool_id}")
            result = await adapter.execute(capability_id, parameters, context)
            
            # Log execution
            execution_time = time.time() - start_time
            await self._log_execution(
                execution_id=execution_id,
                tool_id=tool_id,
                capability_id=capability_id,
                user_id=user_id,
                parameters=parameters,
                result=result,
                error=None,
                execution_time=execution_time
            )
            
            return result
        except Exception as e:
            # Log execution error
            execution_time = time.time() - start_time
            await self._log_execution(
                execution_id=execution_id,
                tool_id=tool_id,
                capability_id=capability_id,
                user_id=user_id,
                parameters=parameters,
                result=None,
                error=str(e),
                execution_time=execution_time
            )
            
            logger.error(f"Error executing capability {capability_id} of tool {tool_id}: {str(e)}")
            raise ToolExecutionError(f"Execution error: {str(e)}")
    
    async def _get_adapter(self, tool_id: str, tool_data: Dict[str, Any]) -> ToolAdapter:
        """
        Get or create an adapter for a tool.
        
        Args:
            tool_id: Tool ID
            tool_data: Tool data
            
        Returns:
            Tool adapter
        """
        # Check if adapter already exists
        if tool_id in self.adapters:
            return self.adapters[tool_id]
        
        # Get implementation type
        implementation = tool_data.get("implementation", {})
        implementation_type = implementation.get("implementation_type")
        if not implementation_type:
            raise ToolExecutionError(f"Implementation type not specified for tool: {tool_id}")
        
        # Get adapter class
        adapter_class = self.adapter_classes.get(implementation_type)
        if not adapter_class:
            raise ToolExecutionError(f"Unsupported implementation type: {implementation_type}")
        
        # Create manifest
        manifest = ToolManifest(**tool_data.get("manifest", {}))
        
        # Create adapter
        adapter = adapter_class(manifest)
        
        # Initialize adapter
        config = implementation.get("config", {})
        initialized = await adapter.initialize(config)
        if not initialized:
            raise ToolExecutionError(f"Failed to initialize adapter for tool: {tool_id}")
        
        # Validate adapter
        validation = await adapter.validate()
        if not validation.is_valid:
            await adapter.shutdown()
            raise ToolExecutionError(f"Adapter validation failed: {validation.errors}")
        
        # Store adapter
        self.adapters[tool_id] = adapter
        
        return adapter
    
    async def _log_execution(
        self,
        execution_id: str,
        tool_id: str,
        capability_id: str,
        user_id: Optional[str],
        parameters: Dict[str, Any],
        result: Optional[Dict[str, Any]],
        error: Optional[str],
        execution_time: float
    ) -> None:
        """
        Log tool execution.
        
        Args:
            execution_id: Execution ID
            tool_id: Tool ID
            capability_id: Capability ID
            user_id: User ID
            parameters: Input parameters
            result: Execution result
            error: Error message
            execution_time: Execution time in seconds
        """
        # In a real implementation, this would log to a database
        log_entry = {
            "execution_id": execution_id,
            "tool_id": tool_id,
            "capability_id": capability_id,
            "user_id": user_id,
            "parameters": self._sanitize_parameters(parameters),
            "result": result,
            "error": error,
            "execution_time": execution_time,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Tool execution: {log_entry}")
    
    def _sanitize_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize parameters for logging.
        
        Args:
            parameters: Input parameters
            
        Returns:
            Sanitized parameters
        """
        # In a real implementation, this would remove sensitive data
        return parameters
    
    async def shutdown(self) -> None:
        """
        Shutdown the Tool Executor and release resources.
        """
        for tool_id, adapter in self.adapters.items():
            try:
                await adapter.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down adapter for tool {tool_id}: {str(e)}")
        
        self.adapters = {}
        logger.info("Tool Executor shut down") 