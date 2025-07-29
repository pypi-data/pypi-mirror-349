"""Command-line interface module for TC Utils package.

This module provides the command-line interface infrastructure,
including command registration, listing, and execution capabilities.
It organizes bioinformatics tools into categories and handles
their integration with the CLI framework.
"""

from typing import Optional, Type

import typer
from rich import print
from rich.table import Table

from tc_utils.core.command import CommandBase, ToolCategory
from tc_utils.core.registry import CommandRegistry

app = typer.Typer(help="Bioinformatics Tools Collection")


def list_commands(category: Optional[ToolCategory] = None):
    """List all available commands."""
    table = Table(title="Available Commands")
    table.add_column("Category")
    table.add_column("Command")
    table.add_column("Description")
    table.add_column("Version")

    for cat in ToolCategory:
        if category and cat != category:
            continue
        commands = CommandRegistry.get_commands_by_category(cat)
        for cmd in commands:
            table.add_row(
                cat.value,
                cmd.meta.name,
                cmd.meta.description,
                cmd.meta.version,
            )

    print(table)


@app.command()
def list(category: Optional[str] = None):
    """List available commands."""
    cat = ToolCategory(category) if category else None
    list_commands(cat)


def create_typer_command(cmd_class: Type[CommandBase]):
    """Create a Typer command from a command class."""
    cmd = cmd_class()

    # 直接使用原始方法的签名
    return cmd.execute


# 修改命令注册部分
for category in ToolCategory:
    category_app = typer.Typer(
        name=category.value, help=f"{category.value.title()} analysis tools"
    )

    commands = CommandRegistry.get_commands_by_category(category)
    for cmd_class in commands:
        # 创建命令函数并注册
        command_func = create_typer_command(cmd_class)
        category_app.command(name=cmd_class.meta.name)(command_func)

    app.add_typer(category_app)
