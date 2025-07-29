"""
MCP Protocol Models

This module defines the data models for the MCP protocol used in Solana integration.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class MCPRequest(BaseModel):
    """
    MCP JSON-RPC Request model.
    """
    jsonrpc: str = "2.0"
    id: str
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)


class MCPResponse(BaseModel):
    """
    MCP JSON-RPC Response model.
    """
    jsonrpc: str = "2.0"
    id: str
    result: Dict[str, Any] = Field(default_factory=dict)


class MCPNotification(BaseModel):
    """
    MCP JSON-RPC Notification model (no response expected).
    """
    jsonrpc: str = "2.0"
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)


class MCPErrorCode(int, Enum):
    """
    MCP Error Codes.
    """
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603
    
    # Solana-specific error codes
    WALLET_NOT_FOUND = -32000
    INSUFFICIENT_FUNDS = -32001
    TRANSACTION_FAILED = -32002
    CONTRACT_ERROR = -32003
    UNAUTHORIZED = -32004
    ACCOUNT_NOT_FOUND = -32005
    INVALID_ACCOUNT_DATA = -32006
    PDA_ERROR = -32007
    CPI_ERROR = -32008


class MCPError(Exception):
    """
    MCP JSON-RPC Error model.
    """
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None
    
    def __init__(
        self,
        code: int,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"[{code}] {message}")
    
    def dict(self) -> Dict[str, Any]:
        """
        Convert the error to a dictionary.
        """
        result = {
            "code": self.code,
            "message": self.message,
        }
        if self.data is not None:
            result["data"] = self.data
        return result


class SolanaCapabilityType(str, Enum):
    """
    Types of Solana capabilities.
    """
    WALLET = "wallet"
    TRANSACTION = "transaction"
    CONTRACT = "contract"
    TOKEN = "token"


class SolanaCapability(BaseModel):
    """
    Solana capability model.
    """
    id: str
    type: SolanaCapabilityType
    name: str
    description: str
    methods: List[str]
    parameters: Dict[str, Any] = Field(default_factory=dict)


class WalletInfo(BaseModel):
    """
    Solana wallet information.
    """
    address: str
    name: Optional[str] = None
    is_default: bool = False


class TokenAccount(BaseModel):
    """
    Solana token account information.
    """
    address: str
    mint: str
    owner: str
    amount: str
    decimals: int
    token_name: Optional[str] = None
    token_symbol: Optional[str] = None


class TransactionInfo(BaseModel):
    """
    Solana transaction information.
    """
    signature: str
    status: str
    block_time: Optional[int] = None
    confirmations: Optional[int] = None
    fee: int
    slot: Optional[int] = None


class AccountInfo(BaseModel):
    """
    Solana account information with parsed data.
    """
    address: str
    owner: str
    lamports: int
    data: str  # Base64 encoded data
    executable: bool
    rent_epoch: int
    parsed_data: Optional[Dict[str, Any]] = None


class AccountFilter(BaseModel):
    """
    Filter for querying program accounts.
    """
    memcmp: Optional[Dict[str, Any]] = None  # {offset: int, bytes: str}
    dataSize: Optional[int] = None


class ProgramAccountConfig(BaseModel):
    """
    Configuration for querying program accounts.
    """
    filters: List[AccountFilter] = Field(default_factory=list)
    encoding: str = "base64"
    with_context: bool = False


class PDAParams(BaseModel):
    """
    Parameters for finding a Program Derived Address (PDA).
    """
    program_id: str
    seeds: List[str]  # Base58 or Base64 encoded seeds


class CPIParams(BaseModel):
    """
    Parameters for Cross-Program Invocation (CPI).
    """
    caller_program_id: str
    target_program_id: str
    instruction_data: str  # Base64 encoded instruction data
    accounts: List[Dict[str, Any]]
    signers: List[str] = Field(default_factory=list)


class BufferLayout(BaseModel):
    """
    Description of a buffer layout for data deserialization.
    """
    name: str
    type: str
    offset: int
    length: Optional[int] = None
    fields: Optional[List["BufferLayout"]] = None

# Resolve forward reference
BufferLayout.update_forward_refs()


class DataSchema(BaseModel):
    """
    Schema for deserializing account data.
    """
    layouts: List[BufferLayout]
    variant_field: Optional[str] = None  # For enum/union types 