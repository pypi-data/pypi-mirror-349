"""
Tool Integration Protocol - Tool Registry

This module implements the Tool Registry component of the Tool Integration Protocol.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

from app.tools.protocol.models import ToolManifest, ToolImplementation, ValidationResult
from app.db.base import Database

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Tool Registry manages tool registration, validation, and lifecycle.
    """
    
    def __init__(self, db: Database):
        """Initialize the Tool Registry."""
        self.db = db
        self._tools: Dict[str, Dict[str, Any]] = {}  # In-memory cache
    
    async def register(self, manifest: ToolManifest, implementation: ToolImplementation) -> str:
        """
        Register a new tool or update an existing tool.
        
        Args:
            manifest: Tool manifest
            implementation: Tool implementation
            
        Returns:
            Tool ID
        """
        # Validate manifest
        validation_result = self.validate_manifest(manifest)
        if not validation_result.is_valid:
            raise ValueError(f"Invalid tool manifest: {validation_result.errors}")
        
        # Check if tool already exists
        existing_tool = await self.get_tool(manifest.tool_id)
        if existing_tool:
            # Update existing tool
            await self._update_tool(manifest, implementation)
            logger.info(f"Updated tool: {manifest.tool_id} (version {manifest.version})")
        else:
            # Register new tool
            await self._create_tool(manifest, implementation)
            logger.info(f"Registered new tool: {manifest.tool_id} (version {manifest.version})")
        
        # Update in-memory cache
        self._tools[manifest.tool_id] = {
            "manifest": manifest.dict(),
            "implementation": implementation.dict()
        }
        
        return manifest.tool_id
    
    async def _create_tool(self, manifest: ToolManifest, implementation: ToolImplementation) -> None:
        """Create a new tool in the database."""
        tool_data = {
            "tool_id": manifest.tool_id,
            "manifest": manifest.dict(),
            "implementation": implementation.dict(),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "status": "active"
        }
        await self.db.insert_tool(tool_data)
    
    async def _update_tool(self, manifest: ToolManifest, implementation: ToolImplementation) -> None:
        """Update an existing tool in the database."""
        tool_data = {
            "manifest": manifest.dict(),
            "implementation": implementation.dict(),
            "updated_at": datetime.utcnow()
        }
        await self.db.update_tool(manifest.tool_id, tool_data)
    
    async def get_tool(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a tool by ID.
        
        Args:
            tool_id: Tool ID
            
        Returns:
            Tool data or None if not found
        """
        # Check in-memory cache first
        if tool_id in self._tools:
            return self._tools[tool_id]
        
        # Query database
        tool_data = await self.db.get_tool(tool_id)
        if tool_data:
            # Update cache
            self._tools[tool_id] = tool_data
            return tool_data
        
        return None
    
    async def list_tools(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        List tools with optional filtering.
        
        Args:
            filters: Optional filters
            
        Returns:
            List of tools
        """
        tools = await self.db.list_tools(filters or {})
        
        # Update cache
        for tool in tools:
            self._tools[tool["tool_id"]] = tool
        
        return tools
    
    async def delete_tool(self, tool_id: str) -> bool:
        """
        Delete a tool.
        
        Args:
            tool_id: Tool ID
            
        Returns:
            True if deleted, False if not found
        """
        # Remove from cache
        if tool_id in self._tools:
            del self._tools[tool_id]
        
        # Delete from database
        return await self.db.delete_tool(tool_id)
    
    def validate_manifest(self, manifest: ToolManifest) -> ValidationResult:
        """
        Validate a tool manifest.
        
        Args:
            manifest: Tool manifest
            
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        # Check tool ID format
        if not manifest.tool_id.isalnum() and not all(c in "-_." for c in manifest.tool_id if not c.isalnum()):
            errors.append("Tool ID must contain only alphanumeric characters, hyphens, underscores, and dots")
        
        # Check version format
        version_parts = manifest.version.split(".")
        if len(version_parts) < 2 or not all(part.isdigit() for part in version_parts):
            errors.append("Version must be in semver format (e.g., 1.0.0)")
        
        # Check capabilities
        if not manifest.capabilities:
            errors.append("Tool must have at least one capability")
        
        # Check capability IDs
        capability_ids = [capability.capability_id for capability in manifest.capabilities]
        if len(capability_ids) != len(set(capability_ids)):
            errors.append("Capability IDs must be unique")
        
        # Check for required fields in capabilities
        for capability in manifest.capabilities:
            if not capability.parameters:
                errors.append(f"Capability {capability.capability_id} must define parameters schema")
            if not capability.returns:
                errors.append(f"Capability {capability.capability_id} must define returns schema")
        
        # Check authentication
        if manifest.authentication.type != "none" and not manifest.authentication.name:
            errors.append("Authentication name is required for non-none authentication types")
        
        # Check platform requirements
        if not manifest.platform_requirements.min_lyraios_version:
            errors.append("Minimum LYRAIOS version is required")
        
        # Add warnings for best practices
        if not manifest.homepage:
            warnings.append("Tool homepage URL is recommended")
        if not manifest.examples:
            warnings.append("Usage examples are recommended")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        ) 