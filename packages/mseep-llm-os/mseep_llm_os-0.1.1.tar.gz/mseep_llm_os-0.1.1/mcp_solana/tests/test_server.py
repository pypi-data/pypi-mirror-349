"""
Tests for the MCP Solana server.
"""

import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mcp_solana.server.server import SolanaMCPServer
from mcp_solana.models.protocol import (
    MCPError,
    MCPErrorCode,
    SolanaCapability,
    SolanaCapabilityType,
)


@pytest.fixture
async def server():
    """Create a server for testing."""
    # Create a server with a mock Solana client
    server = SolanaMCPServer(rpc_url="https://api.mocknet.solana.com")
    
    # Mock the Solana client
    mock_client = AsyncMock()
    mock_client.get_version.return_value = {"solana-core": "1.14.0"}
    mock_client.get_balance.return_value = {
        "jsonrpc": "2.0",
        "result": {"value": 1500000000},
        "id": 1
    }
    server.solana_client = mock_client
    
    # Initialize the server
    await server.initialize()
    
    yield server
    
    # Clean up
    await server.shutdown()


@pytest.mark.asyncio
async def test_initialize(server):
    """Test initializing the server."""
    # Server is already initialized in the fixture
    assert server._initialized is True
    
    # Test re-initializing
    await server.initialize()
    assert server._initialized is True


@pytest.mark.asyncio
async def test_handle_initialize_request(server):
    """Test handling an initialize request."""
    request = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    })
    
    response_json = await server.handle_request(request)
    response = json.loads(response_json)
    
    assert "result" in response
    assert "server_info" in response["result"]
    assert "capabilities" in response["result"]
    assert len(response["result"]["capabilities"]) == 4


@pytest.mark.asyncio
async def test_handle_get_wallet_address_request(server):
    """Test handling a get_wallet_address request."""
    # Test with default wallet
    request = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_wallet_address",
        "params": {}
    })
    
    response_json = await server.handle_request(request)
    response = json.loads(response_json)
    
    assert "result" in response
    assert "address" in response["result"]
    assert "name" in response["result"]
    assert response["result"]["name"] == "default"
    
    # Test with specific wallet
    request = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "get_wallet_address",
        "params": {"wallet_name": "default"}
    })
    
    response_json = await server.handle_request(request)
    response = json.loads(response_json)
    
    assert "result" in response
    assert "address" in response["result"]
    
    # Test with non-existent wallet
    request = json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "get_wallet_address",
        "params": {"wallet_name": "nonexistent"}
    })
    
    response_json = await server.handle_request(request)
    response = json.loads(response_json)
    
    assert "error" in response
    assert response["error"]["code"] == MCPErrorCode.WALLET_NOT_FOUND


@pytest.mark.asyncio
async def test_handle_get_wallet_balance_request(server):
    """Test handling a get_wallet_balance request."""
    # Test with default wallet
    request = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_wallet_balance",
        "params": {}
    })
    
    response_json = await server.handle_request(request)
    response = json.loads(response_json)
    
    assert "result" in response
    assert "balance" in response["result"]
    assert "sol" in response["result"]["balance"]
    assert "lamports" in response["result"]["balance"]
    assert response["result"]["balance"]["lamports"] == 1500000000
    assert response["result"]["balance"]["sol"] == 1.5
    
    # Test with specific address
    request = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "get_wallet_balance",
        "params": {"address": "7XnwN3VaBDfNFiNQjEMnB8VCsYbaNgPwR3Ng9TDuF7Eo"}
    })
    
    response_json = await server.handle_request(request)
    response = json.loads(response_json)
    
    assert "result" in response
    assert "balance" in response["result"]


@pytest.mark.asyncio
async def test_handle_transfer_sol_request(server):
    """Test handling a transfer_sol request."""
    request = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "transfer_sol",
        "params": {
            "to_address": "9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin",
            "amount": 0.1
        }
    })
    
    response_json = await server.handle_request(request)
    response = json.loads(response_json)
    
    assert "result" in response
    assert "transaction" in response["result"]
    assert "signature" in response["result"]["transaction"]
    assert "status" in response["result"]["transaction"]
    assert response["result"]["transaction"]["status"] == "confirmed"


@pytest.mark.asyncio
async def test_handle_get_token_accounts_request(server):
    """Test handling a get_token_accounts request."""
    request = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_token_accounts",
        "params": {}
    })
    
    response_json = await server.handle_request(request)
    response = json.loads(response_json)
    
    assert "result" in response
    assert "token_accounts" in response["result"]
    assert len(response["result"]["token_accounts"]) == 2
    assert "address" in response["result"]["token_accounts"][0]
    assert "mint" in response["result"]["token_accounts"][0]
    assert "token_symbol" in response["result"]["token_accounts"][0]


@pytest.mark.asyncio
async def test_handle_invalid_request(server):
    """Test handling an invalid request."""
    # Test with invalid JSON
    response_json = await server.handle_request("invalid json")
    response = json.loads(response_json)
    
    assert "error" in response
    assert response["error"]["code"] == MCPErrorCode.PARSE_ERROR
    
    # Test with missing method
    request = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "params": {}
    })
    
    response_json = await server.handle_request(request)
    response = json.loads(response_json)
    
    assert "error" in response
    assert response["error"]["code"] == MCPErrorCode.INVALID_REQUEST
    
    # Test with unknown method
    request = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "unknown_method",
        "params": {}
    })
    
    response_json = await server.handle_request(request)
    response = json.loads(response_json)
    
    assert "error" in response
    assert response["error"]["code"] == MCPErrorCode.METHOD_NOT_FOUND


@pytest.mark.asyncio
async def test_handle_notification(server):
    """Test handling a notification."""
    # Create a mock notification handler
    handler_called = False
    
    async def mock_handler(params):
        nonlocal handler_called
        handler_called = True
    
    # Register the handler
    server._notification_handlers["test_notification"] = mock_handler
    
    # Send a notification
    notification = json.dumps({
        "jsonrpc": "2.0",
        "method": "test_notification",
        "params": {"test": "data"}
    })
    
    await server.handle_notification(notification)
    
    # Check that the handler was called
    assert handler_called is True
    
    # Test with unknown method
    handler_called = False
    notification = json.dumps({
        "jsonrpc": "2.0",
        "method": "unknown_notification",
        "params": {}
    })
    
    await server.handle_notification(notification)
    
    # Check that no handler was called
    assert handler_called is False
    
    # Test with invalid JSON
    handler_called = False
    await server.handle_notification("invalid json")
    
    # Check that no handler was called
    assert handler_called is False


@pytest.mark.asyncio
async def test_shutdown(server):
    """Test shutting down the server."""
    # Server is initialized in the fixture
    assert server._initialized is True
    
    # Shutdown the server
    await server.shutdown()
    
    # Check that the server is shut down
    assert server._initialized is False
    
    # Test shutting down an already shut down server
    await server.shutdown()
    assert server._initialized is False 