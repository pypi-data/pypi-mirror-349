"""Configuration settings module for TC Utils package.

This module defines the configuration structure and default
settings for the TC Utils package using Pydantic models.
It includes settings for individual tools, tool categories,
and global application configuration such as resource allocation,
temporary directories, and logging levels.
"""

from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel, Field


class ToolSettings(BaseModel):
    """Tool-specific settings."""

    enabled: bool = True
    threads: int = 1
    memory: str = "1G"
    custom_settings: Dict[str, Any] = Field(default_factory=dict)


class CategorySettings(BaseModel):
    """Category-specific settings."""

    tools: Dict[str, ToolSettings] = Field(default_factory=dict)
    default_threads: int = 1
    default_memory: str = "1G"


class GlobalSettings(BaseModel):
    """Global settings."""

    categories: Dict[str, CategorySettings] = Field(default_factory=dict)
    temp_dir: Path = Field(default=Path("/tmp"))
    cache_dir: Path = Field(default=Path("~/.cache/tc_utils"))
    log_level: str = "INFO"
