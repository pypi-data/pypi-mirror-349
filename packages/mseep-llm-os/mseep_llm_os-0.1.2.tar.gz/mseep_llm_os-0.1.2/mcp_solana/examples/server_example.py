"""
MCP Solana Server Example

This script demonstrates how to set up and run an MCP Solana server.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the package
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp_solana.server.server import SolanaMCPServer, run_server


async def main():
    """
    Run the MCP Solana server example.
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Create and initialize the server
    server = SolanaMCPServer(
        # Use Solana devnet for testing
        rpc_url="https://api.devnet.solana.com",
        # Use a test wallet directory
        wallet_path=os.path.expanduser("~/.solana/test-wallets")
    )
    
    # Initialize the server
    await server.initialize()
    
    # Process a sample request
    sample_request = """
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_wallet_address",
        "params": {}
    }
    """
    
    response = await server.handle_request(sample_request.strip())
    print(f"Sample response: {response}")
    
    # Run the server in a loop
    print("Starting MCP Solana server. Press Ctrl+C to exit.")
    try:
        # In a real application, you would use run_server() instead
        # of this simplified loop
        while True:
            # Wait for input
            print("Enter a JSON-RPC request (or 'exit' to quit):")
            request = input().strip()
            
            if request.lower() == "exit":
                break
            
            # Process the request
            response = await server.handle_request(request)
            print(f"Response: {response}")
    
    except KeyboardInterrupt:
        print("Server interrupted")
    finally:
        # Shutdown the server
        await server.shutdown()
        print("Server shut down")


def run_example():
    """
    Run the example.
    """
    asyncio.run(main())


if __name__ == "__main__":
    run_example() 