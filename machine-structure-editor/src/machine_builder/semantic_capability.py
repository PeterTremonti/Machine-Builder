"""Canonical capabilities for Machine Builder."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .semantic_model import Provenance


@dataclass
class Capability:
    """An ability or outcome that a machine can provide."""

    id: str
    name: str
    description: str = ""

    properties: dict[str, Any] = field(
        default_factory=dict
    )

    provenance: list[Provenance] = field(
        default_factory=list
    )

    def __post_init__(self) -> None:
        """Validate the capability's basic structure."""
        if not self.id:
            raise ValueError(
                "Capability ID cannot be empty."
            )

        if not self.name:
            raise ValueError(
                "Capability name cannot be empty."
            )