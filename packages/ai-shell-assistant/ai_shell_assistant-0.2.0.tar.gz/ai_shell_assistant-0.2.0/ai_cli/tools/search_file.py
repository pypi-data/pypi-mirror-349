"""
Search file tool for AI CLI.
"""
import os
import re
from typing import Any, Dict, List, Optional

from ai_cli.tools.base import BaseTool


class SearchFileTool(BaseTool):
    """A tool to search for content in files."""
    
    name = "search_file"
    description = "Search for content in files using regular expressions or plain text"
    
    @property
    def parameters(self) -> List[Dict[str, Any]]:
        """Get the parameters for the search file tool."""
        return [
            {
                "name": "query",
                "description": "The search query (text or regular expression)",
                "type": "string",
                "required": True
            },
            {
                "name": "path",
                "description": "The file or directory path to search in",
                "type": "string",
                "required": True
            },
            {
                "name": "use_regex",
                "description": "Whether to use regular expressions for searching",
                "type": "boolean",
                "required": False
            },
            {
                "name": "case_sensitive",
                "description": "Whether the search should be case-sensitive",
                "type": "boolean",
                "required": False
            },
            {
                "name": "max_results",
                "description": "Maximum number of results to return",
                "type": "integer",
                "required": False
            }
        ]
    
    def execute(self, args: Dict[str, Any]) -> str:
        """
        Execute the search file tool.
        
        Args:
            args: A dictionary containing the search parameters.
            
        Returns:
            The search results as a string.
        """
        query = args.get("query", "")
        path = args.get("path", "")
        use_regex = args.get("use_regex", False)
        case_sensitive = args.get("case_sensitive", False)
        max_results = args.get("max_results", 100)
        
        if not query:
            return "Error: No search query provided"
        
        if not path:
            return "Error: No path provided"
        
        if not os.path.exists(path):
            return f"Error: Path '{path}' does not exist"
        
        try:
            results = []
            
            # Prepare the search pattern
            if use_regex:
                try:
                    pattern = re.compile(query, flags=0 if case_sensitive else re.IGNORECASE)
                except re.error as e:
                    return f"Error: Invalid regular expression: {str(e)}"
            else:
                pattern = query
            
            # Search in a single file
            if os.path.isfile(path):
                results.extend(self._search_file(path, pattern, use_regex, case_sensitive))
            
            # Search in a directory
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        # Skip binary files and hidden files
                        if file.startswith('.') or self._is_binary(os.path.join(root, file)):
                            continue
                        
                        file_path = os.path.join(root, file)
                        file_results = self._search_file(file_path, pattern, use_regex, case_sensitive)
                        results.extend(file_results)
                        
                        # Check if we've reached the maximum number of results
                        if len(results) >= max_results:
                            results = results[:max_results]
                            break
                    
                    if len(results) >= max_results:
                        break
            
            # Format the results
            if not results:
                return f"No matches found for '{query}' in '{path}'"
            
            formatted_results = f"Found {len(results)} matches for '{query}' in '{path}':\n\n"
            for result in results:
                formatted_results += f"- {result['file']} (line {result['line_number']}): {result['line'].strip()}\n"
            
            return formatted_results
            
        except Exception as e:
            return f"Error searching files: {str(e)}"
    
    def _search_file(self, file_path: str, pattern: Any, use_regex: bool, case_sensitive: bool) -> List[Dict[str, Any]]:
        """
        Search for a pattern in a file.
        
        Args:
            file_path: The path to the file.
            pattern: The search pattern (regex or string).
            use_regex: Whether to use regular expressions.
            case_sensitive: Whether the search should be case-sensitive.
            
        Returns:
            A list of matches, each with file path, line number, and line content.
        """
        results = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    if use_regex:
                        if pattern.search(line):
                            results.append({
                                'file': file_path,
                                'line_number': i,
                                'line': line
                            })
                    else:
                        if case_sensitive:
                            if pattern in line:
                                results.append({
                                    'file': file_path,
                                    'line_number': i,
                                    'line': line
                                })
                        else:
                            if pattern.lower() in line.lower():
                                results.append({
                                    'file': file_path,
                                    'line_number': i,
                                    'line': line
                                })
        except UnicodeDecodeError:
            # Skip files that can't be decoded as text
            pass
        
        return results
    
    def _is_binary(self, file_path: str) -> bool:
        """
        Check if a file is binary.
        
        Args:
            file_path: The path to the file.
            
        Returns:
            True if the file is binary, False otherwise.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(1024)
                return False
        except UnicodeDecodeError:
            return True
