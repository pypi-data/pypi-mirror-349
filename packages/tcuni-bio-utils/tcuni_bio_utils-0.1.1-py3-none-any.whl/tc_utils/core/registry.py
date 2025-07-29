"""Command registry system for TC Utils package.

This module implements a centralized registry for managing and organizing
commands within the package. It provides functionality for registering
commands,
categorizing them by tool type, and retrieving commands by category. The
registry serves as the central point of command management and discovery in the
application.
"""

from typing import Dict, List, Type

from .command import CommandBase, ToolCategory


class CommandRegistry:
    """Command registry with category support."""

    _commands: Dict[str, Type[CommandBase]] = {}
    _categories: Dict[ToolCategory, List[str]] = {
        cat: [] for cat in ToolCategory
    }

    @classmethod
    def register(cls, command: Type[CommandBase]) -> Type[CommandBase]:
        """Register command with category."""
        # 直接访问类属性 meta
        cls._commands[command.meta.name] = command
        cls._categories[command.meta.category].append(command.meta.name)
        return command

    @classmethod
    def get_commands_by_category(
        cls, category: ToolCategory
    ) -> List[Type[CommandBase]]:
        """Get all commands in category."""
        return [cls._commands[name] for name in cls._categories[category]]

    @classmethod
    def clear(cls):
        """Clear all registered commands - helper method for testing."""
        cls._commands.clear()
        cls._categories = {cat: [] for cat in ToolCategory}
