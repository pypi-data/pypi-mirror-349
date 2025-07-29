"""
Authentication module for the API.
"""

from typing import Optional

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

# API key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


class User(BaseModel):
    """User model."""
    
    id: str
    name: str
    roles: list[str] = []


# Mock user database
users = {
    "test-api-key": User(id="user1", name="Test User", roles=["admin"]),
}


async def get_current_user(api_key: str = Security(api_key_header)) -> Optional[User]:
    """
    Get the current user based on the API key.
    
    Args:
        api_key: API key from the request header
        
    Returns:
        User object if authenticated, None otherwise
    """
    if not api_key:
        return None
    
    user = users.get(api_key)
    if not user:
        return None
    
    return user


async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    """
    Get the current user and verify they have admin role.
    
    Args:
        user: Current user
        
    Returns:
        User object if authenticated and has admin role
        
    Raises:
        HTTPException: If not authenticated or not an admin
    """
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if "admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return user 