"""Pytest configuration and shared fixtures."""

import tempfile
from pathlib import Path

import pytest

from local_project_memory.config import MemoryConfig


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def memory_config(temp_project_dir):
    """Create a memory config with temporary directory."""
    config = MemoryConfig(project_root=temp_project_dir)
    config.ensure_directories()
    return config
