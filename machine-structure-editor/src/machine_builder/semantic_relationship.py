"""Canonical semantic relationships for Machine Builder."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .semantic_model import Provenance


RELATIONSHIP_TYPES = frozenset(
    {
        "realizes",
        "supports",
        "requires",
        "depends_on",
        "participates_in",
    }
)


@dataclass
class SemanticRelationship:
    """A typed semantic relationship between two canonical objects."""

    id: str
    source_id: str
    target_id: str
    relationship_type: str

    properties: dict[str, Any] = field(
        default_factory=dict
    )

    provenance: list[Provenance] = field(
        default_factory=list
    )

    def __post_init__(self) -> None:
        """Validate the relationship's basic semantic structure."""
        if not self.id:
            raise ValueError(
                "Semantic relationship ID cannot be empty."
            )

        if not self.source_id:
            raise ValueError(
                "Semantic relationship source ID cannot be empty."
            )

        if not self.target_id:
            raise ValueError(
                "Semantic relationship target ID cannot be empty."
            )

        if self.source_id == self.target_id:
            raise ValueError(
                "A semantic relationship cannot reference itself."
            )

        if (
            self.relationship_type
            not in RELATIONSHIP_TYPES
        ):
            raise ValueError(
                "Unknown semantic relationship type: "
                f"{self.relationship_type}"
            )

    def connects(
        self,
        source_id: str,
        target_id: str,
    ) -> bool:
        """Return whether this relationship connects the given endpoints."""
        return (
            self.source_id == source_id
            and self.target_id == target_id
        )

    def is_type(
        self,
        relationship_type: str,
    ) -> bool:
        """Return whether this relationship has the requested type."""
        return (
            self.relationship_type
            == relationship_type
        )