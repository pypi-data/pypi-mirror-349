"""
Move file tool for AI CLI.
"""
import os
import shutil
from typing import Any, Dict, List

from ai_cli.tools.dangerous import DangerousTool


class MoveFileTool(DangerousTool):
    """A tool to move files or directories from one location to another."""

    name = "move_file"
    description = "Move a file or directory from one location to another"

    @property
    def confirmation_message(self) -> str:
        """Get the confirmation message for the move file tool."""
        return "Warning: You are about to move files or directories. This could potentially overwrite existing files. Continue? (y/n): "

    @property
    def parameters(self) -> List[Dict[str, Any]]:
        """Get the parameters for the move file tool."""
        return [
            {
                "name": "source",
                "description": "The source file or directory path to move",
                "type": "string",
                "required": True
            },
            {
                "name": "destination",
                "description": "The destination path where the file or directory will be moved",
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
        Execute the move file tool.

        Args:
            args: A dictionary containing the move parameters.

        Returns:
            The result of the move operation as a string.
        """
        source = args.get("source", "")
        destination = args.get("destination", "")
        overwrite = args.get("overwrite", False)

        if not source:
            return "Error: No source path provided"

        if not destination:
            return "Error: No destination path provided"

        # Normalize paths
        source = os.path.normpath(source)
        destination = os.path.normpath(destination)

        if not os.path.exists(source):
            return f"Error: Source path '{source}' does not exist"

        # Check if destination exists and handle overwrite
        if os.path.exists(destination) and not overwrite:
            return f"Error: Destination path '{destination}' already exists. Use 'overwrite: true' to force move."

        try:
            # If destination exists and overwrite is True, remove it first
            if os.path.exists(destination) and overwrite:
                if os.path.isfile(destination):
                    os.remove(destination)
                elif os.path.isdir(destination):
                    shutil.rmtree(destination)

            # Create parent directories if they don't exist
            parent_dir = os.path.dirname(destination)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            # Perform the move operation
            shutil.move(source, destination)

            # Determine what was moved (file or directory)
            item_type = "file" if os.path.isfile(destination) else "directory"

            return f"Successfully moved {item_type} from '{source}' to '{destination}'"

        except Exception as e:
            return f"Error moving '{source}' to '{destination}': {str(e)}"