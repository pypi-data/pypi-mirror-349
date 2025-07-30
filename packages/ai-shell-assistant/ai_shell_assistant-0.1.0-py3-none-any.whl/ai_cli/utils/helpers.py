"""
Helper functions for AI CLI.
"""
import os
import json
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration file.
        
    Returns:
        The configuration as a dictionary.
    """
    if not os.path.exists(config_path):
        return {}
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print_error(f"Error loading config: {str(e)}")
        return {}


def save_config(config_path: str, config: Dict[str, Any]) -> bool:
    """
    Save configuration to a JSON file.
    
    Args:
        config_path: Path to the configuration file.
        config: The configuration to save.
        
    Returns:
        True if successful, False otherwise.
    """
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print_error(f"Error saving config: {str(e)}")
        return False


def print_markdown(text: str, title: Optional[str] = None, style: str = "white on black") -> None:
    """
    Print text as markdown in a styled panel using rich.
    Args:
        text: The text to print as markdown.
        title: Optional panel title.
        style: Panel style.
    """
    panel = Panel(
        Markdown(text),
        title=title,
        border_style=style,
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)


def print_error(message: str) -> None:
    """
    Print an error message in a red panel.
    Args:
        message: The error message to print.
    """
    panel = Panel(
        Text(f"[!] {message}", style="bold red"),
        title="Error",
        border_style="red",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)


def print_success(message: str) -> None:
    """
    Print a success message in a green panel.
    Args:
        message: The success message to print.
    """
    panel = Panel(
        Text(f"✔ {message}", style="bold green"),
        title="Success",
        border_style="green",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)


def print_user_message(message: str) -> None:
    """
    Print the user's message in a blue panel.
    """
    panel = Panel(
        Text(message, style="bold cyan"),
        title="You",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)


def print_ai_message(message: str) -> None:
    """
    Print the AI's message in a purple panel.
    """
    panel = Panel(
        Markdown(message),
        title="AI",
        border_style="magenta",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)


def print_tool_message(message: str, tool_name: str) -> None:
    """
    Print a tool execution message in a yellow panel.
    """
    panel = Panel(
        Markdown(message),
        title=f"Tool: {tool_name}",
        border_style="yellow",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)


def print_header(title: str, subtitle: Optional[str] = None) -> None:
    """
    Print a modern header panel for the CLI session.
    """
    header_text = f"[bold white]{title}[/bold white]"
    if subtitle:
        header_text += f"\n[dim]{subtitle}[/dim]"
    panel = Panel(
        Text.from_markup(header_text, justify="center"),
        border_style="bright_blue",
        box=box.DOUBLE,
        padding=(1, 2)
    )
    console.print(panel)
