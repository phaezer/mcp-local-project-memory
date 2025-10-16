"""Configuration for the local project memory server."""

from pathlib import Path

from pydantic import BaseModel, Field


class MemoryConfig(BaseModel):
    """Configuration for memory storage."""

    project_root: Path = Field(
        default_factory=lambda: Path.cwd(),
        description="Root directory of the project"
    )

    @property
    def memories_dir(self) -> Path:
        """Get the memories directory path."""
        return self.project_root / ".ai" / "context" / "memories"

    @property
    def instructions_file(self) -> Path:
        """Get the memory instructions file path."""
        return self.project_root / ".ai" / "context" / "memory-instructions.md"

    def ensure_directories(self) -> None:
        """Ensure all necessary directories exist."""
        self.memories_dir.mkdir(parents=True, exist_ok=True)
        self.instructions_file.parent.mkdir(parents=True, exist_ok=True)
