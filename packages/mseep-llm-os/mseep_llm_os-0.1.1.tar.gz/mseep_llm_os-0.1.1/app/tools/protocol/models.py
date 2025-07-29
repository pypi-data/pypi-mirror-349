"""
Tool Integration Protocol - Data Models

This module defines the data models for the Tool Integration Protocol.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, HttpUrl, validator


class ParameterSchema(BaseModel):
    """Schema for a parameter in a tool capability."""
    
    type: str = Field(..., description="Parameter type (string, number, boolean, object, array)")
    description: str = Field(..., description="Description of the parameter")
    required: bool = Field(False, description="Whether the parameter is required")
    default: Optional[Any] = Field(None, description="Default value for the parameter")
    enum: Optional[List[Any]] = Field(None, description="Enumeration of possible values")
    format: Optional[str] = Field(None, description="Format of the parameter (e.g., date-time, email)")
    
    # Additional fields for specific types
    min_length: Optional[int] = Field(None, description="Minimum length for strings")
    max_length: Optional[int] = Field(None, description="Maximum length for strings")
    pattern: Optional[str] = Field(None, description="Regex pattern for strings")
    minimum: Optional[float] = Field(None, description="Minimum value for numbers")
    maximum: Optional[float] = Field(None, description="Maximum value for numbers")
    exclusive_minimum: Optional[bool] = Field(None, description="Whether minimum is exclusive")
    exclusive_maximum: Optional[bool] = Field(None, description="Whether maximum is exclusive")
    multiple_of: Optional[float] = Field(None, description="Number must be multiple of this value")
    items: Optional[Dict[str, Any]] = Field(None, description="Schema for array items")
    properties: Optional[Dict[str, Dict[str, Any]]] = Field(None, description="Schema for object properties")


class ReturnSchema(BaseModel):
    """Schema for the return value of a tool capability."""
    
    type: str = Field(..., description="Return type (string, number, boolean, object, array)")
    description: str = Field(..., description="Description of the return value")
    properties: Optional[Dict[str, Dict[str, Any]]] = Field(None, description="Schema for object properties")
    items: Optional[Dict[str, Any]] = Field(None, description="Schema for array items")


class Example(BaseModel):
    """Example of tool capability usage."""
    
    input: Dict[str, Any] = Field(..., description="Example input parameters")
    output: Dict[str, Any] = Field(..., description="Example output")
    description: Optional[str] = Field(None, description="Description of the example")


class Capability(BaseModel):
    """Tool capability definition."""
    
    capability_id: str = Field(..., description="Unique identifier for the capability")
    name: str = Field(..., description="Display name for the capability")
    description: str = Field(..., description="Detailed description of what this capability does")
    parameters: Dict[str, Any] = Field(..., description="Schema for input parameters")
    returns: Dict[str, Any] = Field(..., description="Schema for return value")
    examples: List[Example] = Field(default_factory=list, description="Usage examples")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AuthenticationType(str, Enum):
    """Types of authentication supported by tools."""
    
    NONE = "none"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    BASIC = "basic"
    BEARER = "bearer"
    CUSTOM = "custom"


class Authentication(BaseModel):
    """Authentication configuration for a tool."""
    
    type: AuthenticationType = Field(..., description="Type of authentication")
    required: bool = Field(True, description="Whether authentication is required")
    location: Optional[str] = Field(None, description="Where authentication should be provided (header, query, body)")
    name: Optional[str] = Field(None, description="Name of the authentication parameter")
    description: Optional[str] = Field(None, description="Description of the authentication method")
    config: Dict[str, Any] = Field(default_factory=dict, description="Additional configuration for authentication")


class RateLimits(BaseModel):
    """Rate limiting configuration for a tool."""
    
    requests_per_minute: Optional[int] = Field(None, description="Maximum requests per minute")
    requests_per_hour: Optional[int] = Field(None, description="Maximum requests per hour")
    requests_per_day: Optional[int] = Field(None, description="Maximum requests per day")
    burst: Optional[int] = Field(None, description="Maximum burst size")
    concurrent_requests: Optional[int] = Field(None, description="Maximum concurrent requests")


class Dependency(BaseModel):
    """Tool dependency definition."""
    
    tool_id: str = Field(..., description="ID of the required tool")
    version_constraint: str = Field(..., description="Version constraint (e.g., >=1.0.0)")
    optional: bool = Field(False, description="Whether the dependency is optional")


class PlatformRequirements(BaseModel):
    """Platform requirements for a tool."""
    
    min_lyraios_version: str = Field(..., description="Minimum LYRAIOS version required")
    supported_platforms: List[str] = Field(default_factory=list, description="Supported platforms")
    required_capabilities: List[str] = Field(default_factory=list, description="Required system capabilities")


class ToolManifest(BaseModel):
    """Tool manifest definition."""
    
    schema_version: str = Field("1.0", description="Version of the manifest schema")
    tool_id: str = Field(..., description="Unique identifier for the tool")
    name: str = Field(..., description="Display name for the tool")
    version: str = Field(..., description="Tool version")
    description: str = Field(..., description="Detailed description of the tool functionality")
    author: str = Field(..., description="Tool author or organization")
    homepage: Optional[HttpUrl] = Field(None, description="Tool documentation URL")
    license: str = Field(..., description="Tool license")
    categories: List[str] = Field(default_factory=list, description="Tool categories")
    tags: List[str] = Field(default_factory=list, description="Tool tags")
    capabilities: List[Capability] = Field(..., description="Tool capabilities")
    authentication: Authentication = Field(..., description="Authentication configuration")
    rate_limits: Optional[RateLimits] = Field(None, description="Rate limiting configuration")
    dependencies: List[Dependency] = Field(default_factory=list, description="Tool dependencies")
    platform_requirements: PlatformRequirements = Field(..., description="Platform requirements")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata") 