"""
Main CLI entry point for AI CLI package.
"""
import os
from typing import Optional
import click
from ai_cli.chat import ChatSession
from ai_cli.utils.helpers import (
    print_markdown, print_success, print_error, print_user_message, print_ai_message, print_tool_message, print_header,
    print_info, print_warning, create_progress_bar, prompt_user, confirm_action
)
from ai_cli.config import config
from ai_cli.tools import AVAILABLE_TOOLS
from ai_cli.shell_executor import ShellExecutor


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="1.0.0", prog_name="AI CLI")
def main(ctx):
    """AI CLI - A command-line interface for AI chat with extensible tools.
    
    🤖 Interact with AI through natural language commands
    🛠️  Execute file operations and system commands safely
    🔧 Extensible with custom tools and integrations
    """
    if ctx.invoked_subcommand is None:
        # Show a welcome message and help when no subcommand is provided
        print_header("Welcome to AI CLI", "Your intelligent command-line assistant")
        print_info("Use 'ai-cli --help' to see available commands")
        print_markdown("**Quick Start:**\n- `ai-cli init` - Set up AI CLI configuration\n- `ai-cli chat` - Start an interactive chat session\n- `ai-cli shell` - Generate shell commands from natural language\n- `ai-cli tools` - List available tools\n- `ai-cli config-get` - View current configuration")


@main.command()
@click.option("--model", "-m", help="The OpenAI model to use",
              type=click.Choice(["gpt-4.1", "gpt-4o", "gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]),
              default=None)
@click.option("--temperature", "-t", type=float, help="The temperature for the model (0.0-2.0)")
@click.option("--max-tokens", type=int, help="The maximum number of tokens to generate")
@click.option("--system", "-s", help="System prompt to set the AI's behavior")
def chat(model: Optional[str], temperature: Optional[float], max_tokens: Optional[int], system: Optional[str]):
    """Start an interactive chat session with the AI.
    
    Examples:
        ai-cli chat
        ai-cli chat -m gpt-4o -t 0.7
        ai-cli chat --system "You are a helpful coding assistant"
    """
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
    if system:
        session.messages.append({"role": "system", "content": system})

    print_header("AI CLI Chat Session", "Type your messages and press Enter. Type 'exit' or 'quit' to end the session.")
    print_info(f"Model: {config.get('model')} | Temperature: {config.get('temperature')} | Max Tokens: {config.get('max_tokens', 'unlimited')}")
    
    # Show enabled tools
    enabled_tools = config.get('enabled_tools', [])
    if enabled_tools:
        print_markdown(f"**Enabled Tools:** {', '.join(enabled_tools)}")

    # Main chat loop
    while True:
        try:
            # Get user input with a styled prompt
            user_input = click.prompt(click.style("You", fg="cyan", bold=True), prompt_suffix=" > ")

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


@main.command("config-set")
@click.argument("key", type=click.Choice(["api_key", "model", "temperature", "max_tokens", "enabled_tools", "history_size"]))
@click.argument("value")
def config_set(key: str, value: str):
    """Set a configuration value.
    
    Examples:
        ai-cli config-set model gpt-4o
        ai-cli config-set temperature 0.7
        ai-cli config-set enabled_tools "create_file,search_file,shell_command"
    """
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


@main.command("config-get")
@click.argument("key", required=False, type=click.Choice(["api_key", "model", "temperature", "max_tokens", "enabled_tools", "history_size"], case_sensitive=False))
def config_get(key: Optional[str]):
    """Get a configuration value or all values.
    
    Examples:
        ai-cli config-get
        ai-cli config-get model
    """
    if key:
        value = config.get(key)
        if value is not None:
            print_success(f"{key} = {value}")
        else:
            print_error(f"Configuration key not found: {key}")
    else:
        # Print all configuration values
        all_config = config.get_all()
        print_header("Current Configuration", "All settings")
        for k, v in all_config.items():
            # Mask API key for security
            if k == "api_key" and v:
                display_value = v[:8] + "..." + v[-4:] if len(v) > 12 else "***"
            else:
                display_value = v
            print_markdown(f"**{k}**: `{display_value}`")


@main.command()
@click.option("--enabled-only", is_flag=True, help="Show only enabled tools")
def tools(enabled_only: bool):
    """List available tools.
    
    Examples:
        ai-cli tools
        ai-cli tools --enabled-only
    """
    print_header("Available Tools", "Tools that can be used in chat sessions")
    
    enabled_tools = config.get('enabled_tools', [])
    tools_to_show = enabled_tools if enabled_only else AVAILABLE_TOOLS.keys()

    for name, tool_class in AVAILABLE_TOOLS.items():
        if enabled_only and name not in tools_to_show:
            continue
        try:
            tool = tool_class()
            is_enabled = name in enabled_tools
            status = "✅ Enabled" if is_enabled else "❌ Disabled"
            
            print_markdown(f"### {tool.name} {status}")
            print_markdown(f"{tool.description}")

            if tool.parameters:
                print_markdown("**Parameters:**")
                for param in tool.parameters:
                    required = " *(required)*" if param.get("required", False) else ""
                    print_markdown(f"- `{param['name']}`{required}: {param['description']}")

            print()  # Empty line between tools
        except Exception as e:
            print_error(f"Error loading tool '{name}': {str(e)}")


@main.command()
@click.option("--model", "-m", help="The OpenAI model to use",
              type=click.Choice(["gpt-4.1", "gpt-4o", "gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]),
              default=None)
@click.option("--temperature", "-t", type=float, help="The temperature for the model (0.0-2.0)")
@click.option("--auto-execute", is_flag=True, help="Automatically execute generated commands (use with caution)")
def shell(model: Optional[str], temperature: Optional[float], auto_execute: bool):
    """Start an interactive shell command generator session.
    
    Examples:
        ai-cli shell
        ai-cli shell -m gpt-4o --auto-execute
    """
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
    executor.auto_execute = auto_execute

    print_header("AI Shell Command Generator", "Describe what you want to do in natural language, and AI will generate shell commands for you.")
    print_info(f"Model: {config.get('model')} | Auto-execute: {'ON' if auto_execute else 'OFF'}")
    print_markdown("**Commands:**\n- Type `exit` or `quit` to end the session\n- Type `cd <directory>` to change the working directory\n- Describe tasks in natural language")
    
    if auto_execute:
        print_warning("Auto-execute is ON. Commands will run automatically!")

    # Main shell loop
    while True:
        try:
            # Get user input with current directory in prompt
            cwd = os.getcwd()
            prompt = click.style(f"[{cwd}]", fg="blue") + " " + click.style("You", fg="cyan", bold=True)
            user_input = click.prompt(prompt, prompt_suffix=" > ")

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


@main.command()
def init():
    """Initialize AI CLI configuration interactively.
    
    This command guides you through setting up your AI CLI configuration.
    """
    print_header("AI CLI Setup Wizard", "Let's configure your AI CLI")
    
    # Check if API key is already set
    existing_api_key = os.getenv("OPENAI_API_KEY") or config.get("api_key")
    if existing_api_key:
        print_info("OpenAI API key already configured")
        if not confirm_action("Do you want to update the API key?", default=False):
            api_key = existing_api_key
        else:
            api_key = prompt_user("Enter your OpenAI API key", password=True)
            config.set("api_key", api_key)
    else:
        print_warning("No OpenAI API key found")
        api_key = prompt_user("Enter your OpenAI API key", password=True)
        config.set("api_key", api_key)
    
    # Select model
    print_markdown("\n**Available Models:**")
    models = {
        "1": ("gpt-4o", "GPT-4o - Versatile multimodal model (recommended)"),
        "2": ("gpt-4.1", "GPT-4.1 - Flagship model with major improvements"),
        "3": ("gpt-4", "GPT-4 - Advanced reasoning and instruction following"),
        "4": ("gpt-4-turbo", "GPT-4 Turbo - Older high-intelligence model"),
        "5": ("gpt-3.5-turbo", "GPT-3.5 Turbo - Faster and more economical")
    }
    
    for key, (model, desc) in models.items():
        print_markdown(f"{key}. **{model}** - {desc}")
    
    choice = prompt_user("\nSelect a model (1-5)", default="1")
    selected_model = models.get(choice, models["1"])[0]
    config.set("model", selected_model)
    
    # Configure temperature
    temp = prompt_user("\nSet temperature (0.0-2.0, higher = more creative)", default="0.7")
    try:
        config.set("temperature", float(temp))
    except ValueError:
        config.set("temperature", 0.7)
    
    # Select tools to enable
    print_markdown("\n**Available Tools:**")
    tools_list = list(AVAILABLE_TOOLS.keys())
    for i, tool in enumerate(tools_list, 1):
        print_markdown(f"{i}. {tool}")
    
    if confirm_action("\nDo you want to enable all tools?", default=True):
        config.set("enabled_tools", tools_list)
    else:
        selected_tools = []
        for tool in tools_list:
            if confirm_action(f"Enable {tool}?", default=True):
                selected_tools.append(tool)
        config.set("enabled_tools", selected_tools)
    
    # Save configuration
    if config.save():
        print_success("\nConfiguration saved successfully!")
        print_markdown("\n**Next Steps:**")
        print_markdown("- Run `ai-cli chat` to start chatting with AI")
        print_markdown("- Run `ai-cli shell` to generate shell commands")
        print_markdown("- Run `ai-cli config-get` to view your configuration")
    else:
        print_error("Failed to save configuration")


if __name__ == "__main__":
    main()
