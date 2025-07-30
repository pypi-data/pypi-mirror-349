"""
Create file tool for AI CLI.
"""
import os
from typing import Any, Dict, List

from ai_cli.tools.base import BaseTool


class CreateFileTool(BaseTool):
    """A tool to create new files with specified content."""
    
    name = "create_file"
    description = "Create a new file with specified content"
    
    @property
    def parameters(self) -> List[Dict[str, Any]]:
        """Get the parameters for the create file tool."""
        return [
            {
                "name": "path",
                "description": "The path where the file should be created",
                "type": "string",
                "required": True
            },
            {
                "name": "content",
                "description": "The content to write to the file",
                "type": "string",
                "required": False
            },
            {
                "name": "overwrite",
                "description": "Whether to overwrite the file if it already exists",
                "type": "boolean",
                "required": False
            }
        ]
    
    def execute(self, args: Dict[str, Any]) -> str:
        """
        Execute the create file tool.
        
        Args:
            args: A dictionary containing the file creation parameters.
            
        Returns:
            The result of the file creation operation as a string.
        """
        path = args.get("path", "")
        content = args.get("content", "")
        overwrite = args.get("overwrite", False)
        
        if not path:
            return "Error: No file path provided"
        
        # Normalize path
        path = os.path.normpath(path)
        
        # Check if the file already exists
        if os.path.exists(path) and not overwrite:
            return f"Error: File '{path}' already exists. Use 'overwrite: true' to replace it."
        
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            # Write the file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Successfully created file: {path}"
            
        except Exception as e:
            return f"Error creating file: {str(e)}"