"""
MCP Transport Utilities

This module provides transport implementations for MCP communication.
"""

import asyncio
import json
import logging
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

import aiohttp

logger = logging.getLogger(__name__)


class Transport(ABC):
    """
    Abstract base class for MCP transports.
    """
    
    @abstractmethod
    async def send(self, data: str) -> None:
        """
        Send data to the MCP server.
        
        Args:
            data: The data to send.
        """
        pass
    
    @abstractmethod
    async def receive(self) -> str:
        """
        Receive data from the MCP server.
        
        Returns:
            The received data.
        """
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """
        Close the transport.
        """
        pass


class StdioTransport(Transport):
    """
    Transport implementation using standard input/output.
    
    This transport is suitable for local MCP servers that communicate
    via stdin/stdout, such as child processes.
    """
    
    def __init__(self, process: Optional[asyncio.subprocess.Process] = None):
        """
        Initialize the stdio transport.
        
        Args:
            process: Optional subprocess to communicate with.
                If None, the transport will use sys.stdin/stdout.
        """
        self.process = process
        self._receive_queue = asyncio.Queue()
        self._closed = False
        
        if process is None:
            # Use stdin/stdout directly
            self._reader_task = asyncio.create_task(self._read_stdin())
        else:
            # Use subprocess stdout
            self._reader_task = asyncio.create_task(self._read_process())
    
    async def send(self, data: str) -> None:
        """
        Send data to the MCP server.
        
        Args:
            data: The data to send.
        """
        if self._closed:
            raise RuntimeError("Transport is closed")
        
        if self.process is None:
            # Write to stdout
            sys.stdout.write(data + "\n")
            sys.stdout.flush()
        else:
            # Write to process stdin
            self.process.stdin.write((data + "\n").encode("utf-8"))
            await self.process.stdin.drain()
    
    async def receive(self) -> str:
        """
        Receive data from the MCP server.
        
        Returns:
            The received data.
        """
        if self._closed:
            raise RuntimeError("Transport is closed")
        
        return await self._receive_queue.get()
    
    async def close(self) -> None:
        """
        Close the transport.
        """
        if not self._closed:
            self._closed = True
            self._reader_task.cancel()
            
            if self.process is not None:
                try:
                    self.process.terminate()
                    await self.process.wait()
                except Exception as e:
                    logger.warning(f"Error terminating process: {e}")
    
    async def _read_stdin(self) -> None:
        """
        Read data from stdin.
        """
        while not self._closed:
            try:
                line = await asyncio.to_thread(sys.stdin.readline)
                if not line:
                    break
                
                await self._receive_queue.put(line.rstrip("\n"))
            except Exception as e:
                logger.error(f"Error reading from stdin: {e}")
                break
    
    async def _read_process(self) -> None:
        """
        Read data from process stdout.
        """
        if self.process is None or self.process.stdout is None:
            return
        
        while not self._closed:
            try:
                line = await self.process.stdout.readline()
                if not line:
                    break
                
                await self._receive_queue.put(line.decode("utf-8").rstrip("\n"))
            except Exception as e:
                logger.error(f"Error reading from process: {e}")
                break


class HTTPTransport(Transport):
    """
    Transport implementation using HTTP/SSE.
    
    This transport is suitable for remote MCP servers that communicate
    via HTTP and Server-Sent Events (SSE).
    """
    
    def __init__(self, server_url: str):
        """
        Initialize the HTTP transport.
        
        Args:
            server_url: The URL of the MCP server.
        """
        self.server_url = server_url
        self._session: Optional[aiohttp.ClientSession] = None
        self._sse_response: Optional[aiohttp.ClientResponse] = None
        self._receive_queue = asyncio.Queue()
        self._closed = False
        self._reader_task: Optional[asyncio.Task] = None
    
    async def _ensure_session(self) -> None:
        """
        Ensure that the HTTP session is initialized.
        """
        if self._session is None:
            self._session = aiohttp.ClientSession()
            
            # Start SSE connection
            headers = {
                "Accept": "text/event-stream",
                "Cache-Control": "no-cache",
            }
            
            self._sse_response = await self._session.get(
                f"{self.server_url}/events",
                headers=headers
            )
            
            if self._sse_response.status != 200:
                error_text = await self._sse_response.text()
                raise RuntimeError(
                    f"Failed to connect to MCP server: {self._sse_response.status} {error_text}"
                )
            
            self._reader_task = asyncio.create_task(self._read_sse())
    
    async def send(self, data: str) -> None:
        """
        Send data to the MCP server.
        
        Args:
            data: The data to send.
        """
        if self._closed:
            raise RuntimeError("Transport is closed")
        
        await self._ensure_session()
        
        if self._session is None:
            raise RuntimeError("Failed to initialize HTTP session")
        
        async with self._session.post(
            f"{self.server_url}/jsonrpc",
            json=json.loads(data),
            headers={"Content-Type": "application/json"}
        ) as response:
            if response.status != 202:  # Accepted
                error_text = await response.text()
                raise RuntimeError(
                    f"Failed to send data to MCP server: {response.status} {error_text}"
                )
    
    async def receive(self) -> str:
        """
        Receive data from the MCP server.
        
        Returns:
            The received data.
        """
        if self._closed:
            raise RuntimeError("Transport is closed")
        
        await self._ensure_session()
        return await self._receive_queue.get()
    
    async def close(self) -> None:
        """
        Close the transport.
        """
        if not self._closed:
            self._closed = True
            
            if self._reader_task is not None:
                self._reader_task.cancel()
            
            if self._sse_response is not None:
                self._sse_response.close()
            
            if self._session is not None:
                await self._session.close()
    
    async def _read_sse(self) -> None:
        """
        Read Server-Sent Events from the MCP server.
        """
        if self._sse_response is None:
            return
        
        async for line in self._sse_response.content:
            if self._closed:
                break
            
            line = line.decode("utf-8").strip()
            if not line:
                continue
            
            if line.startswith("data: "):
                data = line[6:]  # Remove "data: " prefix
                await self._receive_queue.put(data) 