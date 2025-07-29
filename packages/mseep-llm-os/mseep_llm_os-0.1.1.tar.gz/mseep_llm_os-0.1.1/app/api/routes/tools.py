"""
API routes for the Tool Integration Protocol.
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.auth import get_current_user
from app.db.memory import MemoryDatabase
from app.tools.protocol.executor import ToolExecutionError, ToolExecutor
from app.tools.protocol.models import ToolImplementation, ToolManifest, ValidationResult
from app.tools.protocol.registry import ToolRegistry

router = APIRouter()

# Initialize database and registry
db = MemoryDatabase()
registry = ToolRegistry(db)
executor = ToolExecutor(registry)


@router.post("/register", response_model=Dict[str, Any])
async def register_tool(
    manifest: ToolManifest,
    implementation: ToolImplementation,
    user = Depends(get_current_user)
):
    """
    Register a new tool or update an existing tool.
    """
    try:
        # Validate manifest
        validation_result = registry.validate_manifest(manifest)
        if not validation_result.is_valid:
            raise HTTPException(status_code=400, detail=validation_result.errors)
        
        # Register tool
        tool_id = await registry.register(manifest, implementation)
        
        return {"tool_id": tool_id, "status": "registered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=List[Dict[str, Any]])
async def list_tools(
    category: Optional[str] = Query(None, description="Filter by category"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    user = Depends(get_current_user)
):
    """
    List registered tools with optional filtering.
    """
    try:
        filters = {}
        if category:
            filters["manifest.categories"] = category
        if tag:
            filters["manifest.tags"] = tag
        
        tools = await registry.list_tools(filters)
        
        return tools
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{tool_id}", response_model=Dict[str, Any])
async def get_tool(
    tool_id: str,
    user = Depends(get_current_user)
):
    """
    Get a tool by ID.
    """
    try:
        tool = await registry.get_tool(tool_id)
        if not tool:
            raise HTTPException(status_code=404, detail=f"Tool not found: {tool_id}")
        
        return tool
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{tool_id}", response_model=Dict[str, Any])
async def delete_tool(
    tool_id: str,
    user = Depends(get_current_user)
):
    """
    Delete a tool.
    """
    try:
        deleted = await registry.delete_tool(tool_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Tool not found: {tool_id}")
        
        return {"tool_id": tool_id, "status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{tool_id}/capabilities/{capability_id}/execute", response_model=Dict[str, Any])
async def execute_capability(
    tool_id: str,
    capability_id: str,
    parameters: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None,
    user = Depends(get_current_user)
):
    """
    Execute a tool capability.
    """
    try:
        # Get tool
        tool = await registry.get_tool(tool_id)
        if not tool:
            raise HTTPException(status_code=404, detail=f"Tool not found: {tool_id}")
        
        # Execute capability
        result = await executor.execute(
            tool_id=tool_id,
            capability_id=capability_id,
            parameters=parameters,
            context=context or {},
            user_id=user.id if user else None
        )
        
        return result
    except ToolExecutionError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 