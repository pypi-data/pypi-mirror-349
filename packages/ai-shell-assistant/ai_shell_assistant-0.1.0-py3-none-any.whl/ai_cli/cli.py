"""
Main CLI entry point for AI CLI package.
"""
import os
from typing import Optional
import click
from ai_cli.chat import ChatSession
from ai_cli.utils.helpers import (
    print_markdown, print_success, print_error, print_user_message, print_ai_message, print_tool_message, print_header
)
from ai_cli.config import config
from ai_cli.tools import AVAILABLE_TOOLS
from ai_cli.shell_executor import ShellExecutor


@click.group()
def main():
    """AI CLI - A command-line interface for AI chat with extensible tools."""
    pass


@main.command()
@click.option("--model", help="The OpenAI model to use",
              type=click.Choice(["gpt-4.1", "gpt-4o", "gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]),
              default=None)
@click.option("--temperature", type=float, help="The temperature for the model")
@click.option("--max-tokens", type=int, help="The maximum number of tokens to generate")
def chat(model: Optional[str], temperature: Optional[float], max_tokens: Optional[int]):
    """Start an interactive chat session with the AI."""
    # Update config if options are provided
    if model:
        config.set("model", model)
    if temperature is not None:
        config.set("temperature", temperature)
    if max_tokens is not None:
        config.set("max_tokens", max_tokens)

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY") or config.get("api_key")
    if not api_key:
        print_error("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable or configure it with 'ai-cli config set api_key YOUR_API_KEY'")
        return

    # Create chat session
    session = ChatSession()

    print_header("AI CLI Chat Session", "Type your messages and press Enter. Type 'exit' or 'quit' to end the session.")
    print_markdown(f"Using model: **{config.get('model')}**")

    # Main chat loop
    while True:
        try:
            # Get user input
            print_user_message("Type your message (or 'exit' to quit):")
            user_input = input("[You] > ")

            # Check for exit command
            if user_input.lower() in ["exit", "quit", "q"]:
                print_success("Goodbye!")
                break

            # Send message to AI
            response = session.chat(user_input)

            # The response is already printed in the chat method, so we don't need to print it again here
            # print_ai_message(response)

        except KeyboardInterrupt:
            print_success("\nGoodbye!")
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")


@main.command()
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str):
    """Set a configuration value."""
    # Handle special cases
    if key == "enabled_tools":
        try:
            # Parse comma-separated list
            tools = [t.strip() for t in value.split(",")]
            # Validate tools
            for tool in tools:
                if tool not in AVAILABLE_TOOLS:
                    print_error(f"Unknown tool: {tool}")
                    print_markdown(f"Available tools: {', '.join(AVAILABLE_TOOLS.keys())}")
                    return
            config.set(key, tools)
        except Exception as e:
            print_error(f"Error setting {key}: {str(e)}")
            return
    elif key in ["temperature", "max_tokens", "history_size"]:
        try:
            # Convert to appropriate type
            if key == "temperature":
                config.set(key, float(value))
            else:
                config.set(key, int(value))
        except ValueError:
            print_error(f"Invalid value for {key}: {value}")
            return
    else:
        # Set as string
        config.set(key, value)

    # Save the configuration
    if config.save():
        print_success(f"Configuration updated: {key} = {value}")
    else:
        print_error("Failed to save configuration")


@main.command()
@click.argument("key", required=False)
def config_get(key: Optional[str]):
    """Get a configuration value or all values."""
    if key:
        value = config.get(key)
        if value is not None:
            print_success(f"{key} = {value}")
        else:
            print_error(f"Configuration key not found: {key}")
    else:
        # Print all configuration values
        all_config = config.get_all()
        print_success("Current Configuration:")
        for k, v in all_config.items():
            print(f"  {k} = {v}")


@main.command()
def tools():
    """List available tools."""
    print_success("Available Tools:")

    for name, tool_class in AVAILABLE_TOOLS.items():
        try:
            tool = tool_class()
            print_markdown(f"### {tool.name}")
            print_markdown(f"{tool.description}")

            if tool.parameters:
                print_markdown("**Parameters:**")
                for param in tool.parameters:
                    required = " (required)" if param.get("required", False) else ""
                    print_markdown(f"- `{param['name']}`{required}: {param['description']}")

            print()  # Empty line between tools
        except Exception as e:
            print_error(f"Error loading tool '{name}': {str(e)}")


@main.command()
@click.option("--model", help="The OpenAI model to use",
              type=click.Choice(["gpt-4.1", "gpt-4o", "gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]),
              default=None)
@click.option("--temperature", type=float, help="The temperature for the model")
def shell(model: Optional[str], temperature: Optional[float]):
    """Start an interactive shell command generator session."""
    # Update config if options are provided
    if model:
        config.set("model", model)
    if temperature is not None:
        config.set("temperature", temperature)

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY") or config.get("api_key")
    if not api_key:
        print_error("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable or configure it with 'ai-cli config set api_key YOUR_API_KEY'")
        return

    # Create shell executor
    executor = ShellExecutor()

    print_header("AI Shell Command Generator", "Describe what you want to do in natural language, and AI will generate shell commands for you.")
    print_markdown(f"Using model: **{config.get('model')}**")
    print_markdown("Type 'exit' or 'quit' to end the session. Type 'cd <directory>' to change the working directory.")

    # Main shell loop
    while True:
        try:
            # Get user input
            print_user_message("What would you like to do? (or 'exit' to quit):")
            user_input = input("[You] > ")

            # Check for exit command
            if user_input.lower() in ["exit", "quit", "q"]:
                print_success("Goodbye!")
                break

            # Check for cd command to change directory
            if user_input.lower().startswith("cd "):
                try:
                    directory = user_input[3:].strip()
                    os.chdir(directory)
                    executor.system_info["cwd"] = os.getcwd()
                    print_success(f"Changed directory to: {os.getcwd()}")
                except Exception as e:
                    print_error(f"Error changing directory: {str(e)}")
                continue

            # Process the input
            result = executor.process_input(user_input)

        except KeyboardInterrupt:
            print_success("\nGoodbye!")
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
