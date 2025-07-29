"""Command infrastructure module for TC Utils package.

This module defines the core command architecture,
including the base command class, parameter handling, tool categorization,
and command metadata. It provides the foundation for creating and managing
executable bioinformatics tools within the
package through a consistent interface and metadata structure.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from inspect import signature
from typing import Any, Dict, Optional, Type, get_type_hints

from pydantic import BaseModel


class ToolCategory(Enum):
    """Tool categories."""

    ALIGNMENT = "alignment"
    VCF = "vcf"
    RNASEQ = "rnaseq"


class CommandMeta(BaseModel):
    """Command metadata."""

    name: str
    category: ToolCategory
    description: str
    version: str
    author: str = ""
    citation: Optional[str] = None
    dependencies: Dict[str, str] = {}


@dataclass
class Parameter:
    """Command parameter metadata."""

    name: str
    type: Type
    default: Any = None
    help: str = ""
    required: bool = True


class CommandBase(ABC):
    """Base class for all commands."""

    # 将 meta 从 property 改为类属性
    meta: CommandMeta

    @abstractmethod
    def execute(self) -> Any:
        """Execute command."""
        pass

    @classmethod
    def get_parameters(cls) -> Dict[str, Parameter]:
        """Get command parameters from execute method."""
        sig = signature(cls.execute)
        hints = get_type_hints(cls.execute)
        params = {}

        for name, param in sig.parameters.items():
            if name == "self":
                continue

            param_type = hints.get(name, Any)
            default = param.default if param.default is not param.empty else None
            required = param.default is param.empty

            params[name] = Parameter(
                name=name,
                type=param_type,
                default=default,
                required=required,
                help="",  # 可以通过文档字符串或额外元数据获取
            )

        return params
