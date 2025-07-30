"""
Configuration handling for AI CLI.
"""
import os
from typing import Any, Dict, List, Optional

from ai_cli.utils.helpers import load_config, save_config

# Default configuration
DEFAULT_CONFIG = {
    "api_key": "",
    "model": "gpt-4o",  # Updated to use GPT-4o as default
    "max_tokens": 1000,
    "temperature": 0.7,
    "enabled_tools": [],  # Changed from list of tools to empty list to disable all tools
    "history_size": 10,
    "use_nlu_tool_calling": True
}

# Configuration file path
CONFIG_DIR = os.path.expanduser("~/.ai_cli")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")


class Config:
    """Configuration manager for AI CLI."""

    def __init__(self):
        """Initialize the configuration."""
        self._config = DEFAULT_CONFIG.copy()
        self.load()

    def load(self) -> None:
        """Load configuration from file."""
        loaded_config = load_config(CONFIG_PATH)
        if loaded_config:
            self._config.update(loaded_config)

    def save(self) -> bool:
        """
        Save configuration to file.

        Returns:
            True if successful, False otherwise.
        """
        return save_config(CONFIG_PATH, self._config)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: The configuration key.
            default: The default value if the key is not found.

        Returns:
            The configuration value.
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key: The configuration key.
            value: The value to set.
        """
        self._config[key] = value

    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values.

        Returns:
            A dictionary of all configuration values.
        """
        return self._config.copy()


# Global configuration instance
config = Config()
