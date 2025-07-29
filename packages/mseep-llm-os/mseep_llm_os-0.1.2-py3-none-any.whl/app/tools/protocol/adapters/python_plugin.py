"""
Tool Integration Protocol - Python Plugin Adapter

This module implements the Python Plugin adapter for the Tool Integration Protocol.
"""

import asyncio
import importlib.util
import inspect
import logging
import os
import sys
from typing import Any, Callable, Dict, Optional

from app.tools.protocol.adapters.base import ToolAdapter
from app.tools.protocol.models import ToolManifest, ValidationResult

logger = logging.getLogger(__name__)


class PythonPluginAdapter(ToolAdapter):
    """
    Adapter for Python plugin tools.
    
    This adapter allows integration with Python modules as tools.
    """
    
    def __init__(self, manifest: ToolManifest):
        """
        Initialize the Python Plugin adapter.
        
        Args:
            manifest: Tool manifest
        """
        super().__init__(manifest)
        self.plugin_path = None
        self.plugin_module = None
        self.sandbox_enabled = True
        self.functions = {}
    
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """
        Initialize the adapter with configuration.
        
        Args:
            config: Adapter configuration
            
        Returns:
            True if initialization succeeded, False otherwise
        """
        try:
            # Extract configuration
            self.plugin_path = config.get("plugin_path")
            if not self.plugin_path:
                logger.error("plugin_path is required for Python Plugin adapter")
                return False
            
            self.sandbox_enabled = config.get("sandbox_enabled", True)
            
            # Load plugin
            if self.sandbox_enabled:
                # Use sandbox to load plugin
                self.plugin_module = await self._load_sandboxed_plugin(self.plugin_path)
            else:
                # Load plugin directly
                self.plugin_module = self._load_plugin(self.plugin_path)
            
            if not self.plugin_module:
                logger.error(f"Failed to load plugin: {self.plugin_path}")
                return False
            
            # Load functions
            for capability in self.manifest.capabilities:
                func_name = capability.capability_id
                if not hasattr(self.plugin_module, func_name):
                    logger.error(f"Function not found in plugin: {func_name}")
                    return False
                
                self.functions[func_name] = getattr(self.plugin_module, func_name)
            
            logger.info(f"Python Plugin adapter initialized successfully: {self.plugin_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Python Plugin adapter: {str(e)}")
            return False
    
    def _load_plugin(self, path: str) -> Any:
        """
        Load a Python module from a file path.
        
        Args:
            path: Path to the Python file
            
        Returns:
            Loaded module
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Plugin file not found: {path}")
        
        # Get module name from file path
        module_name = os.path.basename(path)
        if module_name.endswith(".py"):
            module_name = module_name[:-3]
        
        # Load module
        spec = importlib.util.spec_from_file_location(module_name, path)
        if not spec or not spec.loader:
            raise ImportError(f"Failed to load plugin: {path}")
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        return module
    
    async def _load_sandboxed_plugin(self, path: str) -> Any:
        """
        Load a Python module in a sandbox.
        
        Args:
            path: Path to the Python file
            
        Returns:
            Loaded module
        """
        # For now, just use the regular loader
        # In a real implementation, this would use a sandbox like RestrictedPython
        return self._load_plugin(path)
    
    async def validate(self) -> ValidationResult:
        """
        Validate the tool implementation.
        
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        # Check if plugin is loaded
        if not self.plugin_module:
            errors.append("Python Plugin not loaded")
            return ValidationResult(is_valid=False, errors=errors)
        
        # Check capabilities
        for capability in self.manifest.capabilities:
            func_name = capability.capability_id
            
            # Check if function exists
            if not hasattr(self.plugin_module, func_name):
                errors.append(f"Function not found in plugin: {func_name}")
                continue
            
            # Get function
            func = getattr(self.plugin_module, func_name)
            
            # Check if it's callable
            if not callable(func):
                errors.append(f"Not a function: {func_name}")
                continue
            
            # Check function signature
            sig = inspect.signature(func)
            if len(sig.parameters) < 1:
                errors.append(f"Function {func_name} must accept at least one parameter (parameters)")
        
        # Check for initialize and shutdown functions
        if hasattr(self.plugin_module, "initialize") and not callable(getattr(self.plugin_module, "initialize")):
            errors.append("initialize must be a function")
        
        if hasattr(self.plugin_module, "shutdown") and not callable(getattr(self.plugin_module, "shutdown")):
            errors.append("shutdown must be a function")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
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
        # Check if plugin is loaded
        if not self.plugin_module:
            raise RuntimeError("Python Plugin not loaded")
        
        # Get function
        func = self.functions.get(capability_id)
        if not func:
            raise ValueError(f"Function not found: {capability_id}")
        
        # Execute function
        try:
            # Check if function is async
            if asyncio.iscoroutinefunction(func):
                result = await func(parameters, context)
            else:
                result = func(parameters, context)
            
            # Ensure result is a dictionary
            if not isinstance(result, dict):
                result = {"result": result}
            
            return result
        except Exception as e:
            logger.error(f"Error executing capability {capability_id}: {str(e)}")
            raise RuntimeError(f"Execution error: {str(e)}")
    
    async def shutdown(self) -> None:
        """
        Shutdown the adapter and release resources.
        """
        if self.plugin_module and hasattr(self.plugin_module, "shutdown"):
            try:
                shutdown_func = getattr(self.plugin_module, "shutdown")
                if asyncio.iscoroutinefunction(shutdown_func):
                    await shutdown_func()
                else:
                    shutdown_func()
            except Exception as e:
                logger.error(f"Error shutting down plugin: {str(e)}")
        
        self.plugin_module = None
        self.functions = {}
        logger.info("Python Plugin adapter shut down") 