"""
Base class for dangerous tools in AI CLI.
"""
from abc import ABC
from typing import Any, Dict, List, Optional

from ai_cli.tools.base import BaseTool


class DangerousTool(BaseTool, ABC):
    """
    Base class for tools that perform potentially dangerous operations.
    
    Dangerous tools require confirmation before execution to prevent accidental data loss.
    """
    
    dangerous = True
    
    @property
    def confirmation_message(self) -> str:
        """
        Get the confirmation message to display to the user.
        
        Returns:
            A string message asking for confirmation.
        """
        return f"Warning: The '{self.name}' tool can permanently delete or modify data. Are you sure you want to proceed? (y/n): "
