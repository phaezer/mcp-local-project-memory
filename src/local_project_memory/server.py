"""Main server implementation for local project memory."""

from fastmcp import FastMCP

from .config import MemoryConfig
from .tools import register_tools

# Initialize the MCP server
mcp = FastMCP("local-project-memory")

# Initialize configuration
config = MemoryConfig()

# Ensure directories exist
config.ensure_directories()

# Register all tools
register_tools(mcp, config)
