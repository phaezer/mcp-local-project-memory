"""Memory management tools for the MCP server."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP
from pydantic import Field

from ..config import MemoryConfig


def register_tools(mcp: FastMCP, config: MemoryConfig) -> None:
    """Register all memory tools with the MCP server."""

    @mcp.tool()
    def store_memory(
        title: str = Field(description="Title/name for the memory"),
        content: str = Field(description="Content to store in the memory"),
        tags: Optional[str] = Field(
            default=None,
            description="Comma-separated tags for categorization"
        )
    ) -> dict:
        """Store a new memory as a markdown file.

        Args:
            title: Title/name for the memory (used as filename)
            content: Content to store in the memory
            tags: Optional comma-separated tags for categorization

        Returns:
            dict with success status and file path
        """
        config.ensure_directories()

        # Create safe filename from title
        safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)
        safe_title = safe_title.strip().replace(" ", "-").lower()
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{timestamp}-{safe_title}.md"

        file_path = config.memories_dir / filename

        # Create markdown content with frontmatter
        markdown_content = f"""---
title: {title}
created: {datetime.now().isoformat()}
tags: {tags if tags else ""}
---

{content}
"""

        file_path.write_text(markdown_content, encoding="utf-8")

        return {
            "success": True,
            "message": f"Memory stored successfully",
            "file_path": str(file_path),
            "title": title
        }

    @mcp.tool()
    def retrieve_memory(
        filename: str = Field(description="Filename of the memory to retrieve")
    ) -> dict:
        """Retrieve a memory by filename.

        Args:
            filename: Filename of the memory to retrieve

        Returns:
            dict with memory content and metadata
        """
        file_path = config.memories_dir / filename

        if not file_path.exists():
            return {
                "success": False,
                "error": f"Memory not found: {filename}"
            }

        content = file_path.read_text(encoding="utf-8")

        return {
            "success": True,
            "filename": filename,
            "content": content,
            "file_path": str(file_path)
        }

    @mcp.tool()
    def list_memories(
        tag_filter: Optional[str] = Field(
            default=None,
            description="Optional tag to filter memories by"
        )
    ) -> dict:
        """List all stored memories.

        Args:
            tag_filter: Optional tag to filter memories by

        Returns:
            dict with list of memory files and their metadata
        """
        config.ensure_directories()

        memories = []
        for file_path in sorted(config.memories_dir.glob("*.md")):
            content = file_path.read_text(encoding="utf-8")

            # Extract basic metadata
            lines = content.split("\n")
            title = filename = file_path.name
            tags = ""

            # Parse frontmatter if present
            if lines and lines[0].strip() == "---":
                for line in lines[1:]:
                    if line.strip() == "---":
                        break
                    if line.startswith("title:"):
                        title = line.split("title:", 1)[1].strip()
                    elif line.startswith("tags:"):
                        tags = line.split("tags:", 1)[1].strip()

            # Apply tag filter if specified
            if tag_filter and tag_filter.lower() not in tags.lower():
                continue

            memories.append({
                "filename": filename,
                "title": title,
                "tags": tags,
                "path": str(file_path)
            })

        return {
            "success": True,
            "count": len(memories),
            "memories": memories
        }

    @mcp.tool()
    def search_memories(
        query: str = Field(description="Search query to find in memory contents")
    ) -> dict:
        """Search through all memories for a query string.

        Args:
            query: Search query to find in memory contents

        Returns:
            dict with matching memories
        """
        config.ensure_directories()

        matches = []
        query_lower = query.lower()

        for file_path in config.memories_dir.glob("*.md"):
            content = file_path.read_text(encoding="utf-8")

            if query_lower in content.lower():
                # Extract title from frontmatter or use filename
                title = file_path.name
                lines = content.split("\n")
                if lines and lines[0].strip() == "---":
                    for line in lines[1:]:
                        if line.strip() == "---":
                            break
                        if line.startswith("title:"):
                            title = line.split("title:", 1)[1].strip()
                            break

                matches.append({
                    "filename": file_path.name,
                    "title": title,
                    "path": str(file_path)
                })

        return {
            "success": True,
            "query": query,
            "count": len(matches),
            "matches": matches
        }

    @mcp.tool()
    def update_memory(
        filename: str = Field(description="Filename of the memory to update"),
        content: str = Field(description="New content for the memory")
    ) -> dict:
        """Update an existing memory.

        Args:
            filename: Filename of the memory to update
            content: New content for the memory

        Returns:
            dict with success status
        """
        file_path = config.memories_dir / filename

        if not file_path.exists():
            return {
                "success": False,
                "error": f"Memory not found: {filename}"
            }

        # Read existing file to preserve frontmatter
        existing_content = file_path.read_text(encoding="utf-8")
        lines = existing_content.split("\n")

        # Preserve frontmatter if it exists
        frontmatter = []
        if lines and lines[0].strip() == "---":
            frontmatter.append(lines[0])
            for i, line in enumerate(lines[1:], 1):
                frontmatter.append(line)
                if line.strip() == "---":
                    break

        # Create updated content
        if frontmatter:
            updated_content = "\n".join(frontmatter) + "\n\n" + content
        else:
            updated_content = content

        file_path.write_text(updated_content, encoding="utf-8")

        return {
            "success": True,
            "message": "Memory updated successfully",
            "filename": filename,
            "file_path": str(file_path)
        }

    @mcp.tool()
    def delete_memory(
        filename: str = Field(description="Filename of the memory to delete")
    ) -> dict:
        """Delete a memory file.

        Args:
            filename: Filename of the memory to delete

        Returns:
            dict with success status
        """
        file_path = config.memories_dir / filename

        if not file_path.exists():
            return {
                "success": False,
                "error": f"Memory not found: {filename}"
            }

        file_path.unlink()

        return {
            "success": True,
            "message": "Memory deleted successfully",
            "filename": filename
        }

    @mcp.tool()
    def get_memory_instructions() -> dict:
        """Get instructions on how to interact with the memory system.

        Returns:
            dict with instructions content
        """
        config.ensure_directories()

        if not config.instructions_file.exists():
            # Create default instructions
            default_instructions = """# Memory System Instructions

## Overview
This memory system stores project-specific context and knowledge as markdown files.

## Usage Guidelines

### Storing Memories
- Use descriptive titles that summarize the content
- Add relevant tags for categorization
- Include context that would be helpful for future reference

### Retrieving Information
- List all memories to see what's available
- Search for specific terms or concepts
- Retrieve full memory content when needed

### Best Practices
- Keep memories focused on a single topic
- Update memories when information changes
- Use tags consistently for easier filtering
- Delete outdated or irrelevant memories

## Memory Structure
Memories are stored in `.ai/context/memories/` with timestamps and titles.
Each memory includes frontmatter with metadata (title, tags, creation date).
"""
            config.instructions_file.write_text(default_instructions, encoding="utf-8")

        content = config.instructions_file.read_text(encoding="utf-8")

        return {
            "success": True,
            "instructions": content,
            "file_path": str(config.instructions_file)
        }
