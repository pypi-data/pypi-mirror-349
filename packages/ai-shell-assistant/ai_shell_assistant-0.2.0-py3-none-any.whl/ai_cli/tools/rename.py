"""
Rename tool for AI CLI.
"""
import os
import shutil
from typing import Any, Dict, List, Optional

from ai_cli.tools.dangerous import DangerousTool


class RenameTool(DangerousTool):
    """A tool to rename files or directories."""

    name = "rename"
    description = "Rename a file or directory to a new name"

    @property
    def confirmation_message(self) -> str:
        """Get the confirmation message for the rename tool."""
        return "Warning: You are about to rename files or directories. This could potentially overwrite existing files. Continue? (y/n): "

    @property
    def parameters(self) -> List[Dict[str, Any]]:
        """Get the parameters for the rename tool."""
        return [
            {
                "name": "source",
                "description": "The source file or directory path to rename",
                "type": "string",
                "required": True
            },
            {
                "name": "destination",
                "description": "The new name or path for the file or directory",
                "type": "string",
                "required": True
            },
            {
                "name": "overwrite",
                "description": "Whether to overwrite the destination if it already exists",
                "type": "boolean",
                "required": False
            }
        ]

    def execute(self, args: Dict[str, Any]) -> str:
        """
        Execute the rename tool.

        Args:
            args: A dictionary containing the rename parameters.

        Returns:
            The result of the rename operation as a string.
        """
        source = args.get("source", "")
        destination = args.get("destination", "")
        overwrite = args.get("overwrite", False)

        if not source:
            return "Error: No source path provided"

        if not destination:
            return "Error: No destination path provided"

        if not os.path.exists(source):
            return f"Error: Source path '{source}' does not exist"

        if os.path.exists(destination) and not overwrite:
            return f"Error: Destination path '{destination}' already exists. Use 'overwrite: true' to force rename."

        try:
            # If destination exists and overwrite is True, remove it first
            if os.path.exists(destination) and overwrite:
                if os.path.isfile(destination):
                    os.remove(destination)
                else:
                    shutil.rmtree(destination)

            # Perform the rename operation
            shutil.move(source, destination)

            # Determine what was renamed (file or directory)
            item_type = "file" if os.path.isfile(destination) else "directory"

            return f"Successfully renamed {item_type} from '{source}' to '{destination}'"

        except Exception as e:
            return f"Error renaming '{source}' to '{destination}': {str(e)}"
