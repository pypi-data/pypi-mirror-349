"""
Tools package for AI CLI.
"""

from ai_cli.tools.base import BaseTool
from ai_cli.tools.search_file import SearchFileTool
from ai_cli.tools.rename import RenameTool
from ai_cli.tools.remove import RemoveFileTool
from ai_cli.tools.create_file import CreateFileTool
from ai_cli.tools.copy_file import CopyFileTool
from ai_cli.tools.move_file import MoveFileTool
from ai_cli.tools.create_folder import CreateFolderTool

# Register all available tools
AVAILABLE_TOOLS = {
    "search_file": SearchFileTool,
    "rename": RenameTool,
    "remove": RemoveFileTool,
    "create_file": CreateFileTool,
    "copy_file": CopyFileTool,
    "move_file": MoveFileTool,
    "create_folder": CreateFolderTool,
}
