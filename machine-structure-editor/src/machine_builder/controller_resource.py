"""Canonical controller resources for Machine Builder."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .semantic_model import Provenance


@dataclass
class ControllerResource:
    """A resource provided by a machine controller."""

    id: str
    name: str
    resource_type: str
    controller_id: str | None = None

    properties: dict[str, Any] = field(
        default_factory=dict
    )

    provenance: list[Provenance] = field(
        default_factory=list
    )

    def __post_init__(self) -> None:
        """Validate the resource's basic identity."""
        if not self.id:
            raise ValueError(
                "Controller resource ID cannot be empty."
            )

        if not self.name:
            raise ValueError(
                "Controller resource name cannot be empty."
            )

        if not self.resource_type:
            raise ValueError(
                "Controller resource type cannot be empty."
            )