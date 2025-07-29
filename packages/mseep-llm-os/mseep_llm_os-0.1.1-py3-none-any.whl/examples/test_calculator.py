"""
Script to test the calculator tool.
"""

import asyncio
import os
import sys

import httpx

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


async def test_calculator():
    """Test the calculator tool."""
    # Test add capability
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/tools/calculator/capabilities/add/execute",
            json={
                "parameters": {"a": 2, "b": 3},
                "context": {}
            },
            headers={
                "X-API-Key": "test-api-key"
            }
        )
    
    # Check response
    if response.status_code == 200:
        print(f"Add capability executed successfully: {response.json()}")
    else:
        print(f"Failed to execute add capability: {response.status_code} {response.text}")
    
    # Test subtract capability
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/tools/calculator/capabilities/subtract/execute",
            json={
                "parameters": {"a": 5, "b": 3},
                "context": {}
            },
            headers={
                "X-API-Key": "test-api-key"
            }
        )
    
    # Check response
    if response.status_code == 200:
        print(f"Subtract capability executed successfully: {response.json()}")
    else:
        print(f"Failed to execute subtract capability: {response.status_code} {response.text}")


if __name__ == "__main__":
    asyncio.run(test_calculator()) 