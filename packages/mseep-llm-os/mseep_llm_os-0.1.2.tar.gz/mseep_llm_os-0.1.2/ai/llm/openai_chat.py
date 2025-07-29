from typing import Optional, Dict, Any, Iterator, AsyncIterator, Union
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion
from phi.llm.openai import OpenAIChat as PhiOpenAIChat
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class CustomOpenAIChat(PhiOpenAIChat):
    def __init__(self, api_key: str, base_url: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        # Initialize OpenAI client with custom base URL and API key
        client_params = {
            "api_key": api_key,
        }
        
        if base_url:
            client_params["base_url"] = base_url
            
        self.client = OpenAI(**client_params)
        
    def get_client(self) -> OpenAI:
        """Override to return our custom client"""
        return self.client
    
    async def get_async_client(self) -> AsyncOpenAI:
        """Returns a custom async OpenAI client"""
        
        # Get settings from environment variables or configuration
        api_key = self.api_key
        base_url = self.base_url
        organization = self.organization
        
        # Create client configuration
        client_kwargs: Dict[str, Any] = {
            "api_key": api_key,
            "timeout": self.timeout,
            # Add custom headers directly in the client configuration
            "default_headers": {
                "User-Agent": "CustomOpenAIChat/1.0"
            }
        }
        
        # Add optional configuration
        if base_url:
            client_kwargs["base_url"] = base_url
        if organization:
            client_kwargs["organization"] = organization
            
        # Create custom async client
        return AsyncOpenAI(**client_kwargs)

    def create_completion(self, stream: bool = False) -> Union[ChatCompletion, Iterator[str]]:
        """Create chat completion"""
        try:
            client = self.get_client()
            response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=stream,
                **self.completion_kwargs
            )
            
            if stream:
                return self._process_stream_response(response)
            return response
            
        except Exception as e:
            logger.error(f"Failed to create chat completion: {e}")
            raise

    async def acreate_completion(self, stream: bool = False) -> Union[ChatCompletion, AsyncIterator[str]]:
        """Create async chat completion"""
        try:
            client = await self.get_async_client()
            response = await client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=stream,
                **self.completion_kwargs
            )
            
            if stream:
                return self._process_async_stream_response(response)
            return response
            
        except Exception as e:
            logger.error(f"Failed to create async chat completion: {e}")
            raise

    def _process_stream_response(self, response: Iterator[ChatCompletion]) -> Iterator[str]:
        """Process stream response"""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    async def _process_async_stream_response(self, response: AsyncIterator[ChatCompletion]) -> AsyncIterator[str]:
        """Process async stream response"""
        async for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content