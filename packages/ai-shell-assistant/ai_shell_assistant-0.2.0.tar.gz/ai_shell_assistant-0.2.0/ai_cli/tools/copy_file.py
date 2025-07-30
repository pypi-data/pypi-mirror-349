"""
Copy file tool for AI CLI.
"""
import os
import shutil
from typing import Any, Dict, List

from ai_cli.tools.dangerous import DangerousTool


class CopyFileTool(DangerousTool):
    """A tool to copy files or directories from one location to another."""

    name = "copy_file"
    description = "Copy a file or directory from one location to another"

    @property
    def confirmation_message(self) -> str:
        """Get the confirmation message for the copy file tool."""
        return "Warning: You are about to copy files or directories. This could potentially overwrite existing files. Continue? (y/n): "

    @property
    def parameters(self) -> List[Dict[str, Any]]:
        """Get the parameters for the copy file tool."""
        return [
            {
                "name": "source",
                "description": "The source file or directory path to copy",
                "type": "string",
                "required": True
            },
            {
                "name": "destination",
                "description": "The destination path where the file or directory will be copied",
                "type": "string",
                "required": True
            },
            {
                "name": "overwrite",
                "description": "Whether to overwrite the destination if it already exists",
                "type": "boolean",
                "required": False
            },
            {
                "name": "recursive",
                "description": "Whether to recursively copy directories (required for directories)",
                "type": "boolean",
                "required": False
            }
        ]

    def execute(self, args: Dict[str, Any]) -> str:
        """
        Execute the copy file tool.

        Args:
            args: A dictionary containing the copy parameters.

        Returns:
            The result of the copy operation as a string.
        """
        source = args.get("source", "")
        destination = args.get("destination", "")
        overwrite = args.get("overwrite", False)
        recursive = args.get("recursive", True)  # Default to True for convenience

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
            return f"Error: Destination path '{destination}' already exists. Use 'overwrite: true' to force copy."

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

            # Perform the copy operation
            if os.path.isfile(source):
                # Copy a file
                shutil.copy2(source, destination)
                return f"Successfully copied file from '{source}' to '{destination}'"
            elif os.path.isdir(source):
                # Copy a directory
                if recursive:
                    shutil.copytree(source, destination)
                    return f"Successfully copied directory from '{source}' to '{destination}'"
                else:
                    return f"Error: '{source}' is a directory. Use 'recursive: true' to copy directories."
            else:
                return f"Error: '{source}' is neither a file nor a directory"

        except Exception as e:
            return f"Error copying '{source}' to '{destination}': {str(e)}"
