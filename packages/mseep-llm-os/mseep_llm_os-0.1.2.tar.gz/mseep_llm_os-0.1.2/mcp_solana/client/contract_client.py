"""
MCP Solana Contract Client

This module implements the enhanced MCP client for Solana smart contract operations.
It provides advanced contract interaction capabilities beyond the basic client.
"""

import base64
import logging
from typing import Any, Dict, List, Optional, Union, Callable

from ..models.protocol import (
    AccountFilter,
    AccountInfo,
    BufferLayout,
    DataSchema,
    PDAParams,
    CPIParams,
)
from .client import SolanaMCPClient

logger = logging.getLogger(__name__)


class SolanaContractClient:
    """
    Enhanced MCP Client for Solana smart contract operations.
    
    This client extends the basic Solana MCP client with advanced
    smart contract interaction capabilities, including program account parsing,
    data deserialization, PDA handling, and cross-program invocations.
    """
    
    def __init__(self, client: SolanaMCPClient):
        """
        Initialize the Solana Contract Client.
        
        Args:
            client: The base Solana MCP client to use for communication.
        """
        self.client = client
    
    async def get_program_accounts(
        self,
        program_id: str,
        filters: Optional[List[Dict[str, Any]]] = None,
    ) -> List[AccountInfo]:
        """
        Get all accounts owned by a program.
        
        Args:
            program_id: The program ID to query accounts for.
            filters: Optional filters to apply to the query.
                Each filter should be a dictionary with one of:
                - memcmp: {offset: int, bytes: str}
                - dataSize: int
            
        Returns:
            A list of account information objects.
        """
        params = {
            "program_id": program_id,
        }
        
        if filters:
            params["filters"] = filters
        
        response = await self.client._send_request("get_program_accounts", params)
        
        # Convert response to AccountInfo objects
        accounts = []
        for account_data in response.get("accounts", []):
            accounts.append(AccountInfo(**account_data))
        
        return accounts
    
    async def get_account_info(self, address: str) -> AccountInfo:
        """
        Get information about a specific account.
        
        Args:
            address: The account address to query.
            
        Returns:
            The account information.
        """
        params = {
            "address": address,
        }
        
        response = await self.client._send_request("get_account_info", params)
        
        # Convert response to AccountInfo object
        account_data = response.get("account", {})
        return AccountInfo(**account_data)
    
    async def deserialize_account_data(
        self,
        data: str,
        schema: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Deserialize account data according to a schema.
        
        Args:
            data: The account data (base64 encoded).
            schema: The schema describing the data layout.
                Should contain:
                - layouts: List of BufferLayout objects
                - variant_field: Optional name of field determining variant (for enums)
            
        Returns:
            The deserialized data.
        """
        params = {
            "data": data,
            "schema": schema,
        }
        
        response = await self.client._send_request("deserialize_account_data", params)
        
        return response.get("parsed_data", {})
    
    async def find_program_address(
        self,
        program_id: str,
        seeds: List[str],
    ) -> Dict[str, Union[str, int]]:
        """
        Find a program derived address (PDA).
        
        Args:
            program_id: The program ID to derive the address for.
            seeds: The seeds to use in derivation (base58 or base64 encoded).
            
        Returns:
            A dictionary containing the derived address and bump seed.
        """
        params = {
            "program_id": program_id,
            "seeds": seeds,
        }
        
        return await self.client._send_request("find_program_address", params)
    
    async def create_cpi_transaction(
        self,
        caller_program_id: str,
        target_program_id: str,
        instruction_data: str,
        accounts: List[Dict[str, Any]],
        signers: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a Cross-Program Invocation (CPI) transaction.
        
        Args:
            caller_program_id: The calling program's ID.
            target_program_id: The target program's ID.
            instruction_data: The instruction data (base64 encoded).
            accounts: The accounts to include.
                Each account should be a dictionary with:
                - pubkey: str
                - is_signer: bool
                - is_writable: bool
            signers: The additional signers.
            
        Returns:
            A dictionary containing the CPI transaction data.
        """
        params = {
            "caller_program_id": caller_program_id,
            "target_program_id": target_program_id,
            "instruction_data": instruction_data,
            "accounts": accounts,
        }
        
        if signers:
            params["signers"] = signers
        
        return await self.client._send_request("create_cpi_transaction", params)
    
    async def call_contract_with_parsing(
        self,
        program_id: str,
        instruction_data: str,
        accounts: List[Dict[str, Any]],
        data_schema: Optional[Dict[str, Any]] = None,
        wallet_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Call a smart contract with data parsing.
        
        Args:
            program_id: The ID of the program to call.
            instruction_data: The instruction data to send to the program.
            accounts: The accounts to include in the transaction.
            data_schema: The schema to use for parsing the returned data.
                If provided, the returned data will be parsed according to this schema.
            wallet_name: The name of the wallet to use for the transaction.
                If None, the default wallet will be used.
                
        Returns:
            A dictionary containing the result of the contract call.
        """
        params = {
            "program_id": program_id,
            "instruction_data": instruction_data,
            "accounts": accounts,
            "parse_data": data_schema is not None,
        }
        
        if data_schema:
            params["data_schema"] = data_schema
            
        if wallet_name:
            params["wallet_name"] = wallet_name
        
        return await self.client._send_request("call_contract", params)
    
    async def get_and_parse_account(
        self,
        address: str,
        schema: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Get an account and parse its data in a single operation.
        
        Args:
            address: The account address to query.
            schema: The schema to use for parsing the account data.
            
        Returns:
            The account information with parsed data.
        """
        # Get the account info
        account = await self.get_account_info(address)
        
        # Parse the data
        parsed_data = await self.deserialize_account_data(account.data, schema)
        
        # Add parsed data to account
        account_dict = account.dict()
        account_dict["parsed_data"] = parsed_data
        
        return account_dict
    
    async def get_and_parse_program_accounts(
        self,
        program_id: str,
        schema: Dict[str, Any],
        filters: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get all program accounts and parse their data in a single operation.
        
        Args:
            program_id: The program ID to query accounts for.
            schema: The schema to use for parsing the account data.
            filters: Optional filters to apply to the query.
            
        Returns:
            A list of account information objects with parsed data.
        """
        # Get the program accounts
        accounts = await self.get_program_accounts(program_id, filters)
        
        # Parse each account's data
        result = []
        for account in accounts:
            try:
                account_dict = account.dict()
                parsed_data = await self.deserialize_account_data(account.data, schema)
                account_dict["parsed_data"] = parsed_data
                result.append(account_dict)
            except Exception as e:
                logger.warning(f"Failed to parse account {account.address}: {e}")
                account_dict = account.dict()
                account_dict["parsed_data"] = None
                result.append(account_dict)
        
        return result 