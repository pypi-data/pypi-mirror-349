"""
MCP Solana Client Example

This example demonstrates how to use the MCP Solana client to interact with
a Solana blockchain through an MCP server.
"""

import asyncio
import logging
import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from client.client import SolanaMCPClient


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """
    Main example function.
    """
    # Create a client with HTTP transport
    client = SolanaMCPClient(server_url="http://localhost:8080")
    
    try:
        # Initialize the client
        logger.info("Initializing client...")
        success = await client.initialize()
        if not success:
            logger.error("Failed to initialize client")
            return
        
        # Get wallet address
        logger.info("Getting wallet address...")
        address = await client.get_wallet_address()
        logger.info(f"Wallet address: {address}")
        
        # Get wallet balance
        logger.info("Getting wallet balance...")
        balance = await client.get_wallet_balance(address)
        logger.info(f"Wallet balance: {balance}")
        
        # Get token accounts
        logger.info("Getting token accounts...")
        token_accounts = await client.get_token_accounts(address)
        logger.info(f"Found {len(token_accounts)} token accounts")
        for account in token_accounts:
            logger.info(f"  - {account.get('token_name', 'Unknown')} ({account.get('token_symbol', '?')}): {account.get('amount', '0')}")
        
        # Example: Transfer SOL (commented out for safety)
        """
        logger.info("Transferring SOL...")
        recipient = "RECIPIENT_ADDRESS_HERE"
        amount = 0.01  # SOL
        tx = await client.transfer_sol(recipient, amount)
        logger.info(f"Transfer transaction: {tx}")
        """
        
        # Example: Deploy a contract (commented out for safety)
        """
        logger.info("Deploying contract...")
        with open("path/to/program.so", "rb") as f:
            program_data = base64.b64encode(f.read()).decode("utf-8")
        
        deployment = await client.deploy_contract(program_data)
        logger.info(f"Contract deployed: {deployment}")
        """
        
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        # Close the client
        logger.info("Closing client...")
        await client.close()


if __name__ == "__main__":
    asyncio.run(main()) 