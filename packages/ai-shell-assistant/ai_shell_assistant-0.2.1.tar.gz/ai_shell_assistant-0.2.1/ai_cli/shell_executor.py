"""
Shell command executor for AI CLI.

This module provides functionality to convert natural language into shell commands
and execute them safely.
"""
import os
import subprocess
import platform
from typing import Dict, List, Optional, Tuple, Any
import openai
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Confirm

from ai_cli.config import config
from ai_cli.utils.helpers import print_error, print_success, print_markdown

console = Console()


class ShellExecutor:
    """
    A class that uses AI to convert natural language into shell commands and execute them.
    """

    def __init__(self):
        """Initialize the shell executor."""
        self.history = []
        self.system_info = self._get_system_info()
        self.auto_execute = False

        # Set the OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY") or config.get("api_key")
        if api_key:
            openai.api_key = api_key

        # Model information
        self.model_info = {
            "gpt-4.1": "GPT-4.1 - Flagship model with major improvements in coding, instruction following, and long context",
            "gpt-4o": "GPT-4o - Versatile multimodal model with text, image, and audio capabilities",
            "gpt-4": "GPT-4 - Advanced reasoning and instruction following",
            "gpt-4-turbo": "GPT-4 Turbo - Older high-intelligence model, consider using GPT-4o instead",
            "gpt-3.5-turbo": "GPT-3.5 Turbo - Faster and more economical model"
        }

    def _get_system_info(self) -> Dict[str, str]:
        """
        Get information about the current system.

        Returns:
            A dictionary containing system information.
        """
        system_info = {
            "os": platform.system(),
            "cwd": os.getcwd(),
            "shell": os.environ.get("SHELL", ""),
        }

        # Add more detailed OS info
        if system_info["os"] == "Windows":
            system_info["os_version"] = platform.version()
        elif system_info["os"] == "Linux":
            try:
                with open("/etc/os-release") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            system_info["os_version"] = line.split("=")[1].strip().strip('"')
                            break
            except:
                system_info["os_version"] = platform.version()
        elif system_info["os"] == "Darwin":
            system_info["os_version"] = f"macOS {platform.mac_ver()[0]}"

        return system_info

    def generate_command(self, user_input: str) -> Tuple[str, str]:
        """
        Generate a shell command from natural language input.

        Args:
            user_input: The natural language description of what to do.

        Returns:
            A tuple containing the generated command and its explanation.
        """
        if not openai.api_key:
            raise ValueError("OpenAI API key not set")

        # Create a system message that guides the AI to generate safe and appropriate commands
        system_message = f"""
        You are a command-line assistant that converts natural language into shell commands.

        Current system information:
        - Operating System: {self.system_info['os']} {self.system_info.get('os_version', '')}
        - Current Working Directory: {self.system_info['cwd']}
        - Shell: {self.system_info['shell']}

        Guidelines for generating commands:
        1. Generate commands that are safe to execute
        2. NEVER generate commands that could cause data loss without explicit confirmation
        3. NEVER generate commands that could harm the system
        4. Be EXPLICIT and SPECIFIC - show the exact command that will run
        5. Provide a clear explanation of what the command does and why each option is used
        6. If multiple commands are needed, use appropriate operators (&&, ||, ;)
        7. If the request is ambiguous, generate the safest interpretation
        8. For destructive operations (delete, remove, etc.), include safeguards like -i for interactive mode
        9. Adapt commands to the user's operating system
        10. For complex tasks, break down into multiple commands with explanations
        11. Always include the full path or relative path when working with files
        12. For commands that might affect many files (like rm), show exactly what will be affected

        Your response should be in this format:
        ```
        <command>
        ```

        <explanation>
        """

        try:
            response = openai.chat.completions.create(
                model=config.get("model", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=500,
                temperature=0.2
            )

            content = response.choices[0].message.content

            # Extract the command and explanation
            command = ""
            explanation = content

            # Look for the command between ``` markers
            import re
            command_match = re.search(r'```(?:bash|shell|sh)?\n(.*?)\n```', content, re.DOTALL)
            if command_match:
                command = command_match.group(1).strip()
                # Remove the command block from the explanation
                explanation = re.sub(r'```(?:bash|shell|sh)?\n.*?\n```', '', content, flags=re.DOTALL).strip()

            return command, explanation

        except Exception as e:
            print_error(f"Error generating command: {str(e)}")
            return "", f"Error: {str(e)}"

    def execute_command(self, command: str) -> str:
        """
        Execute a shell command and return its output.

        Args:
            command: The shell command to execute.

        Returns:
            The output of the command.
        """
        try:
            # Execute the command and capture output
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=self.system_info["cwd"]
            )

            # Prepare the output
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                if output:
                    output += "\n"
                output += f"Error: {result.stderr}"

            # Add exit code information
            output += f"\nExit code: {result.returncode}"

            return output

        except Exception as e:
            return f"Error executing command: {str(e)}"

    def process_input(self, user_input: str) -> str:
        """
        Process natural language input, generate a command, and execute it after confirmation.

        Args:
            user_input: The natural language description of what to do.

        Returns:
            The result of the command execution.
        """
        # Generate the command
        command, explanation = self.generate_command(user_input)

        if not command:
            return "Sorry, I couldn't generate a command from your input."

        # Display the command and explanation
        console.print("\n[bold red]Command to Execute:[/bold red]")
        console.print(Panel(Syntax(command, "bash", theme="monokai", line_numbers=False), border_style="red"))

        console.print("\n[bold cyan]Explanation:[/bold cyan]")
        print_markdown(explanation)

        # Display model information
        current_model = config.get("model", "gpt-4o")
        model_description = self.model_info.get(current_model, "Custom model")
        console.print(f"\n[dim]Generated using {model_description}[/dim]")

        # Display warning for potentially dangerous commands
        if any(keyword in command.lower() for keyword in ["rm ", "rmdir", "del ", "delete", "format", "drop"]):
            console.print("\n[bold red]⚠️ WARNING: This command may delete or modify files or data. Please review carefully![/bold red]")

        # Ask for confirmation or auto-execute
        should_execute = self.auto_execute or Confirm.ask("\n[bold yellow]Do you want to execute this command?[/bold yellow]")
        
        if should_execute:
            if self.auto_execute:
                console.print("\n[bold yellow]Auto-executing command...[/bold yellow]")
            console.print("\n[bold yellow]Executing command:[/bold yellow] " + command)
            result = self.execute_command(command)

            # Display the result
            console.print("\n[bold green]Command Output:[/bold green]")
            console.print(Panel(result, border_style="green"))

            return f"Command executed: {command}\n\n{result}"
        else:
            return "Command execution cancelled."