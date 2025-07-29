"""
Tool Integration Protocol - REST API Adapter

This module implements the REST API adapter for the Tool Integration Protocol.
"""

import logging
from typing import Any, Dict, Optional

import httpx

from app.tools.protocol.adapters.base import ToolAdapter
from app.tools.protocol.models import ToolManifest, ValidationResult

logger = logging.getLogger(__name__)


class RestApiAdapter(ToolAdapter):
    """
    Adapter for REST API tools.
    
    This adapter allows integration with external REST APIs.
    """
    
    def __init__(self, manifest: ToolManifest):
        """
        Initialize the REST API adapter.
        
        Args:
            manifest: Tool manifest
        """
        super().__init__(manifest)
        self.base_url = None
        self.headers = {}
        self.timeout = 30
        self.client = None
    
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
            self.base_url = config.get("base_url")
            if not self.base_url:
                logger.error("base_url is required for REST API adapter")
                return False
            
            self.headers = config.get("headers", {})
            self.timeout = config.get("timeout", 30)
            
            # Initialize HTTP client
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.headers,
                timeout=self.timeout
            )
            
            # Test connection
            test_url = config.get("test_url", "/")
            response = await self.client.get(test_url)
            response.raise_for_status()
            
            logger.info(f"REST API adapter initialized successfully: {self.base_url}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize REST API adapter: {str(e)}")
            return False
    
    async def validate(self) -> ValidationResult:
        """
        Validate the tool implementation.
        
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        # Check if client is initialized
        if not self.client:
            errors.append("REST API adapter not initialized")
            return ValidationResult(is_valid=False, errors=errors)
        
        # Check authentication
        auth = self.manifest.authentication
        if auth.type != "none" and not auth.name:
            errors.append("Authentication name is required for REST API tools")
        
        # Check capabilities
        for capability in self.manifest.capabilities:
            # Check if endpoint is specified in metadata
            endpoint = capability.metadata.get("endpoint")
            if not endpoint:
                errors.append(f"Capability {capability.capability_id} must specify endpoint in metadata")
            
            # Check if method is specified in metadata
            method = capability.metadata.get("method")
            if not method:
                warnings.append(f"Capability {capability.capability_id} should specify HTTP method in metadata")
        
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
        # Check if client is initialized
        if not self.client:
            raise RuntimeError("REST API adapter not initialized")
        
        # Find capability
        capability = None
        for cap in self.manifest.capabilities:
            if cap.capability_id == capability_id:
                capability = cap
                break
        
        if not capability:
            raise ValueError(f"Capability not found: {capability_id}")
        
        # Get endpoint and method from metadata
        endpoint = capability.metadata.get("endpoint")
        if not endpoint:
            raise ValueError(f"Endpoint not specified for capability: {capability_id}")
        
        method = capability.metadata.get("method", "POST").upper()
        
        # Prepare request
        headers = {}
        
        # Add authentication if required
        auth = self.manifest.authentication
        if auth.type != "none" and auth.required:
            auth_value = context.get("auth", {}).get(auth.name)
            if not auth_value:
                raise ValueError(f"Authentication required: {auth.name}")
            
            if auth.location == "header":
                headers[auth.name] = auth_value
            elif auth.location == "query":
                # Add to query parameters
                parameters[auth.name] = auth_value
        
        # Execute request
        try:
            if method == "GET":
                response = await self.client.get(endpoint, params=parameters, headers=headers)
            elif method == "POST":
                response = await self.client.post(endpoint, json=parameters, headers=headers)
            elif method == "PUT":
                response = await self.client.put(endpoint, json=parameters, headers=headers)
            elif method == "DELETE":
                response = await self.client.delete(endpoint, params=parameters, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Check response
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            
            return result
        except httpx.HTTPError as e:
            logger.error(f"HTTP error executing capability {capability_id}: {str(e)}")
            raise RuntimeError(f"HTTP error: {str(e)}")
        except Exception as e:
            logger.error(f"Error executing capability {capability_id}: {str(e)}")
            raise RuntimeError(f"Execution error: {str(e)}")
    
    async def shutdown(self) -> None:
        """
        Shutdown the adapter and release resources.
        """
        if self.client:
            await self.client.aclose()
            self.client = None
            logger.info("REST API adapter shut down") 