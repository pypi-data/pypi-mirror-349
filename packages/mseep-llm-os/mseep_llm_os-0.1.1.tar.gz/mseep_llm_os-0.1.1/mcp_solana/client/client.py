"""
MCP Solana Client

This module implements the MCP client for Solana blockchain operations.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union, Callable

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
)
from ..utils.transport import Transport, StdioTransport, HTTPTransport

logger = logging.getLogger(__name__)


class SolanaMCPClient:
    """
    MCP Client for Solana blockchain operations.
    
    This client provides an interface to interact with the Solana blockchain
    through an MCP server, supporting wallet management, transaction signing,
    and smart contract interactions.
    """
    
    def __init__(
        self,
        transport: Optional[Transport] = None,
        server_url: Optional[str] = None,
    ):
        """
        Initialize the Solana MCP Client.
        
        Args:
            transport: The transport to use for communication with the server.
                If None, a transport will be created based on server_url.
            server_url: The URL of the MCP server.
                If None, a local server will be used via stdin/stdout.
        """
        if transport is None:
            if server_url is not None:
                self.transport = HTTPTransport(server_url)
            else:
                self.transport = StdioTransport()
        else:
            self.transport = transport
        
        self._request_id = 0
        self._capabilities: List[SolanaCapability] = []
        self._initialized = False
        self._notification_handlers: Dict[str, List[Callable]] = {}
    
    async def initialize(self) -> Dict[str, Any]:
        """
        Initialize the client and connect to the server.
        
        Returns:
            The server information and capabilities.
        """
        if self._initialized:
            return {
                "server_info": {},
                "capabilities": [cap.dict() for cap in self._capabilities]
            }
        
        # Start the transport
        await self.transport.start()
        
        # Start the notification listener
        asyncio.create_task(self._notification_listener())
        
        # Send initialize request
        response = await self._send_request("initialize", {})
        
        # Parse capabilities
        capabilities = []
        for cap_data in response.get("capabilities", []):
            capabilities.append(SolanaCapability(**cap_data))
        
        self._capabilities = capabilities
        self._initialized = True
        
        return response
    
    async def get_wallet_address(self, wallet_name: Optional[str] = None) -> Dict[str, str]:
        """
        Get the address of a wallet.
        
        Args:
            wallet_name: The name of the wallet to get the address for.
                If None, the default wallet will be used.
                
        Returns:
            A dictionary containing the wallet address and name.
        """
        params = {}
        if wallet_name is not None:
            params["wallet_name"] = wallet_name
        
        return await self._send_request("get_wallet_address", params)
    
    async def get_wallet_balance(self, address: Optional[str] = None) -> Dict[str, Dict[str, Union[float, int]]]:
        """
        Get the balance of a wallet.
        
        Args:
            address: The address of the wallet to get the balance for.
                If None, the default wallet will be used.
                
        Returns:
            A dictionary containing the wallet balance in SOL and lamports.
        """
        params = {}
        if address is not None:
            params["address"] = address
        
        return await self._send_request("get_wallet_balance", params)
    
    async def transfer_sol(
        self,
        to_address: str,
        amount: float,
        from_address: Optional[str] = None,
    ) -> Dict[str, TransactionInfo]:
        """
        Transfer SOL from one wallet to another.
        
        Args:
            to_address: The address to transfer SOL to.
            amount: The amount of SOL to transfer.
            from_address: The address to transfer SOL from.
                If None, the default wallet will be used.
                
        Returns:
            A dictionary containing the transaction information.
        """
        params = {
            "to_address": to_address,
            "amount": amount,
        }
        if from_address is not None:
            params["from_address"] = from_address
        
        return await self._send_request("transfer_sol", params)
    
    async def deploy_contract(
        self,
        program_data: str,
        wallet_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Deploy a smart contract to the Solana blockchain.
        
        Args:
            program_data: The compiled program data to deploy.
            wallet_name: The name of the wallet to use for deployment.
                If None, the default wallet will be used.
                
        Returns:
            A dictionary containing the deployment information.
        """
        params = {
            "program_data": program_data,
        }
        if wallet_name is not None:
            params["wallet_name"] = wallet_name
        
        return await self._send_request("deploy_contract", params)
    
    async def call_contract(
        self,
        program_id: str,
        instruction_data: str,
        accounts: List[Dict[str, Any]],
        wallet_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Call a smart contract on the Solana blockchain.
        
        Args:
            program_id: The ID of the program to call.
            instruction_data: The instruction data to send to the program.
            accounts: The accounts to include in the transaction.
            wallet_name: The name of the wallet to use for the transaction.
                If None, the default wallet will be used.
                
        Returns:
            A dictionary containing the result of the contract call.
        """
        params = {
            "program_id": program_id,
            "instruction_data": instruction_data,
            "accounts": accounts,
        }
        if wallet_name is not None:
            params["wallet_name"] = wallet_name
        
        return await self._send_request("call_contract", params)
    
    async def get_token_accounts(
        self,
        owner_address: Optional[str] = None,
        mint_address: Optional[str] = None,
    ) -> Dict[str, List[TokenAccount]]:
        """
        Get token accounts for a wallet.
        
        Args:
            owner_address: The address of the wallet to get token accounts for.
                If None, the default wallet will be used.
            mint_address: The address of the token mint to filter by.
                If None, all token accounts will be returned.
                
        Returns:
            A dictionary containing a list of token accounts.
        """
        params = {}
        if owner_address is not None:
            params["owner_address"] = owner_address
        if mint_address is not None:
            params["mint_address"] = mint_address
        
        return await self._send_request("get_token_accounts", params)
    
    async def shutdown(self) -> Dict[str, bool]:
        """
        Shutdown the server.
        
        Returns:
            A dictionary indicating success.
        """
        try:
            return await self._send_request("shutdown", {})
        finally:
            await self.close()
    
    async def close(self) -> None:
        """
        Close the client connection.
        """
        if not self._initialized:
            return
        
        await self.transport.close()
        self._initialized = False
    
    def register_notification_handler(
        self,
        method: str,
        handler: Callable[[Dict[str, Any]], None],
    ) -> None:
        """
        Register a handler for notifications.
        
        Args:
            method: The notification method to handle.
            handler: The handler function to call when a notification is received.
        """
        if method not in self._notification_handlers:
            self._notification_handlers[method] = []
        
        self._notification_handlers[method].append(handler)
    
    def unregister_notification_handler(
        self,
        method: str,
        handler: Callable[[Dict[str, Any]], None],
    ) -> None:
        """
        Unregister a handler for notifications.
        
        Args:
            method: The notification method to unregister the handler for.
            handler: The handler function to unregister.
        """
        if method in self._notification_handlers:
            if handler in self._notification_handlers[method]:
                self._notification_handlers[method].remove(handler)
    
    async def _send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a request to the server.
        
        Args:
            method: The method to call.
            params: The parameters to pass to the method.
            
        Returns:
            The response result.
            
        Raises:
            MCPError: If the server returns an error.
        """
        if not self._initialized and method != "initialize":
            await self.initialize()
        
        # Create request
        self._request_id += 1
        request = MCPRequest(
            jsonrpc="2.0",
            id=self._request_id,
            method=method,
            params=params
        )
        
        # Send request
        request_json = json.dumps(request.dict())
        response_json = await self.transport.send(request_json)
        
        # Parse response
        try:
            response_data = json.loads(response_json)
            
            # Check for error
            if "error" in response_data:
                error_data = response_data["error"]
                raise MCPError(
                    code=error_data.get("code", MCPErrorCode.INTERNAL_ERROR),
                    message=error_data.get("message", "Unknown error"),
                    data=error_data.get("data")
                )
            
            # Return result
            return response_data.get("result", {})
            
        except json.JSONDecodeError:
            raise MCPError(
                code=MCPErrorCode.PARSE_ERROR,
                message="Invalid JSON in response"
            )
    
    async def _notification_listener(self) -> None:
        """
        Listen for notifications from the server.
        """
        while self._initialized:
            try:
                notification_json = await self.transport.receive()
                if not notification_json:
                    continue
                
                # Parse notification
                notification_data = json.loads(notification_json)
                
                # Check if it's a notification (no id)
                if "id" not in notification_data or notification_data["id"] is None:
                    notification = MCPNotification(**notification_data)
                    
                    # Call handlers
                    handlers = self._notification_handlers.get(notification.method, [])
                    for handler in handlers:
                        try:
                            handler(notification.params)
                        except Exception as e:
                            logger.error(f"Error in notification handler: {e}")
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in notification listener: {e}")
                await asyncio.sleep(1)  # Avoid tight loop on error 