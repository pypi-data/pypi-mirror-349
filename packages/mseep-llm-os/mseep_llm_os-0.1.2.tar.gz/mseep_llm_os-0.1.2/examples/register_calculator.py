"""
Script to register the calculator tool.
"""

import asyncio
import json
import os
import sys

import httpx

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.tools.protocol.models import ToolManifest, ToolImplementation


async def register_calculator():
    """Register the calculator tool."""
    # Load manifest
    with open("examples/tools/calculator_manifest.json", "r") as f:
        manifest_data = json.load(f)
    
    # Create manifest
    manifest = ToolManifest(**manifest_data)
    
    # Create implementation
    implementation = ToolImplementation(
        implementation_type="python_plugin",
        config={
            "plugin_path": os.path.abspath("examples/tools/calculator.py"),
            "sandbox_enabled": False
        }
    )
    
    # Register tool
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/tools/register",
            json={
                "manifest": manifest.dict(),
                "implementation": implementation.dict()
            },
            headers={
                "X-API-Key": "test-api-key"
            }
        )
    
    # Check response
    if response.status_code == 200:
        print(f"Calculator tool registered successfully: {response.json()}")
    else:
        print(f"Failed to register calculator tool: {response.status_code} {response.text}")


if __name__ == "__main__":
    asyncio.run(register_calculator()) 