"""
Base class for AI CLI tools.

This module provides the abstract base class that all tools in the AI CLI must inherit from.
It defines the common interface and functionality that all tools must implement.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseTool(ABC):
    """
    Base class for all tools in the AI CLI.
    
    All tools must inherit from this class and implement its abstract methods.
    Each tool must define:
    - name: A unique identifier for the tool
    - description: A human-readable description of what the tool does
    - parameters: A list of parameters the tool accepts
    - execute: The method that implements the tool's functionality
    """

    name: str
    description: str

    def __init__(self):
        """
        Initialize the tool.
        
        Validates that the tool has the required name and description attributes.
        """
        if not hasattr(self, 'name'):
            raise ValueError("Tool must have a name")
        if not hasattr(self, 'description'):
            raise ValueError("Tool must have a description")

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> str:
        """
        Execute the tool with the given arguments.

        Args:
            args: A dictionary of arguments for the tool.

        Returns:
            The result of the tool execution as a string.
        """
        pass

    @property
    @abstractmethod
    def parameters(self) -> List[Dict[str, Any]]:
        """
        Get the parameters that this tool accepts.

        Each parameter should be a dictionary with at least:
        - name: The parameter name
        - description: A description of the parameter
        - type: The parameter type (string, boolean, etc.)
        - required: Whether the parameter is required

        Returns:
            A list of parameter definitions.
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the tool to a dictionary representation for the OpenAI API.

        This method formats the tool in the structure expected by OpenAI's
        function calling API.

        Returns:
            A dictionary representation of the tool.
        """
        properties = {}
        required_params = []
        
        for param in self.parameters:
            param_name = param["name"]
            param_dict = {
                "type": param.get("type", "string"),
                "description": param["description"]
            }
            
            # Add enum values if provided
            if "enum" in param:
                param_dict["enum"] = param["enum"]
                
            properties[param_name] = param_dict
            
            # Track required parameters
            if param.get("required", False):
                required_params.append(param_name)
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required_params
                }
            }
        }