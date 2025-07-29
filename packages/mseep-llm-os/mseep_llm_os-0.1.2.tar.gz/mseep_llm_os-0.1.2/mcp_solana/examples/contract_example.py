"""
MCP Solana Contract Example

This script demonstrates how to use the enhanced MCP client for Solana smart contract operations.
"""

import asyncio
import base64
import logging
import os
import sys

# Add parent directory to path to import mcp_solana
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from mcp_solana.client import SolanaMCPClient, SolanaContractClient
from mcp_solana.models.protocol import BufferLayout, DataSchema, AccountFilter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """
    Main function demonstrating the use of SolanaContractClient.
    """
    try:
        # Create base client and connect to the server
        logger.info("Creating client and connecting to server...")
        client = SolanaMCPClient()
        await client.initialize()
        
        # Create contract client using the base client
        contract_client = SolanaContractClient(client)
        
        # Example 1: Query program accounts
        logger.info("Example 1: Querying program accounts")
        program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"  # Solana Token Program
        
        # Create filter for token accounts with a specific size
        filters = [
            {
                "dataSize": 165  # Size of token accounts
            }
        ]
        
        # Get program accounts
        accounts = await contract_client.get_program_accounts(program_id, filters)
        logger.info(f"Found {len(accounts)} accounts")
        
        # Show the first account
        if accounts:
            logger.info(f"First account: {accounts[0]}")
        
        # Example 2: Deserialize account data
        logger.info("\nExample 2: Deserializing account data")
        if accounts:
            # Define a schema for token account data
            schema = DataSchema(
                layouts=[
                    BufferLayout(
                        name="tokenAccount",
                        type="struct",
                        offset=0,
                        fields=[
                            BufferLayout(name="mint", type="publickey", offset=0),
                            BufferLayout(name="owner", type="publickey", offset=32),
                            BufferLayout(name="amount", type="u64", offset=64),
                            BufferLayout(name="delegateOption", type="u32", offset=72),
                            BufferLayout(name="delegate", type="publickey", offset=76),
                            BufferLayout(name="state", type="u8", offset=108),
                            BufferLayout(name="isNativeOption", type="u32", offset=109),
                            BufferLayout(name="isNative", type="u64", offset=113),
                            BufferLayout(name="delegatedAmount", type="u64", offset=121),
                            BufferLayout(name="closeAuthorityOption", type="u32", offset=129),
                            BufferLayout(name="closeAuthority", type="publickey", offset=133),
                        ]
                    )
                ]
            )
            
            # Get first account data
            account_data = accounts[0].data
            
            # Deserialize the data
            parsed_data = await contract_client.deserialize_account_data(account_data, schema.dict())
            logger.info(f"Parsed data: {parsed_data}")
        
        # Example 3: Find a program derived address (PDA)
        logger.info("\nExample 3: Finding a PDA")
        program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"  # Solana Token Program
        
        # Create seeds (example: "token" and a public key)
        seeds = [
            base64.b64encode(b"token").decode("ascii"),
            "11111111111111111111111111111111"  # Example public key
        ]
        
        # Find PDA
        pda_result = await contract_client.find_program_address(program_id, seeds)
        logger.info(f"PDA result: {pda_result}")
        
        # Example 4: Create a CPI transaction
        logger.info("\nExample 4: Creating a CPI transaction")
        
        # Define parameters for the CPI
        caller_program_id = "MyProgram111111111111111111111111111111111111"
        target_program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
        
        # Create simple instruction data (e.g., a token transfer instruction)
        instruction_data = base64.b64encode(bytes([3, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0])).decode("ascii")
        
        # Define accounts for the instruction
        accounts = [
            {
                "pubkey": "11111111111111111111111111111111",
                "is_signer": True,
                "is_writable": True
            },
            {
                "pubkey": "22222222222222222222222222222222",
                "is_signer": False,
                "is_writable": True
            },
            {
                "pubkey": "33333333333333333333333333333333",
                "is_signer": False,
                "is_writable": False
            }
        ]
        
        # Create CPI transaction
        cpi_result = await contract_client.create_cpi_transaction(
            caller_program_id,
            target_program_id,
            instruction_data,
            accounts
        )
        logger.info(f"CPI transaction: {cpi_result}")
        
        # Example 5: Call a contract with data parsing
        logger.info("\nExample 5: Calling a contract with data parsing")
        
        # Define parameters for the contract call
        program_id = "MyProgram111111111111111111111111111111111111"
        instruction_data = base64.b64encode(bytes([1, 2, 3, 4])).decode("ascii")
        
        # Define accounts for the instruction
        accounts = [
            {
                "pubkey": "11111111111111111111111111111111",
                "is_signer": True,
                "is_writable": True
            },
            {
                "pubkey": "22222222222222222222222222222222",
                "is_signer": False,
                "is_writable": True
            }
        ]
        
        # Define schema for parsing the return data
        data_schema = DataSchema(
            layouts=[
                BufferLayout(
                    name="result",
                    type="struct",
                    offset=0,
                    fields=[
                        BufferLayout(name="success", type="bool", offset=0),
                        BufferLayout(name="value", type="u64", offset=1)
                    ]
                )
            ]
        ).dict()
        
        # Call contract with parsing
        call_result = await contract_client.call_contract_with_parsing(
            program_id,
            instruction_data,
            accounts,
            data_schema
        )
        logger.info(f"Contract call result: {call_result}")
        
        # Example 6: Get and parse account data in one step
        logger.info("\nExample 6: Getting and parsing account data in one step")
        
        if accounts:
            # Get and parse the first account from earlier
            address = accounts[0].address
            
            # Get and parse the account
            parsed_account = await contract_client.get_and_parse_account(
                address,
                schema.dict()
            )
            logger.info(f"Parsed account: {parsed_account}")
            
            # Example 7: Get and parse all program accounts in one step
            logger.info("\nExample 7: Getting and parsing all program accounts in one step")
            
            # Only get a few accounts to keep the example reasonable
            filters = [
                {
                    "dataSize": 165  # Size of token accounts
                }
            ]
            
            # Limit to just 2 accounts for the example
            limited_accounts = await contract_client.get_and_parse_program_accounts(
                program_id,
                schema.dict(),
                filters
            )
            logger.info(f"Parsed {len(limited_accounts)} accounts")
            
            # Show the first parsed account
            if limited_accounts:
                logger.info(f"First parsed account data: {limited_accounts[0]['parsed_data']}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        # Close the client
        logger.info("Closing client...")
        await client.close()


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main()) 