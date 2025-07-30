# BioContext MCP

A Python package for working with Model Context Protocol (MCP) servers,
designed for easy integration with LLMs.

## Quick Start

```python
from biocontext import MCPConnection, OpenAPIServerFactory

# Connect to an existing MCP server
async with MCPConnection("my-server") as conn:
    # Get available tools
    tools = await conn.get_tools()

    # Call a tool
    result = await conn.call_tool("tool-name", {"param": "value"})

# Create MCP servers from OpenAPI specs
factory = OpenAPIServerFactory()
servers = await factory.create_servers()
```

## Use Cases

### 1. Connecting to Existing MCP Servers

Use `MCPConnection` to connect to any MCP server and access its tools:

```python
from biocontext import MCPConnection

async def use_remote_tools():
    async with MCPConnection("my-server") as conn:
        # List available tools
        tools = await conn.get_tools()
        print(f"Available tools: {list(tools.keys())}")

        # Call a tool
        result = await conn.call_tool("search", {"query": "example"})
        print(f"Search results: {result}")
```

### 2. Creating MCP Servers from OpenAPI Specs

Use `OpenAPIServerFactory` to create MCP servers from OpenAPI specifications:

```python
from biocontext import OpenAPIServerFactory

async def create_servers():
    # Create servers from OpenAPI specs
    factory = OpenAPIServerFactory()
    servers = await factory.create_servers()

    # Use the created servers
    for server in servers:
        tools = await server.get_tools()
        print(f"Server {server.name} has tools: {list(tools.keys())}")
```

## Configuration

### OpenAPI Server Configuration

Create a `config.yaml` file in the `biocontext/config` directory:

```yaml
schemas:
  - name: example-server
    url: https://api.example.com/openapi.json
    type: json
    base: https://api.example.com
```

## Integration with LLMs

The package is designed to work seamlessly with LLMs. Here's a typical workflow:

1. Connect to or create MCP servers
2. Get available tools and their descriptions
3. Use the tools in your LLM prompts
4. Call tools based on LLM decisions

Example with an LLM:

```python
from biocontext import MCPConnection

async def llm_workflow():
    async with MCPConnection("my-server") as conn:
        # Get tool descriptions for the LLM
        tools = await conn.get_tools()

        # Example LLM prompt
        prompt = f"""
        Available tools:
        {tools}

        User request: Search for information about proteins
        """

        # LLM decides to use the search tool
        result = await conn.call_tool("search", {"query": "proteins"})
```

## Installation

```bash
pip install biocontext
```

## Requirements

- Python 3.8+
- fastmcp
- httpx
- requests
- pyyaml

## Features

- Simple interface for interacting with MCP servers
- Support for OpenAPI-based MCP servers
- Async/await support for efficient I/O operations
- Utility functions for common operations

## License

MIT License - see LICENSE file for details
