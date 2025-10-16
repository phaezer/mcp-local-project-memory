# Local Project Memory MCP Server

A Model Context Protocol (MCP) server for storing and retrieving project-specific context and memories for LLMs. This server enables AI assistants to maintain persistent knowledge about your project across sessions.

## Features

- **Store Memories**: Save project context as markdown files with metadata
- **Retrieve Memories**: Access stored information by filename
- **Search Memories**: Find relevant context using keyword search
- **List Memories**: Browse all stored memories with optional tag filtering
- **Update Memories**: Modify existing memories while preserving metadata
- **Delete Memories**: Remove outdated or irrelevant memories
- **Memory Instructions**: Get guidance on how to use the memory system

## Installation

### From Source

```bash
cd local-project-memory
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Configuration

The server stores memories in `.ai/context/memories/` within your project directory. Each memory is saved as a markdown file with frontmatter containing metadata:

```markdown
---
title: Memory Title
created: 2025-01-15T10:30:00
tags: tag1, tag2
---

Memory content goes here...
```

## Usage

### Running the Server

```bash
local-project-memory
```

Or with Python:

```bash
python -m local_project_memory
```

### Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector local-project-memory
```

### Adding to Claude Desktop

Edit your Claude Desktop config file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add the server configuration:

```json
{
  "mcpServers": {
    "local-project-memory": {
      "command": "local-project-memory"
    }
  }
}
```

Or if installed with uvx:

```json
{
  "mcpServers": {
    "local-project-memory": {
      "command": "uvx",
      "args": ["local-project-memory"]
    }
  }
}
```

Restart Claude Desktop to load the server.

## Available Tools

### store_memory
Store a new memory with title, content, and optional tags.

**Parameters:**
- `title` (string): Title/name for the memory
- `content` (string): Content to store
- `tags` (string, optional): Comma-separated tags

### retrieve_memory
Retrieve a memory by filename.

**Parameters:**
- `filename` (string): Filename of the memory to retrieve

### list_memories
List all stored memories with optional tag filtering.

**Parameters:**
- `tag_filter` (string, optional): Filter memories by tag

### search_memories
Search through all memories for a query string.

**Parameters:**
- `query` (string): Search query

### update_memory
Update an existing memory's content.

**Parameters:**
- `filename` (string): Filename of the memory to update
- `content` (string): New content

### delete_memory
Delete a memory file.

**Parameters:**
- `filename` (string): Filename of the memory to delete

### get_memory_instructions
Get instructions on how to interact with the memory system.

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src tests
ruff check src tests
```

### Type Checking

```bash
mypy src
```

## Project Structure

```
local-project-memory/
├── src/
│   └── local_project_memory/
│       ├── __init__.py
│       ├── __main__.py
│       ├── server.py          # Main server setup
│       ├── config.py          # Configuration management
│       └── tools/
│           └── __init__.py    # Memory management tools
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Test fixtures
│   └── test_tools.py         # Tool tests
├── pyproject.toml            # Project metadata and dependencies
├── pytest.ini                # Pytest configuration
└── README.md                 # This file
```

## Memory Storage

Memories are stored locally in your project at:
```
.ai/context/memories/
```

Each memory file follows the naming convention:
```
YYYYMMDD-HHMMSS-memory-title.md
```

Instructions for the memory system are stored at:
```
.ai/context/memory-instructions.md
```

## Use Cases

- **Project Context**: Store architectural decisions, patterns, and conventions
- **Code Knowledge**: Document complex implementations and their rationale
- **API Documentation**: Keep track of external APIs and their usage
- **Best Practices**: Record project-specific guidelines and standards
- **Issue Tracking**: Maintain notes about known issues and their solutions
- **Session Continuity**: Share context between different AI assistant sessions

## License

MIT

## Author

Your Name <your.email@example.com>
