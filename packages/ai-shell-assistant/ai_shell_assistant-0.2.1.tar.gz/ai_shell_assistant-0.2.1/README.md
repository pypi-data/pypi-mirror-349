# AI Shell Assistant

AI Shell Assistant is a command-line tool that uses AI to convert natural language into shell commands. It allows you to describe what you want to do in plain English, and the AI will generate and execute the appropriate shell commands for you.

## Warning

**USE AT YOUR OWN RISK**: This tool executes shell commands on your system. While it includes safety measures and requires confirmation before executing any command, there is always a risk when executing automatically generated commands. The authors are not responsible for any damage, data loss, or other negative consequences that may result from using this tool.

- Always carefully review commands before confirming execution
- Be especially cautious with commands that modify or delete files
- Consider running in a test environment for unfamiliar operations

## Features

- **Natural Language to Shell Commands**: Describe tasks in plain English and get the corresponding shell commands
- **Command Explanations**: Get detailed explanations of what each command does
- **Safety First**: All commands require confirmation before execution (with optional auto-execute mode)
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Interactive Chat**: Full AI chat capabilities with system prompt support
- **Rich Terminal UI**: Modern, colorful interface with progress indicators and styled prompts
- **Interactive Setup Wizard**: Easy configuration with `ai-cli init` command
- **Multiple AI Models**: Support for the latest OpenAI models including GPT-4.1 and GPT-4o
- **Extensible Tools**: File operations, search, and more tools that can be enabled/disabled
- **Enhanced Security**: Password-protected API key input and masked display

## Supported AI Models

AI Shell Assistant supports multiple OpenAI models:

- **GPT-4.1**: Flagship model with major improvements in coding, instruction following, and long context handling
- **GPT-4o** (default): Versatile multimodal model with text, image, and audio capabilities
- **GPT-4**: Advanced reasoning and instruction following
- **GPT-4-turbo**: Older high-intelligence model, consider using GPT-4o instead
- **GPT-3.5-turbo**: Faster and more economical model

## Installation

### From PyPI (Recommended)

Install the package directly from PyPI:

```bash
pip install ai-shell-assistant
```

### From Source

1. Clone this repository:
   ```bash
   git clone https://github.com/PierrunoYT/ai-shell-assistant.git
   cd ai-shell-assistant
   ```

2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

   Or install with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Quick Start

1. **Run the interactive setup wizard**:
   ```bash
   ai-cli init
   ```
   This will guide you through:
   - Setting up your OpenAI API key
   - Choosing your preferred AI model
   - Configuring temperature settings
   - Enabling/disabling tools

2. **Or set your API key manually**:
   
   **Environment Variable** (recommended):
   ```bash
   export OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   **Using the CLI**:
   ```bash
   ai-cli config-set api_key your_openai_api_key_here
   ```

## Usage

### Getting Started

Run AI CLI without any arguments to see the welcome screen and available commands:
```bash
ai-cli
```

Or use the help flag for detailed command information:
```bash
ai-cli --help
```

### Shell Command Generator

Generate shell commands from natural language descriptions:

```bash
ai-cli shell
```

With specific options:
```bash
# Use a specific model
ai-cli shell --model gpt-4.1

# Short form with auto-execute (use with caution!)
ai-cli shell -m gpt-4o --auto-execute

# Adjust temperature for more/less creative responses
ai-cli shell -t 0.3
```

Example interactions:
- "List all Python files in the current directory"
- "Find all files modified in the last 7 days"
- "Create a backup of my project folder"
- "Show me system information"

### AI Chat

Start an interactive chat session with the AI:

```bash
ai-cli chat
```

With specific options:
```bash
# Use specific model and temperature
ai-cli chat --model gpt-4.1 --temperature 0.8

# Short form with system prompt
ai-cli chat -m gpt-4o -s "You are a helpful coding assistant"

# Set max tokens
ai-cli chat --max-tokens 2000
```

### Configuration

View all configuration:
```bash
ai-cli config-get
```

View specific configuration:
```bash
ai-cli config-get model
ai-cli config-get temperature
```

Set configuration values:
```bash
ai-cli config-set key value
```

Example configurations:
```bash
# Set AI model
ai-cli config-set model gpt-4.1
ai-cli config-set model gpt-4o

# Set temperature (0.0-2.0)
ai-cli config-set temperature 0.7

# Set max tokens
ai-cli config-set max_tokens 2000

# Enable specific tools
ai-cli config-set enabled_tools "create_file,search_file,shell_command"
```

### Available Tools

List all available tools:
```bash
ai-cli tools
```

Show only enabled tools:
```bash
ai-cli tools --enabled-only
```

Tools can be enabled/disabled during setup (`ai-cli init`) or via configuration.

## Key Bindings and Commands

- **Exit**: Type `exit`, `quit`, or `q` to end a session
- **Change Directory**: In shell mode, use `cd <directory>` to navigate
- **Interrupt**: Press `Ctrl+C` to cancel current operation

## Security Considerations

- The tool uses the OpenAI API to generate commands, which means your queries are sent to OpenAI's servers
- Commands are only executed after explicit user confirmation (unless auto-execute is enabled)
- API keys are masked when displayed in configuration
- Password input is hidden when entering API keys
- Consider reviewing the generated commands carefully before execution
- For sensitive operations, verify the command's correctness independently
- Be extremely cautious when using `--auto-execute` mode

## Version History

- **v0.2.0**: Enhanced CLI with rich formatting, interactive setup wizard, auto-execute mode, and improved UX
- **v0.1.0**: Initial release with basic chat and shell command generation

## License

MIT

## Credits

Created by PierrunoYT