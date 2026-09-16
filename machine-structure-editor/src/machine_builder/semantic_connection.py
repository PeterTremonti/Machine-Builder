"""Canonical physical connection semantics.

A SemanticConnection represents a physical relationship between two
canonical ports.

Endpoint order is intentionally not semantic. Physical electrical
connections are not inherently directional. Directional signal relationships
can be represented separately later.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .semantic_model import Provenance


@dataclass
class SemanticConnection:
    """Physical connection between two canonical ports."""

    id: str
    endpoint_a_id: str
    endpoint_b_id: str

    connection_type: str = "unknown"

    properties: dict[str, Any] = field(
        default_factory=dict
    )

    provenance: list[Provenance] = field(
        default_factory=list
    )

    def contains_port(
        self,
        port_id: str,
    ) -> bool:
        """Return whether this connection contains the given port."""
        return (
            self.endpoint_a_id == port_id
            or self.endpoint_b_id == port_id
        )

    def connects_same_ports(
        self,
        first_port_id: str,
        second_port_id: str,
    ) -> bool:
        """Return whether this connection joins the given ports."""
        return {
            self.endpoint_a_id,
            self.endpoint_b_id,
        } == {
            first_port_id,
            second_port_id,
        }

    def is_self_connection(self) -> bool:
        """Return whether both endpoints are the same port."""
        return (
            self.endpoint_a_id
            == self.endpoint_b_id
        )