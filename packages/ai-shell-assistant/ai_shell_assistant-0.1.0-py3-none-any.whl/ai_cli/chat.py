import os
import re
import json
from typing import Any, Dict, List, Tuple
from ai_cli.utils.helpers import print_tool_message, print_ai_message
from ai_cli.config import config
from ai_cli.tools import AVAILABLE_TOOLS
import openai
from rich.console import Console

class ChatSession:
    """A chat session with the AI."""

    def __init__(self):
        """Initialize the chat session."""
        self.history = []
        self.tools = self._load_tools()
        self.console = Console()
        self.use_nlu_tool_calling = config.get("use_nlu_tool_calling", True)
        
        # Set the OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY") or config.get("api_key")
        if api_key:
            openai.api_key = api_key

    def _load_tools(self):
        """
        Load the enabled tools.

        Returns:
            A dictionary of tool instances.
        """
        enabled_tools = config.get("enabled_tools", [])
        tools = {}

        for tool_name in enabled_tools:
            if tool_name in AVAILABLE_TOOLS:
                try:
                    tool_class = AVAILABLE_TOOLS[tool_name]
                    tools[tool_name] = tool_class()
                except Exception as e:
                    from ai_cli.utils.helpers import print_error
                    print_error(f"Failed to load tool '{tool_name}': {str(e)}")

        return tools

    def get_tool_definitions(self):
        """
        Get the tool definitions for the OpenAI API.

        Returns:
            A list of tool definitions.
        """
        return [tool.to_dict() for tool in self.tools.values()]

    def detect_tool_intent(self, message: str) -> Tuple[bool, List[Dict[str, Any]]]:
        # ... (unchanged, see previous full code)
        if not self.use_nlu_tool_calling or not self.tools:
            return False, []
        try:
            system_message = """
            You are a tool intent detector. Your job is to determine if the user's message contains an intent to use one or more tools.
            If you detect a tool intent, respond with a JSON object containing the tool information:
            - For a single tool: {"tools": [{"tool_name": "name", "parameters": {"param1": "value1"}}]}
            - For multiple tools: {"tools": [{"tool_name": "name1", "parameters": {...}}, {"tool_name": "name2", "parameters": {...}}]}
            If you don't detect any tool intent, respond with: {"tools": []}
            Important: If the user's request requires multiple steps with different tools, identify ALL the tools needed and include them in the response.
            For example, if the user wants to create a file and then copy it, include both the create_file and copy_file tools.
            Special instructions for path parameters:
            - For file or directory paths, provide just the path without additional words like "directory" or "folder"
            - For example, if the user says "search in the ai_cli directory", the path should be just "ai_cli"
            - If the user mentions a file, include the file extension
            - If the user refers to "the project" or "this project", use "project" as the path
            - If the user doesn't specify a path, assume they mean the current directory and use "." as the path
            """
            tools_info = "Available tools:\n"
            for tool_name, tool in self.tools.items():
                tools_info += f"- {tool_name}: {tool.description}\n"
                tools_info += "  Parameters:\n"
                for param in tool.parameters:
                    required = " (required)" if param.get("required", False) else ""
                    tools_info += f"  - {param['name']}{required}: {param['description']}\n"
            response = openai.chat.completions.create(
                model=config.get("model", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"{tools_info}\n\nUser message: {message}"}
                ],
                max_tokens=500,
                temperature=0.2
            )
            content = response.choices[0].message.content
            try:
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    result = json.loads(json_str)
                    tools_list = result.get("tools", [])
                    if not tools_list:
                        return False, []
                    valid_tool_calls = []
                    for tool_info in tools_list:
                        tool_name = tool_info.get("tool_name")
                        params = tool_info.get("parameters", {})
                        if not tool_name or tool_name not in self.tools:
                            continue
                        if "path" in params:
                            path = params["path"]
                            if path.lower() in ["project", "this project", "the project", "current project"]:
                                path = "."
                            else:
                                for term in [" directory", " folder", " repo", " repository"]:
                                    path = path.replace(term, "")
                                path = path.strip('"\'')
                                if path.startswith("the "):
                                    path = path[4:]
                                if path.startswith("this "):
                                    path = path[5:]
                            params["path"] = path
                        if tool_name == "search_file":
                            if "path" not in params or not params["path"]:
                                params["path"] = "."
                            self.console.print(f"[dim]Searching in path: {params['path']}[/dim]")
                        valid_tool_calls.append({
                            "name": tool_name,
                            "arguments": params
                        })
                    return len(valid_tool_calls) > 0, valid_tool_calls
            except (json.JSONDecodeError, AttributeError):
                pass
            return False, []
        except Exception as e:
            from ai_cli.utils.helpers import print_error
            print_error(f"Error detecting tool intent: {str(e)}")
            return False, []

    def execute_tool(self, tool_call):
        """
        Execute a tool call from the AI.
        Args:
            tool_call: The tool call from the OpenAI API.
        Returns:
            The result of the tool execution.
        """
        if isinstance(tool_call, dict):
            tool_name = tool_call["name"]
            args = tool_call["arguments"]
        else:
            tool_name = tool_call.function.name
            try:
                args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                return "Error: Invalid JSON in tool arguments"
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found or not enabled"
        tool = self.tools[tool_name]
        # Special logic for move_file: create destination directory if needed
        if tool_name == "move_file":
            destination = args.get("destination", "")
            source = args.get("source", "")
            dest_is_dir = (
                (destination and not os.path.splitext(destination)[1]) or
                (destination.endswith(os.sep)) or
                (os.path.isdir(destination))
            )
            if dest_is_dir and not os.path.exists(destination):
                if "create_folder" in self.tools:
                    self.console.print(f"[bold cyan]Destination directory '{destination}' does not exist. Creating it with create_folder tool.[/bold cyan]")
                    folder_args = {"path": destination}
                    folder_result = self.tools["create_folder"].execute(folder_args)
                    self.console.print(f"[dim]Result from create_folder: {folder_result}[/dim]")
                if not destination.endswith(os.sep):
                    destination = destination + os.sep
                args["destination"] = os.path.join(destination, os.path.basename(source))
        if hasattr(tool, 'dangerous') and tool.dangerous:
            confirmation_msg = tool.confirmation_message
            self.console.print(f"[bold red]{confirmation_msg}[/bold red]", end="")
            confirmation = input().strip().lower()
            if confirmation != 'y' and confirmation != 'yes':
                return "Operation cancelled by user."
        try:
            result = tool.execute(args)
            print_tool_message(result, tool_name)
            return result
        except Exception as e:
            from ai_cli.utils.helpers import print_error
            print_error(f"Error executing tool '{tool_name}': {str(e)}")
            return f"Error executing tool '{tool_name}': {str(e)}"

    def execute_multiple_tools(self, tool_calls: List[Dict[str, Any]]) -> str:
        if not tool_calls:
            return "No tools to execute."
        results = []
        tool_names = []
        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_names.append(tool_name)
            self.console.print(f"[bold cyan]Executing tool: {tool_name}[/bold cyan]")
            result = self.execute_tool(tool_call)
            results.append(f"Result from {tool_name}:\n{result}")
        if len(tool_names) == 1:
            intro = f"I'll use the {tool_names[0]} tool to help with that."
        else:
            tool_list = ", ".join(tool_names[:-1]) + f" and {tool_names[-1]}"
            intro = f"I'll use the {tool_list} tools to help with that."
        combined_results = "\n\n".join(results)
        print_tool_message(f"{intro}\n\nHere's what I found:\n\n{combined_results}", "Tools")
        return f"{intro}\n\nHere's what I found:\n\n{combined_results}"

    def chat(self, message: str) -> str:
        # Check if API key is set
        if not openai.api_key:
            api_key = os.getenv("OPENAI_API_KEY") or config.get("api_key")
            if api_key:
                openai.api_key = api_key
            else:
                return "Error: OpenAI API key not set. Please set the OPENAI_API_KEY environment variable or configure it in the settings."
        
        if self.use_nlu_tool_calling and self.tools:
            has_tool_intent, tool_calls = self.detect_tool_intent(message)
            if has_tool_intent and tool_calls:
                tool_names = [tool["name"] for tool in tool_calls]
                self.console.print(f"[bold cyan]Detected tool intent: {', '.join(tool_names)}[/bold cyan]")
                combined_result = self.execute_multiple_tools(tool_calls)
                self.history.append({"role": "user", "content": message})
                self.history.append({
                    "role": "assistant",
                    "content": combined_result
                })
                print_ai_message(combined_result)
                return combined_result
        self.history.append({"role": "user", "content": message})
        history_size = config.get("history_size", 10)
        if len(self.history) > history_size * 2:
            self.history = self.history[-history_size * 2:]
        try:
            messages = self.history.copy()
            model = config.get("model", "gpt-3.5-turbo")
            max_tokens = config.get("max_tokens", 1000)
            temperature = config.get("temperature", 0.7)
            tools = self.get_tool_definitions()
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                tools=tools if tools else None,
                tool_choice="auto"
            )
            response_message = response.choices[0].message
            if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    tool_result = self.execute_tool(tool_call)
                    self.history.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": tool_call.id,
                                "type": "function",
                                "function": {
                                    "name": tool_call.function.name,
                                    "arguments": tool_call.function.arguments
                                }
                            }
                        ]
                    })
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })
                second_response = openai.chat.completions.create(
                    model=model,
                    messages=self.history,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                response_message = second_response.choices[0].message
            self.history.append({
                "role": "assistant",
                "content": response_message.content
            })
            print_ai_message(response_message.content)
            return response_message.content
        except Exception as e:
            from ai_cli.utils.helpers import print_error
            error_message = f"Error communicating with OpenAI: {str(e)}"
            print_error(error_message)
            return error_message