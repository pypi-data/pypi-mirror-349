"""
MCP Solana Contract Server

This module implements the enhanced MCP server for Solana smart contract operations.
It extends the basic server with advanced contract interaction capabilities.
"""

import base64
import json
import logging
from typing import Any, Dict, List, Optional, Union

from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction, TransactionInstruction, AccountMeta

try:
    import base58
except ImportError:
    # Fallback implementation if base58 is not available
    import hashlib
    
    class Base58:
        ALPHABET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        
        @staticmethod
        def b58decode(s):
            if isinstance(s, str):
                s = s.encode('ascii')
            
            # Convert base58 string to integer
            value = 0
            for c in s:
                value = value * 58 + Base58.ALPHABET.index(c)
            
            # Convert integer to bytes
            result = value.to_bytes((value.bit_length() + 7) // 8, 'big')
            return result
    
    base58 = Base58

from ..models.protocol import (
    MCPError,
    MCPErrorCode,
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


class SolanaContractServer:
    """
    Enhanced Solana MCP Server for smart contract interactions.
    
    This class provides methods for advanced smart contract interactions,
    including program account parsing, data deserialization, PDA handling,
    and cross-program invocation support.
    """
    
    def __init__(self, solana_client: AsyncClient):
        """
        Initialize the Solana Contract Server.
        
        Args:
            solana_client: The Solana RPC client to use for interactions.
        """
        self.solana_client = solana_client
    
    async def get_program_accounts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get all accounts owned by a program.
        
        Args:
            params: The request parameters.
                program_id: The program ID to query accounts for.
                filters: Optional filters to apply.
            
        Returns:
            A dictionary containing the program accounts.
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
    
    async def get_account_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get information about a specific account.
        
        Args:
            params: The request parameters.
                address: The account address to query.
            
        Returns:
            A dictionary containing the account information.
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
    
    def deserialize_account_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deserialize account data according to a schema.
        
        Args:
            params: The request parameters.
                data: The account data (base64 encoded).
                schema: The schema describing the data layout.
            
        Returns:
            A dictionary containing the deserialized data.
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
    
    def find_program_address(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find a program derived address (PDA).
        
        Args:
            params: The request parameters.
                program_id: The program ID to derive the address for.
                seeds: The seeds to use in derivation (base58 or base64 encoded).
            
        Returns:
            A dictionary containing the derived address and bump seed.
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
    
    def create_cpi_transaction(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a Cross-Program Invocation (CPI) transaction.
        
        Args:
            params: The request parameters.
                caller_program_id: The calling program's ID.
                target_program_id: The target program's ID.
                instruction_data: The instruction data (base64 encoded).
                accounts: The accounts to include.
                signers: The additional signers.
            
        Returns:
            A dictionary containing the CPI transaction data.
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
    
    async def call_contract(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a smart contract with enhanced account data parsing.
        
        Args:
            params: The request parameters.
                program_id: The ID of the program to call.
                instruction_data: The instruction data to send to the program.
                accounts: The accounts to include in the transaction.
                parse_data: Whether to parse the returned data.
                data_schema: The schema to use for parsing the returned data.
            
        Returns:
            A dictionary containing the result of the contract call.
        """
        # Get parameters
        program_id = params.get("program_id")
        instruction_data = params.get("instruction_data")
        accounts = params.get("accounts", [])
        parse_data = params.get("parse_data", False)
        data_schema_dict = params.get("data_schema")
        
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
        
        try:
            # In a real implementation, this would create and submit a transaction
            # For this example, we'll create a simulated transaction and result
            
            # Simulate transaction execution
            signature = f"CallContract_{program_id[:8]}"
            
            # Generate simulated return data
            return_data = base64.b64encode(b"Example return data").decode("utf-8")
            
            # Parse data if requested
            parsed_data = None
            if parse_data and data_schema_dict:
                try:
                    data_schema = DataSchema(**data_schema_dict)
                    parsed_data = DataDeserializer.deserialize(return_data, data_schema)
                except Exception as e:
                    logger.warning(f"Failed to parse return data: {e}")
            
            # Create response
            result = {
                "transaction": {
                    "signature": signature,
                    "status": "confirmed",
                    "block_time": 1234567890,
                    "confirmations": 32,
                    "fee": 5000,
                    "slot": 123456789
                },
                "data": return_data
            }
            
            if parsed_data is not None:
                result["parsed_data"] = parsed_data
            
            return {"result": result}
            
        except MCPError as e:
            # Re-raise MCP errors
            raise
        except Exception as e:
            logger.error(f"Error calling contract: {e}")
            raise MCPError(
                code=MCPErrorCode.CONTRACT_ERROR,
                message=f"Failed to call contract: {str(e)}"
            ) 