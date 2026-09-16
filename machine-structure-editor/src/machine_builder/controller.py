"""Canonical machine-controller definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .semantic_model import Provenance


@dataclass
class Controller:
    """A controller used as part of a machine."""

    id: str
    name: str
    controller_type: str
    version: str | None = None

    properties: dict[str, Any] = field(
        default_factory=dict
    )

    provenance: list[Provenance] = field(
        default_factory=list
    )

    def __post_init__(self) -> None:
        """Validate the controller's basic identity."""
        if not self.id:
            raise ValueError(
                "Controller ID cannot be empty."
            )

        if not self.name:
            raise ValueError(
                "Controller name cannot be empty."
            )

        if not self.controller_type:
            raise ValueError(
                "Controller type cannot be empty."
            )