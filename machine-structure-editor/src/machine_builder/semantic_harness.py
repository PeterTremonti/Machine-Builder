"""Canonical physical groupings of semantic wire connections."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .semantic_model import Provenance


@dataclass
class Harness:
    """A named physical grouping of direct connections and child harnesses.

    A harness groups existing canonical connections. It does not represent
    an additional electrical connection, wire, or conductor.
    """

    id: str
    name: str
    member_connection_ids: list[str] = field(default_factory=list)
    child_harness_ids: list[str] = field(default_factory=list)
    properties: dict[str, Any] = field(default_factory=dict)
    provenance: list[Provenance] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Reject malformed identity and repeated local memberships."""
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("Harness ID must be a non-empty string.")

        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Harness name must be a non-empty string.")

        for field_name, identifiers in (
            ("member connection IDs", self.member_connection_ids),
            ("child harness IDs", self.child_harness_ids),
        ):
            if not isinstance(identifiers, list):
                raise ValueError(f"Harness {field_name} must be a list.")

            if any(
                not isinstance(identifier, str) or not identifier.strip()
                for identifier in identifiers
            ):
                raise ValueError(
                    f"Harness {field_name} must contain non-empty strings."
                )

            if len(identifiers) != len(set(identifiers)):
                raise ValueError(f"Harness contains repeated {field_name}.")
