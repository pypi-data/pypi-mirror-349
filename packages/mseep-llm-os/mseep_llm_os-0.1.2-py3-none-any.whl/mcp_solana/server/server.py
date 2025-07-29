"""
MCP Solana Server

This module implements the MCP server for Solana blockchain operations.
"""

import argparse
import asyncio
import base64
import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional, Union

import solana
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction, TransactionInstruction, AccountMeta

from ..models.protocol import (
    MCPRequest,
    MCPResponse,
    MCPNotification,
    MCPError,
    MCPErrorCode,
    SolanaCapability,
    SolanaCapabilityType,
    WalletInfo,
    TokenAccount,
    TransactionInfo,
    AccountInfo,
    AccountFilter,
    ProgramAccountConfig,
    PDAParams,
    CPIParams,
    DataSchema,
    BufferLayout,
)

from ..utils.contract_utils import (
    AccountParser,
    DataDeserializer,
    PDAHelper, 
    CPIHelper
)

logger = logging.getLogger(__name__)


class SolanaMCPServer:
    """
    MCP Server for Solana blockchain operations.
    
    This server provides Solana blockchain capabilities to MCP clients,
    such as wallet management, transaction signing, and smart contract
    interactions.
    """
    
    def __init__(
        self,
        rpc_url: str = "https://api.devnet.solana.com",
        wallet_path: Optional[str] = None,
    ):
        """
        Initialize the Solana MCP Server.
        
        Args:
            rpc_url: The URL of the Solana RPC endpoint.
            wallet_path: Path to the wallet keystore directory.
                If None, a default path will be used.
        """
        self.rpc_url = rpc_url
        self.wallet_path = wallet_path or os.path.expanduser("~/.solana/wallets")
        self.solana_client = AsyncClient(rpc_url)
        self._wallets: Dict[str, WalletInfo] = {}
        self._request_handlers: Dict[str, callable] = {}
        self._notification_handlers: Dict[str, callable] = {}
        self._initialized = False
        
        # Register request handlers
        self._register_handlers()
    
    async def initialize(self) -> None:
        """
        Initialize the server.
        """
        if self._initialized:
            return
        
        # Load wallets
        await self._load_wallets("DefaultWalletAddress123")  # Placeholder for demo
        
        # Test connection to Solana
        try:
            version = await self.solana_client.get_version()
            logger.info(f"Connected to Solana node: {version}")
        except Exception as e:
            logger.error(f"Failed to connect to Solana node: {e}")
            raise
        
        self._initialized = True
        logger.info("Solana MCP server initialized successfully")
    
    async def handle_request(self, request_json: str) -> str:
        """
        Handle an incoming MCP request.
        
        Args:
            request_json: The JSON-encoded request.
            
        Returns:
            The JSON-encoded response.
        """
        try:
            request_data = json.loads(request_json)
            request = MCPRequest(**request_data)
            
            # Check if we have a handler for this method
            handler = self._request_handlers.get(request.method)
            if handler is None:
                error = MCPError(
                    code=MCPErrorCode.METHOD_NOT_FOUND,
                    message=f"Method not found: {request.method}"
                )
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "error": error.dict()
                })
            
            # Call the handler
            try:
                result = await handler(request.params)
                response = MCPResponse(
                    jsonrpc="2.0",
                    id=request.id,
                    result=result
                )
                return json.dumps(response.dict())
            except MCPError as e:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "error": e.dict()
                })
            except Exception as e:
                logger.error(f"Error handling request: {e}")
                error = MCPError(
                    code=MCPErrorCode.INTERNAL_ERROR,
                    message=str(e)
                )
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": request.id,
                    "error": error.dict()
                })
                
        except json.JSONDecodeError:
            error = MCPError(
                code=MCPErrorCode.PARSE_ERROR,
                message="Invalid JSON"
            )
            return json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": error.dict()
            })
        except Exception as e:
            logger.error(f"Error parsing request: {e}")
            error = MCPError(
                code=MCPErrorCode.INVALID_REQUEST,
                message=str(e)
            )
            return json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": error.dict()
            })
    
    async def handle_notification(self, notification_json: str) -> None:
        """
        Handle an incoming MCP notification.
        
        Args:
            notification_json: The JSON-encoded notification.
        """
        try:
            notification_data = json.loads(notification_json)
            notification = MCPNotification(**notification_data)
            
            # Check if we have a handler for this method
            handler = self._notification_handlers.get(notification.method)
            if handler is None:
                logger.warning(f"No handler for notification method: {notification.method}")
                return
            
            # Call the handler
            try:
                await handler(notification.params)
            except Exception as e:
                logger.error(f"Error handling notification: {e}")
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON in notification")
        except Exception as e:
            logger.error(f"Error parsing notification: {e}")
    
    async def shutdown(self) -> None:
        """
        Shutdown the server.
        """
        if not self._initialized:
            return
        
        # Close Solana client
        await self.solana_client.close()
        
        self._initialized = False
        logger.info("Solana MCP server shut down")
    
    def _register_handlers(self) -> None:
        """
        Register request and notification handlers.
        """
        # Request handlers
        self._request_handlers = {
            "initialize": self._handle_initialize,
            "get_wallet_address": self._handle_get_wallet_address,
            "get_wallet_balance": self._handle_get_wallet_balance,
            "transfer_sol": self._handle_transfer_sol,
            "deploy_contract": self._handle_deploy_contract,
            "call_contract": self._handle_call_contract,
            "get_token_accounts": self._handle_get_token_accounts,
            "get_program_accounts": self._handle_get_program_accounts,
            "get_account_info": self._handle_get_account_info,
            "deserialize_account_data": self._handle_deserialize_account_data,
            "find_program_address": self._handle_find_program_address,
            "create_cpi_transaction": self._handle_create_cpi_transaction,
            "shutdown": self._handle_shutdown,
        }
        
        # Notification handlers
        self._notification_handlers = {
            # Add notification handlers here
        }
    
    async def _load_wallets(self, address) -> None:
        """
        Load wallet information from the wallet directory.
        """
        # In a real implementation, this would load actual wallet files
        # For this example, we'll just create a dummy wallet
        self._wallets = {
            "default": WalletInfo(
                address=address,
                name="default",
                is_default=True
            )
        }
        logger.info(f"Loaded {len(self._wallets)} wallets")
    
    async def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the initialize request.
        
        Args:
            params: The request parameters.
            
        Returns:
            The response result.
        """
        await self.initialize()
        
        # Return server capabilities
        capabilities = [
            SolanaCapability(
                id="wallet",
                type=SolanaCapabilityType.WALLET,
                name="Solana Wallet",
                description="Manage Solana wallets and check balances",
                methods=["get_wallet_address", "get_wallet_balance"]
            ),
            SolanaCapability(
                id="transaction",
                type=SolanaCapabilityType.TRANSACTION,
                name="Solana Transactions",
                description="Send Solana transactions",
                methods=["transfer_sol"]
            ),
            SolanaCapability(
                id="contract",
                type=SolanaCapabilityType.CONTRACT,
                name="Solana Smart Contracts",
                description="Deploy and interact with Solana programs",
                methods=[
                    "deploy_contract", 
                    "call_contract",
                    "get_program_accounts",
                    "get_account_info",
                    "deserialize_account_data",
                    "find_program_address",
                    "create_cpi_transaction"
                ]
            ),
            SolanaCapability(
                id="token",
                type=SolanaCapabilityType.TOKEN,
                name="Solana Tokens",
                description="Manage Solana tokens",
                methods=["get_token_accounts"]
            ),
        ]
        
        return {
            "server_info": {
                "name": "solana_mcp_server",
                "version": "0.1.0",
                "rpc_url": self.rpc_url,
            },
            "capabilities": [cap.dict() for cap in capabilities]
        }
    
    async def _handle_get_wallet_address(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the get_wallet_address request.
        
        Args:
            params: The request parameters.
            
        Returns:
            The response result.
        """
        wallet_name = params.get("wallet_name")
        
        if wallet_name is not None:
            if wallet_name not in self._wallets:
                raise MCPError(
                    code=MCPErrorCode.WALLET_NOT_FOUND,
                    message=f"Wallet not found: {wallet_name}"
                )
            wallet = self._wallets[wallet_name]
        else:
            # Use default wallet
            wallet = next((w for w in self._wallets.values() if w.is_default), None)
            if wallet is None:
                raise MCPError(
                    code=MCPErrorCode.WALLET_NOT_FOUND,
                    message="No default wallet found"
                )
        
        return {
            "address": wallet.address,
            "name": wallet.name
        }
    
    async def _handle_get_wallet_balance(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the get_wallet_balance request.
        
        Args:
            params: The request parameters.
            
        Returns:
            The response result.
        """
        address = params.get("address")
        
        if address is None:
            # Use default wallet
            wallet = next((w for w in self._wallets.values() if w.is_default), None)
            if wallet is None:
                raise MCPError(
                    code=MCPErrorCode.WALLET_NOT_FOUND,
                    message="No default wallet found"
                )
            address = wallet.address
        
        try:
            # Get balance from Solana
            balance = await self.solana_client.get_balance(PublicKey(address))
            
            return {
                "balance": {
                    "sol": balance["result"]["value"] / 1_000_000_000,  # Convert lamports to SOL
                    "lamports": balance["result"]["value"]
                }
            }
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            raise MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message=f"Failed to get balance: {str(e)}"
            )
    
    async def _handle_transfer_sol(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the transfer_sol request.
        
        Args:
            params: The request parameters.
            
        Returns:
            The response result.
        """
        # In a real implementation, this would create and send a transaction
        # For this example, we'll just return a dummy transaction
        # get signature, status, block_time, confirmations, fee, slot from params
        signature = params.get("signature")
        status = params.get("status")
        block_time = params.get("block_time")
        confirmations = params.get("confirmations")
        fee = params.get("fee")
        slot = params.get("slot")
        return {
            "transaction": {
                "signature": signature,
                "status": "confirmed",
                "block_time": block_time,
                "confirmations": confirmations,
                "fee": fee,
                "slot": slot
            }
        }
    
    async def _handle_deploy_contract(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the deploy_contract request.
        
        Args:
            params: The request parameters.
            
        Returns:
            The response result.
        """
        # In a real implementation, this would deploy a program
        # For this example, we'll just return a dummy deployment
        program_id = params.get("program_id", "ProgramID123456789abcdef")
        program_data = params.get("program_data", "")
        
        # Create a simulated transaction for program deployment
        signature = "DeploymentSignature123456789abcdef"
        
        return {
            "deployment": {
                "program_id": program_id,
                "transaction": {
                    "signature": signature,
                    "status": "confirmed",
                    "block_time": 1234567890,
                    "confirmations": 10,
                    "fee": 5000,
                    "slot": 123456789
                }
            }
        }
    
    async def _handle_call_contract(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the call_contract request.
        
        Args:
            params: The request parameters.
            
        Returns:
            The response result.
        """
        # Get parameters
        program_id = params.get("program_id", "")
        instruction_data = params.get("instruction_data", "")
        accounts = params.get("accounts", [])
        wallet_name = params.get("wallet_name")
        
        # Validate parameters
        if not program_id:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Missing program_id parameter"
            )
        
        if not instruction_data:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Missing instruction_data parameter"
            )
        
        if not accounts:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Missing accounts parameter"
            )
        
        # In a real implementation, this would create and submit a transaction
        # For demonstration purposes, we'll create a simulated transaction
        signature = "CallContractSignature123456789abcdef"
        
        # Create a response with transaction information and simulated return data
        return {
            "result": {
                "transaction": {
                    "signature": signature,
                    "status": "confirmed",
                    "block_time": 1234567890,
                    "confirmations": 32,
                    "fee": 5000,
                    "slot": 123456789
                },
                "data": base64.b64encode(b"Example return data").decode("utf-8")
            }
        }
    
    async def _handle_get_program_accounts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the get_program_accounts request.
        
        Args:
            params: The request parameters.
                program_id: The program ID to query accounts for.
                filters: Optional filters to apply.
            
        Returns:
            The response result with program accounts.
        """
        # Get parameters
        program_id = params.get("program_id")
        filters_data = params.get("filters", [])
        
        # Validate parameters
        if not program_id:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Missing program_id parameter"
            )
        
        # Convert filters to AccountFilter objects
        filters = []
        for filter_data in filters_data:
            filters.append(AccountFilter(**filter_data))
        
        try:
            # Query program accounts
            accounts = await AccountParser.get_program_accounts(
                self.solana_client,
                program_id,
                filters
            )
            
            # Return accounts as dictionaries
            return {
                "accounts": [account.dict() for account in accounts]
            }
        except MCPError as e:
            # Re-raise MCP errors
            raise
        except Exception as e:
            logger.error(f"Error getting program accounts: {e}")
            raise MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message=f"Failed to get program accounts: {str(e)}"
            )
    
    async def _handle_get_account_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the get_account_info request.
        
        Args:
            params: The request parameters.
                address: The account address to query.
            
        Returns:
            The response result with account information.
        """
        # Get parameters
        address = params.get("address")
        
        # Validate parameters
        if not address:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Missing address parameter"
            )
        
        try:
            # Query account info
            account_info = await AccountParser.get_account_info(
                self.solana_client,
                address
            )
            
            if account_info is None:
                raise MCPError(
                    code=MCPErrorCode.ACCOUNT_NOT_FOUND,
                    message=f"Account not found: {address}"
                )
            
            # Return account info as dictionary
            return {
                "account": account_info.dict()
            }
        except MCPError as e:
            # Re-raise MCP errors
            raise
        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            raise MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message=f"Failed to get account info: {str(e)}"
            )
    
    async def _handle_deserialize_account_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the deserialize_account_data request.
        
        Args:
            params: The request parameters.
                data: The account data (base64 encoded).
                schema: The schema describing the data layout.
            
        Returns:
            The response result with deserialized data.
        """
        # Get parameters
        data = params.get("data")
        schema_data = params.get("schema")
        
        # Validate parameters
        if not data:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Missing data parameter"
            )
        
        if not schema_data:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Missing schema parameter"
            )
        
        try:
            # Convert schema to DataSchema object
            schema = DataSchema(**schema_data)
            
            # Deserialize data
            parsed_data = DataDeserializer.deserialize(data, schema)
            
            # Return deserialized data
            return {
                "parsed_data": parsed_data
            }
        except MCPError as e:
            # Re-raise MCP errors
            raise
        except Exception as e:
            logger.error(f"Error deserializing account data: {e}")
            raise MCPError(
                code=MCPErrorCode.INVALID_ACCOUNT_DATA,
                message=f"Failed to deserialize account data: {str(e)}"
            )
    
    async def _handle_find_program_address(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the find_program_address request.
        
        Args:
            params: The request parameters.
                program_id: The program ID to derive the address for.
                seeds: The seeds to use in derivation (base58 or base64 encoded).
            
        Returns:
            The response result with derived PDA.
        """
        # Get parameters
        program_id = params.get("program_id")
        seed_strings = params.get("seeds", [])
        
        # Validate parameters
        if not program_id:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Missing program_id parameter"
            )
        
        if not seed_strings:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Missing seeds parameter"
            )
        
        try:
            # Convert seed strings to bytes
            seeds = []
            for seed_str in seed_strings:
                try:
                    # Try decoding as base58 or base64
                    try:
                        seeds.append(base58.b58decode(seed_str))
                    except:
                        seeds.append(base64.b64decode(seed_str))
                except:
                    raise MCPError(
                        code=MCPErrorCode.INVALID_PARAMS,
                        message=f"Invalid seed format: {seed_str}"
                    )
            
            # Find program address
            address, bump = PDAHelper.find_program_address(program_id, seeds)
            
            # Return derived address and bump seed
            return {
                "address": address,
                "bump_seed": bump
            }
        except MCPError as e:
            # Re-raise MCP errors
            raise
        except Exception as e:
            logger.error(f"Error finding program address: {e}")
            raise MCPError(
                code=MCPErrorCode.PDA_ERROR,
                message=f"Failed to find program address: {str(e)}"
            )
    
    async def _handle_create_cpi_transaction(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the create_cpi_transaction request.
        
        Args:
            params: The request parameters.
                caller_program_id: The calling program's ID.
                target_program_id: The target program's ID.
                instruction_data: The instruction data (base64 encoded).
                accounts: The accounts to include.
                signers: The additional signers.
            
        Returns:
            The response result with transaction data.
        """
        # Get parameters
        caller_program_id = params.get("caller_program_id")
        target_program_id = params.get("target_program_id")
        instruction_data_b64 = params.get("instruction_data")
        accounts = params.get("accounts", [])
        signers = params.get("signers", [])
        
        # Validate parameters
        if not caller_program_id:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Missing caller_program_id parameter"
            )
        
        if not target_program_id:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Missing target_program_id parameter"
            )
        
        if not instruction_data_b64:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Missing instruction_data parameter"
            )
        
        if not accounts:
            raise MCPError(
                code=MCPErrorCode.INVALID_PARAMS,
                message="Missing accounts parameter"
            )
        
        try:
            # Decode instruction data
            instruction_data = base64.b64decode(instruction_data_b64)
            
            # Create CPI instruction
            instruction = CPIHelper.create_cpi_instruction(
                caller_program_id,
                target_program_id,
                instruction_data,
                accounts
            )
            
            # In a real implementation, this would be used to create and sign a transaction
            # For this example, we'll return the instruction details
            
            # Get account metas as dictionaries
            account_metas = [
                {
                    "pubkey": str(acc.pubkey),
                    "is_signer": acc.is_signer,
                    "is_writable": acc.is_writable
                }
                for acc in instruction.keys
            ]
            
            # Return CPI instruction details
            return {
                "instruction": {
                    "program_id": str(instruction.program_id),
                    "data": base64.b64encode(instruction.data).decode("utf-8"),
                    "accounts": account_metas
                },
                "transaction": {
                    "signature": "CPITransactionSignature123456789abcdef",
                    "status": "confirmed",
                    "block_time": 1234567890,
                    "confirmations": 32,
                    "fee": 5000,
                    "slot": 123456789
                }
            }
        except MCPError as e:
            # Re-raise MCP errors
            raise
        except Exception as e:
            logger.error(f"Error creating CPI transaction: {e}")
            raise MCPError(
                code=MCPErrorCode.CPI_ERROR,
                message=f"Failed to create CPI transaction: {str(e)}"
            )
    
    async def _handle_get_token_accounts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the get_token_accounts request.
        
        Args:
            params: The request parameters.
            
        Returns:
            The response result.
        """
        # In a real implementation, this would get token accounts from Solana
        # For this example, we'll just return dummy token accounts
        address = params.get("address")
        mint = params.get("mint")
        owner = params.get("owner")
        amount = params.get("amount")
        decimals = params.get("decimals")
        token_name = params.get("token_name")
        token_symbol = params.get("token_symbol")
        return {
            "token_accounts": [
                {
                    "address": address,
                    "mint": mint,
                    "owner": owner,
                    "amount": amount,
                    "decimals": decimals,
                    "token_name": token_name,
                    "token_symbol": token_symbol
                }
            ]
        }
    
    async def _handle_shutdown(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle the shutdown request.
        
        Args:
            params: The request parameters.
            
        Returns:
            The response result.
        """
        await self.shutdown()
        return {"success": True}


async def run_server(
    rpc_url: str = "https://api.devnet.solana.com",
    wallet_path: Optional[str] = None,
    port: int = 8080,
) -> None:
    """
    Run the MCP Solana server.
    
    Args:
        rpc_url: The URL of the Solana RPC endpoint.
        wallet_path: Path to the wallet keystore directory.
        port: The port to listen on for HTTP connections.
    """
    server = SolanaMCPServer(rpc_url=rpc_url, wallet_path=wallet_path)
    
    # Initialize the server
    await server.initialize()
    
    # In a real implementation, this would start an HTTP server
    # For this example, we'll just use stdin/stdout
    logger.info("MCP Solana server is running (stdin/stdout mode)")
    
    try:
        while True:
            line = await asyncio.to_thread(sys.stdin.readline)
            if not line:
                break
            
            response = await server.handle_request(line.strip())
            sys.stdout.write(response + "\n")
            sys.stdout.flush()
    except KeyboardInterrupt:
        logger.info("Server interrupted")
    finally:
        await server.shutdown()


def main() -> None:
    """
    Main entry point.
    """
    parser = argparse.ArgumentParser(description="MCP Solana Server")
    parser.add_argument(
        "--rpc-url",
        default="https://api.devnet.solana.com",
        help="Solana RPC URL (default: https://api.devnet.solana.com)"
    )
    parser.add_argument(
        "--wallet-path",
        help="Path to wallet keystore directory"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port to listen on for HTTP connections (default: 8080)"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default: INFO)"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Run the server
    asyncio.run(run_server(
        rpc_url=args.rpc_url,
        wallet_path=args.wallet_path,
        port=args.port
    ))


if __name__ == "__main__":
    main() 