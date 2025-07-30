"""
AI CLI - A command-line interface for AI chat with extensible tools.

A powerful command-line interface that uses AI to convert natural language
into shell commands and provides extensible tools for file operations.
"""

__version__ = "0.2.1"
__author__ = "PierrunoYT"
__email__ = "pierrebruno@hotmail.ch"
__description__ = "AI-powered command-line interface with extensible tools"
__url__ = "https://github.com/PierrunoYT/ai-shell-assistant"

# Import main components for easier access
from ai_cli.chat import ChatSession
from ai_cli.config import config
from ai_cli.shell_executor import ShellExecutor
