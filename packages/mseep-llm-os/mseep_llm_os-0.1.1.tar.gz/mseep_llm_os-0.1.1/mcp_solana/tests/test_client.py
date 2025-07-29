"""
Tests for the MCP Solana client.
"""

import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mcp_solana.client.client import SolanaMCPClient
from mcp_solana.models.protocol import (
    MCPError,
    MCPErrorCode,
    SolanaCapability,
    SolanaCapabilityType,
)
from mcp_solana.utils.transport import Transport


class MockTransport(Transport):
    """Mock transport for testing."""
    
    def __init__(self):
        self.sent_messages = []
        self.receive_queue = asyncio.Queue()
        self.closed = False
    
    async def start(self):
        """Start the transport."""
        pass
    
    async def send(self, data: str) -> str:
        """Send data and return a mock response."""
        self.sent_messages.append(data)
        request = json.loads(data)
        
        # Generate a response based on the request
        if request["method"] == "initialize":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "server_info": {
                        "name": "mock_solana_server",
                        "version": "0.1.0",
                        "rpc_url": "https://api.mocknet.solana.com",
                    },
                    "capabilities": [
                        {
                            "id": "wallet",
                            "type": "wallet",
                            "name": "Solana Wallet",
                            "description": "Manage Solana wallets",
                            "methods": ["get_wallet_address", "get_wallet_balance"]
                        },
                        {
                            "id": "transaction",
                            "type": "transaction",
                            "name": "Solana Transactions",
                            "description": "Send Solana transactions",
                            "methods": ["transfer_sol"]
                        }
                    ]
                }
            })
        elif request["method"] == "get_wallet_address":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "address": "7XnwN3VaBDfNFiNQjEMnB8VCsYbaNgPwR3Ng9TDuF7Eo",
                    "name": "default"
                }
            })
        elif request["method"] == "get_wallet_balance":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "balance": {
                        "sol": 1.5,
                        "lamports": 1500000000
                    }
                }
            })
        elif request["method"] == "transfer_sol":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "transaction": {
                        "signature": "5UfgccYEPu7fqrk4TQ3sFfYGQNYUXQqXLUGQDY8irDYxb6L9TpxvzMkrAGZMSNwAhNNjASrszSYt5BNqUzHQUiHY",
                        "status": "confirmed",
                        "block_time": 1679012345,
                        "confirmations": 10,
                        "fee": 5000,
                        "slot": 123456789
                    }
                }
            })
        elif request["method"] == "get_token_accounts":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "token_accounts": [
                        {
                            "address": "7XnwN3VaBDfNFiNQjEMnB8VCsYbaNgPwR3Ng9TDuF7Eo",
                            "mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                            "owner": "7XnwN3VaBDfNFiNQjEMnB8VCsYbaNgPwR3Ng9TDuF7Eo",
                            "amount": "100000000",
                            "decimals": 6,
                            "token_name": "USD Coin",
                            "token_symbol": "USDC"
                        }
                    ]
                }
            })
        elif request["method"] == "error_test":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": request["id"],
                "error": {
                    "code": MCPErrorCode.INTERNAL_ERROR,
                    "message": "Test error"
                }
            })
        elif request["method"] == "shutdown":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "success": True
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": request["id"],
                "error": {
                    "code": MCPErrorCode.METHOD_NOT_FOUND,
                    "message": f"Method not found: {request['method']}"
                }
            })
    
    async def receive(self) -> str:
        """Receive data from the queue."""
        try:
            return await asyncio.wait_for(self.receive_queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            return ""
    
    async def close(self) -> None:
        """Close the transport."""
        self.closed = True
    
    def add_notification(self, method: str, params: dict) -> None:
        """Add a notification to the receive queue."""
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        self.receive_queue.put_nowait(json.dumps(notification))


@pytest.fixture
def mock_transport():
    """Create a mock transport."""
    return MockTransport()


@pytest.fixture
def client(mock_transport):
    """Create a client with a mock transport."""
    return SolanaMCPClient(transport=mock_transport)


@pytest.mark.asyncio
async def test_initialize(client, mock_transport):
    """Test initializing the client."""
    result = await client.initialize()
    
    # Check that the request was sent
    assert len(mock_transport.sent_messages) == 1
    request = json.loads(mock_transport.sent_messages[0])
    assert request["method"] == "initialize"
    
    # Check the result
    assert "server_info" in result
    assert "capabilities" in result
    assert len(result["capabilities"]) == 2
    
    # Check that the client is initialized
    assert client._initialized is True
    assert len(client._capabilities) == 2


@pytest.mark.asyncio
async def test_get_wallet_address(client):
    """Test getting a wallet address."""
    result = await client.get_wallet_address()
    
    assert "address" in result
    assert result["address"] == "7XnwN3VaBDfNFiNQjEMnB8VCsYbaNgPwR3Ng9TDuF7Eo"
    assert "name" in result
    assert result["name"] == "default"


@pytest.mark.asyncio
async def test_get_wallet_balance(client):
    """Test getting a wallet balance."""
    result = await client.get_wallet_balance()
    
    assert "balance" in result
    assert "sol" in result["balance"]
    assert result["balance"]["sol"] == 1.5
    assert "lamports" in result["balance"]
    assert result["balance"]["lamports"] == 1500000000


@pytest.mark.asyncio
async def test_transfer_sol(client):
    """Test transferring SOL."""
    result = await client.transfer_sol(
        to_address="9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin",
        amount=0.1
    )
    
    assert "transaction" in result
    assert "signature" in result["transaction"]
    assert "status" in result["transaction"]
    assert result["transaction"]["status"] == "confirmed"


@pytest.mark.asyncio
async def test_get_token_accounts(client):
    """Test getting token accounts."""
    result = await client.get_token_accounts()
    
    assert "token_accounts" in result
    assert len(result["token_accounts"]) == 1
    assert "address" in result["token_accounts"][0]
    assert "mint" in result["token_accounts"][0]
    assert "token_symbol" in result["token_accounts"][0]
    assert result["token_accounts"][0]["token_symbol"] == "USDC"


@pytest.mark.asyncio
async def test_error_handling(client):
    """Test error handling."""
    with pytest.raises(MCPError) as excinfo:
        await client._send_request("error_test", {})
    
    assert excinfo.value.code == MCPErrorCode.INTERNAL_ERROR
    assert excinfo.value.message == "Test error"


@pytest.mark.asyncio
async def test_notification_handling(client, mock_transport):
    """Test notification handling."""
    # Create a mock handler
    handler_called = False
    handler_params = None
    
    def notification_handler(params):
        nonlocal handler_called, handler_params
        handler_called = True
        handler_params = params
    
    # Register the handler
    client.register_notification_handler("test_notification", notification_handler)
    
    # Initialize the client to start the notification listener
    await client.initialize()
    
    # Add a notification
    mock_transport.add_notification("test_notification", {"test": "data"})
    
    # Wait for the notification to be processed
    await asyncio.sleep(0.2)
    
    # Check that the handler was called
    assert handler_called is True
    assert handler_params == {"test": "data"}
    
    # Unregister the handler
    client.unregister_notification_handler("test_notification", notification_handler)
    
    # Reset the flags
    handler_called = False
    handler_params = None
    
    # Add another notification
    mock_transport.add_notification("test_notification", {"test": "data2"})
    
    # Wait for the notification to be processed
    await asyncio.sleep(0.2)
    
    # Check that the handler was not called
    assert handler_called is False


@pytest.mark.asyncio
async def test_close(client, mock_transport):
    """Test closing the client."""
    # Initialize the client
    await client.initialize()
    
    # Close the client
    await client.close()
    
    # Check that the transport was closed
    assert mock_transport.closed is True
    assert client._initialized is False


@pytest.mark.asyncio
async def test_shutdown(client, mock_transport):
    """Test shutting down the server."""
    # Initialize the client
    await client.initialize()
    
    # Shutdown the server
    result = await client.shutdown()
    
    # Check the result
    assert "success" in result
    assert result["success"] is True
    
    # Check that the client was closed
    assert mock_transport.closed is True
    assert client._initialized is False 