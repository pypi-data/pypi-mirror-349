"""Unit tests for the command registry system.

This module contains test cases for the CommandRegistry class, verifying its
functionality for registering commands, managing command categories, and
retrieving commands. It tests command registration, multiple command handling,
category organization, and edge cases.
"""

from typing import Type

import pytest

from tc_utils.core.command import CommandBase, CommandMeta, ToolCategory
from tc_utils.core.registry import CommandRegistry


@pytest.fixture(autouse=True)
def setup_registry():
    """Initialize and cleanup registry for each test."""
    CommandRegistry.clear()
    yield


# 创建测试用的命令类
def create_test_command(name: str, category: ToolCategory) -> Type[CommandBase]:
    """Create test command classes."""

    class TestCommand(CommandBase):
        meta = CommandMeta(
            name=name,
            category=category,
            description="Test command",
            version="1.0.0",
        )

    return TestCommand


def test_register_command():
    """Test registering a single command."""
    test_cmd = create_test_command("test_cmd", ToolCategory.ALIGNMENT)

    registered_cmd = CommandRegistry.register(test_cmd)

    assert registered_cmd == test_cmd
    assert CommandRegistry._commands["test_cmd"] == test_cmd
    assert "test_cmd" in CommandRegistry._categories[ToolCategory.ALIGNMENT]


def test_register_multiple_commands():
    """Test registering multiple commands in different categories."""
    cmd1 = create_test_command("cmd1", ToolCategory.ALIGNMENT)
    cmd2 = create_test_command("cmd2", ToolCategory.RNASEQ)
    cmd3 = create_test_command("cmd3", ToolCategory.ALIGNMENT)

    CommandRegistry.register(cmd1)
    CommandRegistry.register(cmd2)
    CommandRegistry.register(cmd3)

    assert len(CommandRegistry._commands) == 3
    assert len(CommandRegistry._categories[ToolCategory.ALIGNMENT]) == 2
    assert len(CommandRegistry._categories[ToolCategory.RNASEQ]) == 1


def test_get_commands_by_category():
    """Test retrieving commands by category."""
    cmd1 = create_test_command("cmd1", ToolCategory.ALIGNMENT)
    cmd2 = create_test_command("cmd2", ToolCategory.RNASEQ)
    cmd3 = create_test_command("cmd3", ToolCategory.ALIGNMENT)

    CommandRegistry.register(cmd1)
    CommandRegistry.register(cmd2)
    CommandRegistry.register(cmd3)

    ass_commands = CommandRegistry.get_commands_by_category(ToolCategory.ALIGNMENT)
    utility_commands = CommandRegistry.get_commands_by_category(ToolCategory.RNASEQ)

    assert len(ass_commands) == 2
    assert len(utility_commands) == 1
    assert cmd1 in ass_commands
    assert cmd3 in ass_commands
    assert cmd2 in utility_commands


def test_get_commands_empty_category():
    """Test retrieving commands from an empty category."""
    commands = CommandRegistry.get_commands_by_category(ToolCategory.ALIGNMENT)
    assert len(commands) == 0
