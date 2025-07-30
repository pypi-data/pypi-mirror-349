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
- **Safety First**: All commands require confirmation before execution
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Interactive Chat**: Full AI chat capabilities for general assistance
- **Rich Terminal UI**: Colorful and informative terminal interface
- **Multiple AI Models**: Support for the latest OpenAI models including GPT-4.1 and GPT-4o

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

### Configuration

Set your OpenAI API key either as an environment variable or through the CLI:

1. **Environment Variable** (recommended):
   ```bash
   export OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **Using the CLI**:
   ```bash
   ai-cli config_set api_key your_openai_api_key_here
   ```

## Usage

### Shell Command Generator

Generate shell commands from natural language descriptions:

```bash
ai-cli shell
```

With specific model:
```bash
ai-cli shell --model gpt-4.1
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

With specific model and parameters:
```bash
ai-cli chat --model gpt-4.1 --temperature 0.8
```

### Configuration

View current configuration:
```bash
ai-cli config_get
```

Set configuration values:
```bash
ai-cli config_set key value
```

Example configurations:
```bash
ai-cli config_set model gpt-4.1
ai-cli config_set model gpt-4o
ai-cli config_set temperature 0.7
ai-cli config_set max_tokens 2000
```

### Available Tools

List all available tools:
```bash
ai-cli tools
```

## Security Considerations

- The tool uses the OpenAI API to generate commands, which means your queries are sent to OpenAI's servers
- Commands are only executed after explicit user confirmation
- Consider reviewing the generated commands carefully before execution
- For sensitive operations, verify the command's correctness independently

## License

MIT

## Credits

Created by PierrunoYT