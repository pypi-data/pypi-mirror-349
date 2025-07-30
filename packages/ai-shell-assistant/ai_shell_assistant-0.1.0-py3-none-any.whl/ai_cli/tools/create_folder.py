"""
Create folder tool for AI CLI.
"""
import os
from typing import Any, Dict, List

from ai_cli.tools.base import BaseTool


class CreateFolderTool(BaseTool):
    """A tool to create new folders (directories)."""

    name = "create_folder"
    description = "Create a new folder (directory) at the specified path."

    @property
    def parameters(self) -> List[Dict[str, Any]]:
        """Get the parameters for the create folder tool."""
        return [
            {
                "name": "path",
                "description": "The path where the folder should be created",
                "type": "string",
                "required": True
            },
            {
                "name": "exist_ok",
                "description": "Whether to not error if the folder already exists (default: true)",
                "type": "boolean",
                "required": False
            }
        ]

    def execute(self, args: Dict[str, Any]) -> str:
        """
        Execute the create folder tool.

        Args:
            args: A dictionary containing the folder creation parameters.

        Returns:
            The result of the folder creation operation as a string.
        """
        path = args.get("path", "")
        exist_ok = args.get("exist_ok", True)

        if not path:
            return "Error: No folder path provided"

        # Normalize path
        path = os.path.normpath(path)

        try:
            os.makedirs(path, exist_ok=exist_ok)
            return f"Successfully created folder: {path}"
        except Exception as e:
            return f"Error creating folder: {str(e)}"
