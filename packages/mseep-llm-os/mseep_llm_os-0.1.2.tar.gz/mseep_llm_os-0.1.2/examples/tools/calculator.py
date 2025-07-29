"""
Example calculator tool for the LYRAIOS Tool Integration Protocol.
"""

from typing import Any, Dict


def add(parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add two numbers.
    
    Args:
        parameters: Input parameters
        context: Execution context
        
    Returns:
        Result
    """
    a = parameters.get("a", 0)
    b = parameters.get("b", 0)
    
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Parameters 'a' and 'b' must be numbers")
    
    result = a + b
    
    return {
        "result": result
    }


def subtract(parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Subtract two numbers.
    
    Args:
        parameters: Input parameters
        context: Execution context
        
    Returns:
        Result
    """
    a = parameters.get("a", 0)
    b = parameters.get("b", 0)
    
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Parameters 'a' and 'b' must be numbers")
    
    result = a - b
    
    return {
        "result": result
    }


def multiply(parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Multiply two numbers.
    
    Args:
        parameters: Input parameters
        context: Execution context
        
    Returns:
        Result
    """
    a = parameters.get("a", 0)
    b = parameters.get("b", 0)
    
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Parameters 'a' and 'b' must be numbers")
    
    result = a * b
    
    return {
        "result": result
    }


def divide(parameters: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Divide two numbers.
    
    Args:
        parameters: Input parameters
        context: Execution context
        
    Returns:
        Result
    """
    a = parameters.get("a", 0)
    b = parameters.get("b", 0)
    
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Parameters 'a' and 'b' must be numbers")
    
    if b == 0:
        raise ValueError("Division by zero")
    
    result = a / b
    
    return {
        "result": result
    }


def initialize():
    """
    Initialize the calculator tool.
    """
    print("Calculator tool initialized")


def shutdown():
    """
    Shutdown the calculator tool.
    """
    print("Calculator tool shut down") 