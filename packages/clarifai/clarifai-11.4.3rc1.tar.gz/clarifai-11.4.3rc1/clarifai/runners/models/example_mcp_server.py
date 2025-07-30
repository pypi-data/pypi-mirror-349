"""Example of how to create an MCP server using MCPClass."""

from typing import Dict
from fastmcp import Tool

from clarifai.runners.models.mcp_class import MCPClass


class ExampleMCPServer(MCPClass):
    """Example MCP server that provides a simple calculator tool."""

    def __init__(self):
        super().__init__()
        
        # Define and register a calculator tool
        calculator_tool = Tool(
            name="calculator",
            description="A simple calculator that can add two numbers",
            parameters={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        )
        
        @calculator_tool
        async def add(params: Dict[str, float]) -> float:
            """Add two numbers together."""
            return params["a"] + params["b"]

        # Register the tool with the MCP server
        self.add_tool(calculator_tool)


# Usage example:
if __name__ == "__main__":
    # Create and run the server
    server = ExampleMCPServer()
    
    # The server is now ready to handle MCP requests through the mcp_transport method
    # For example, a client could send a request to list tools or call the calculator
