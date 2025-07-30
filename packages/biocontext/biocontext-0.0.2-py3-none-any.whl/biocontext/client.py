"""MCP connection implementation."""

from typing import Any

from fastmcp import Client, FastMCP


class MCPConnectionError(Exception):
    """Base exception for MCP connection errors."""


class MCPNotInitializedError(MCPConnectionError):
    """Raised when trying to use an uninitialized MCP connection."""


class MCPConnection:
    """A connection to an MCP server.

    This class provides a simple interface to connect to and interact with an existing MCP server.
    It handles the basic operations like getting available tools and resources, and calling tools.
    """

    def __init__(self, name: str, base_url: str | None = None):
        """Initialize the MCP connection.

        Args:
            name: The name of the MCP server to connect to
            base_url: Optional base URL for HTTP-based MCP servers
        """
        self.name = name
        self.base_url = base_url
        self._client = None
        self._mcp = FastMCP(name=name, stateless_http=True)

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = Client(self._mcp)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    async def get_tools(self) -> dict[str, Any]:
        """Get all available tools from the MCP server."""
        if not self._client:
            raise MCPNotInitializedError()
        return await self._client.get_tools()

    async def get_resources(self) -> dict[str, Any]:
        """Get all available resources from the MCP server."""
        if not self._client:
            raise MCPNotInitializedError()
        return await self._client.get_resources()

    async def call_tool(self, tool_name: str, params: dict[str, Any]) -> list[Any]:
        """Call a specific tool on the MCP server.

        Args:
            tool_name: Name of the tool to call
            params: Parameters to pass to the tool

        Returns:
            List of results from the tool call
        """
        if not self._client:
            raise MCPNotInitializedError()
        return await self._client.call_tool(tool_name, params)
