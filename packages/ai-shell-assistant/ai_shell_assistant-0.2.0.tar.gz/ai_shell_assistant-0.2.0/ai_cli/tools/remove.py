"""
Remove tool for AI CLI.
"""
import os
import shutil
from typing import Any, Dict, List, Optional

from ai_cli.tools.dangerous import DangerousTool


class RemoveFileTool(DangerousTool):
    """A tool to remove files or directories."""

    name = "remove"
    description = "Remove a file or directory from the filesystem"

    @property
    def confirmation_message(self) -> str:
        """Get the confirmation message for the remove tool."""
        return "Warning: You are about to permanently delete files or directories. This action cannot be undone. Continue? (y/n): "

    @property
    def parameters(self) -> List[Dict[str, Any]]:
        """Get the parameters for the remove tool."""
        return [
            {
                "name": "path",
                "description": "The path to the file or directory to remove",
                "type": "string",
                "required": True
            },
            {
                "name": "recursive",
                "description": "Whether to recursively remove directories (required for non-empty directories)",
                "type": "boolean",
                "required": False
            },
            {
                "name": "force",
                "description": "Whether to ignore errors and force removal",
                "type": "boolean",
                "required": False
            }
        ]

    def execute(self, args: Dict[str, Any]) -> str:
        """
        Execute the remove tool.

        Args:
            args: A dictionary containing the remove parameters.

        Returns:
            The result of the remove operation as a string.
        """
        path = args.get("path", "")
        recursive = args.get("recursive", False)
        force = args.get("force", False)

        if not path:
            return "Error: No path provided"

        if not os.path.exists(path):
            return f"Error: Path '{path}' does not exist"

        try:
            if os.path.isfile(path):
                # Remove a file
                os.remove(path)
                return f"Successfully removed file '{path}'"
            else:
                # Remove a directory
                if recursive:
                    shutil.rmtree(path, ignore_errors=force)
                    return f"Successfully removed directory '{path}' and its contents"
                else:
                    try:
                        os.rmdir(path)
                        return f"Successfully removed empty directory '{path}'"
                    except OSError as e:
                        if "not empty" in str(e).lower():
                            return f"Error: Directory '{path}' is not empty. Use 'recursive: true' to remove it and its contents."
                        else:
                            raise
        except Exception as e:
            if force:
                return f"Warning: Encountered errors while removing '{path}', but continued due to force option: {str(e)}"
            else:
                return f"Error removing '{path}': {str(e)}"
