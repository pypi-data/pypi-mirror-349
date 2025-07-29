"""
Contract Utilities for Solana MCP

This module provides utilities for interacting with Solana smart contracts,
including account parsing, data deserialization, PDAs, and cross-program invocations.
"""

import base64
import binascii
import struct
from typing import Any, Dict, List, Optional, Tuple, Union

from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.system_program import SYS_PROGRAM_ID
from solana.transaction import AccountMeta, TransactionInstruction
from solana.rpc.types import MemcmpOpts

from ..models.protocol import (
    AccountInfo, 
    AccountFilter, 
    BufferLayout, 
    DataSchema,
    MCPError,
    MCPErrorCode
)


class AccountParser:
    """
    Utility class for parsing Solana program accounts.
    """
    
    @staticmethod
    async def get_program_accounts(
        client: AsyncClient,
        program_id: str,
        filters: List[AccountFilter] = None
    ) -> List[AccountInfo]:
        """
        Get all accounts owned by a program.
        
        Args:
            client: The Solana RPC client.
            program_id: The program ID to query accounts for.
            filters: Optional filters to apply to the query.
            
        Returns:
            A list of account information objects.
        """
        try:
            memcmp_opts = []
            data_size = None
            
            if filters:
                for filter_opt in filters:
                    if filter_opt.memcmp:
                        memcmp = filter_opt.memcmp
                        memcmp_opts.append(
                            MemcmpOpts(
                                offset=memcmp.get("offset", 0),
                                bytes=memcmp.get("bytes", "")
                            )
                        )
                    if filter_opt.dataSize is not None:
                        data_size = filter_opt.dataSize
            
            program_id_key = PublicKey(program_id)
            resp = await client.get_program_accounts(
                program_id_key,
                encoding="base64",
                data_slice=None,
                memcmp_opts=memcmp_opts,
                data_size=data_size
            )
            
            result = []
            for item in resp["result"]:
                account_info = AccountInfo(
                    address=str(item["pubkey"]),
                    owner=str(item["account"]["owner"]),
                    lamports=item["account"]["lamports"],
                    data=item["account"]["data"][0],  # [data, encoding]
                    executable=item["account"]["executable"],
                    rent_epoch=item["account"]["rentEpoch"],
                    parsed_data=None
                )
                result.append(account_info)
            
            return result
        except Exception as e:
            raise MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message=f"Failed to get program accounts: {str(e)}"
            )
    
    @staticmethod
    async def get_account_info(
        client: AsyncClient,
        address: str
    ) -> Optional[AccountInfo]:
        """
        Get information about a specific account.
        
        Args:
            client: The Solana RPC client.
            address: The account address to query.
            
        Returns:
            Account information or None if not found.
        """
        try:
            resp = await client.get_account_info(
                PublicKey(address),
                encoding="base64"
            )
            
            if not resp["result"]["value"]:
                return None
                
            account = resp["result"]["value"]
            account_info = AccountInfo(
                address=address,
                owner=str(account["owner"]),
                lamports=account["lamports"],
                data=account["data"][0],  # [data, encoding]
                executable=account["executable"],
                rent_epoch=account["rentEpoch"],
                parsed_data=None
            )
            
            return account_info
        except Exception as e:
            raise MCPError(
                code=MCPErrorCode.INTERNAL_ERROR,
                message=f"Failed to get account info: {str(e)}"
            )


class DataDeserializer:
    """
    Utility class for deserializing Solana account data.
    """
    
    TYPE_PARSERS = {
        "u8": lambda data, offset: (data[offset], 1),
        "u16": lambda data, offset: (struct.unpack("<H", data[offset:offset+2])[0], 2),
        "u32": lambda data, offset: (struct.unpack("<I", data[offset:offset+4])[0], 4),
        "u64": lambda data, offset: (struct.unpack("<Q", data[offset:offset+8])[0], 8),
        "i8": lambda data, offset: (struct.unpack("<b", data[offset:offset+1])[0], 1),
        "i16": lambda data, offset: (struct.unpack("<h", data[offset:offset+2])[0], 2),
        "i32": lambda data, offset: (struct.unpack("<i", data[offset:offset+4])[0], 4),
        "i64": lambda data, offset: (struct.unpack("<q", data[offset:offset+8])[0], 8),
        "f32": lambda data, offset: (struct.unpack("<f", data[offset:offset+4])[0], 4),
        "f64": lambda data, offset: (struct.unpack("<d", data[offset:offset+8])[0], 8),
        "bool": lambda data, offset: (bool(data[offset]), 1),
        "publickey": lambda data, offset: (str(PublicKey(data[offset:offset+32])), 32),
    }
    
    @classmethod
    def deserialize(
        cls,
        data: str,
        schema: DataSchema
    ) -> Dict[str, Any]:
        """
        Deserialize account data according to a schema.
        
        Args:
            data: Base64 encoded account data.
            schema: The schema describing the data layout.
            
        Returns:
            The parsed data as a dictionary.
        """
        try:
            binary_data = base64.b64decode(data)
            result = {}
            
            for layout in schema.layouts:
                parsed_field, _ = cls._parse_layout(binary_data, layout, 0)
                result.update(parsed_field)
            
            return result
        except Exception as e:
            raise MCPError(
                code=MCPErrorCode.INVALID_ACCOUNT_DATA,
                message=f"Failed to deserialize data: {str(e)}"
            )
    
    @classmethod
    def _parse_layout(
        cls,
        data: bytes,
        layout: BufferLayout,
        base_offset: int
    ) -> Tuple[Dict[str, Any], int]:
        """
        Parse a specific layout from binary data.
        
        Args:
            data: The binary data to parse.
            layout: The layout description.
            base_offset: The base offset in the data.
            
        Returns:
            A tuple of (parsed_data, bytes_consumed).
        """
        offset = base_offset + layout.offset
        
        if layout.type == "struct" and layout.fields:
            result = {}
            total_size = 0
            
            for field in layout.fields:
                field_data, field_size = cls._parse_layout(data, field, offset)
                result.update(field_data)
                total_size = max(total_size, field.offset + field_size)
            
            return {layout.name: result}, total_size
            
        elif layout.type == "array" and layout.fields:
            # The first field is the element type, length is required for arrays
            if not layout.length:
                raise ValueError("Array layout requires length")
                
            element_layout = layout.fields[0]
            result = []
            total_size = 0
            
            for i in range(layout.length):
                # Adjust the element layout's offset for the current array index
                element_offset = offset + (i * element_layout.offset)
                element_data, element_size = cls._parse_layout(
                    data, 
                    element_layout, 
                    element_offset
                )
                result.append(list(element_data.values())[0])  # Get the parsed value
                total_size += element_size
            
            return {layout.name: result}, total_size
            
        elif layout.type in cls.TYPE_PARSERS:
            value, size = cls.TYPE_PARSERS[layout.type](data, offset)
            return {layout.name: value}, size
            
        elif layout.type == "bytes" and layout.length:
            # Special case for fixed-length byte arrays
            value = data[offset:offset+layout.length]
            return {layout.name: base64.b64encode(value).decode('utf-8')}, layout.length
            
        else:
            raise ValueError(f"Unsupported layout type: {layout.type}")


class PDAHelper:
    """
    Utility class for working with Program Derived Addresses (PDAs).
    """
    
    @staticmethod
    def find_program_address(
        program_id: str,
        seeds: List[bytes]
    ) -> Tuple[str, int]:
        """
        Find a valid program derived address and its bump seed.
        
        Args:
            program_id: The program ID to derive the address for.
            seeds: The seeds to use in derivation.
            
        Returns:
            A tuple of (address, bump_seed).
        """
        try:
            program_id_key = PublicKey(program_id)
            
            # Find the first valid bump seed (0-255)
            for bump in range(256):
                try:
                    all_seeds = seeds + [bytes([bump])]
                    address = PublicKey.find_program_address(
                        all_seeds, 
                        program_id_key
                    )
                    return (str(address[0]), address[1])
                except:
                    continue
                
            raise ValueError("Could not find a valid program address")
        except Exception as e:
            raise MCPError(
                code=MCPErrorCode.PDA_ERROR,
                message=f"Failed to find program address: {str(e)}"
            )
    
    @staticmethod
    def derive_buffer_seed(
        offset: int,
        data: bytes,
        owner_address: str
    ) -> bytes:
        """
        Create a buffer seed from account data for PDA derivation.
        
        Args:
            offset: The offset into the buffer.
            data: The data to use.
            owner_address: The owner account address.
            
        Returns:
            The derived seed.
        """
        try:
            # Create a seed that combines owner and data
            owner_bytes = bytes(PublicKey(owner_address))
            seed_data = owner_bytes[offset:offset+16] + data
            
            # Hash the resulting data to create a valid seed
            return seed_data[:32]  # Use up to 32 bytes
        except Exception as e:
            raise MCPError(
                code=MCPErrorCode.PDA_ERROR,
                message=f"Failed to derive buffer seed: {str(e)}"
            )


class CPIHelper:
    """
    Utility class for Cross-Program Invocations (CPI).
    """
    
    @staticmethod
    def create_cpi_instruction(
        caller_program_id: str,
        target_program_id: str,
        instruction_data: bytes,
        accounts: List[Dict[str, Any]]
    ) -> TransactionInstruction:
        """
        Create a transaction instruction for a CPI.
        
        Args:
            caller_program_id: The calling program's ID.
            target_program_id: The target program's ID.
            instruction_data: The instruction data.
            accounts: The accounts to include.
            
        Returns:
            A transaction instruction for the CPI.
        """
        try:
            # Convert account specifications to AccountMeta objects
            account_metas = []
            for account in accounts:
                is_signer = account.get("is_signer", False)
                is_writable = account.get("is_writable", False)
                account_metas.append(
                    AccountMeta(
                        pubkey=PublicKey(account["pubkey"]),
                        is_signer=is_signer,
                        is_writable=is_writable
                    )
                )
            
            # Create the instruction
            return TransactionInstruction(
                program_id=PublicKey(target_program_id),
                data=instruction_data,
                keys=account_metas
            )
        except Exception as e:
            raise MCPError(
                code=MCPErrorCode.CPI_ERROR,
                message=f"Failed to create CPI instruction: {str(e)}"
            )
    
    @staticmethod
    def encode_instruction_data(
        params: Dict[str, Any],
        schema: List[Tuple[str, str]]
    ) -> bytes:
        """
        Encode instruction data according to a schema.
        
        Args:
            params: The parameters to encode.
            schema: The schema describing parameter types [(name, type), ...].
            
        Returns:
            The encoded instruction data.
        """
        try:
            result = bytearray()
            
            for name, param_type in schema:
                value = params.get(name)
                
                if param_type == "u8":
                    result.extend(struct.pack("<B", value))
                elif param_type == "u16":
                    result.extend(struct.pack("<H", value))
                elif param_type == "u32":
                    result.extend(struct.pack("<I", value))
                elif param_type == "u64":
                    result.extend(struct.pack("<Q", value))
                elif param_type == "i8":
                    result.extend(struct.pack("<b", value))
                elif param_type == "i16":
                    result.extend(struct.pack("<h", value))
                elif param_type == "i32":
                    result.extend(struct.pack("<i", value))
                elif param_type == "i64":
                    result.extend(struct.pack("<q", value))
                elif param_type == "bool":
                    result.extend(struct.pack("<B", 1 if value else 0))
                elif param_type == "publickey":
                    result.extend(bytes(PublicKey(value)))
                elif param_type.startswith("bytes"):
                    # Handle fixed-size byte arrays
                    try:
                        length = int(param_type.split("[")[1].split("]")[0])
                        if isinstance(value, str):
                            value = base64.b64decode(value)
                        result.extend(value.ljust(length, b'\x00')[:length])
                    except:
                        raise ValueError(f"Invalid bytes parameter: {param_type}")
                else:
                    raise ValueError(f"Unsupported parameter type: {param_type}")
            
            return bytes(result)
        except Exception as e:
            raise MCPError(
                code=MCPErrorCode.CPI_ERROR,
                message=f"Failed to encode instruction data: {str(e)}"
            ) 