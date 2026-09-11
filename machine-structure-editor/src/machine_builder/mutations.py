"""Explicit visual-model mutations.

User-visible editing operations are represented as mutations instead of
allowing UI code to directly manipulate the visual model.

This is intentionally a small mechanism for V0.1. It is not yet intended to
be a full command/undo/redo framework.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .visual_model import VisualModel, VisualNode


class Mutation(Protocol):
    """Protocol implemented by all model mutations."""

    def apply(self, model: VisualModel) -> None:
        """Apply this mutation to the supplied visual model."""
        ...


@dataclass(frozen=True)
class CreateNode:
    """Create a new visual node."""

    node: VisualNode

    def apply(self, model: VisualModel) -> None:
        model.add_node(self.node)


@dataclass(frozen=True)
class MoveNode:
    """Move an existing visual node to presentation coordinates."""

    node_id: str
    x: float
    y: float

    def apply(self, model: VisualModel) -> None:
        node = model.nodes.get(self.node_id)
        if node is None:
            raise KeyError(f"Unknown visual node: {self.node_id}")

        node.x = self.x
        node.y = self.y


@dataclass(frozen=True)
class DeleteNode:
    """Delete an existing visual node."""

    node_id: str

    def apply(self, model: VisualModel) -> None:
        model.remove_node(self.node_id)


@dataclass(frozen=True)
class CreateConnection:
    """Create a visual connection between two existing visual ports."""

    connection_id: str
    source_port_id: str
    target_port_id: str
    connection_type: str = "unknown"

    def apply(self, model: VisualModel) -> None:
        from .visual_model import VisualConnection

        connection = VisualConnection(
            id=self.connection_id,
            source_port_id=self.source_port_id,
            target_port_id=self.target_port_id,
            connection_type=self.connection_type,
        )

        model.add_connection(connection)


@dataclass(frozen=True)
class DeleteConnection:
    """Delete an existing visual connection."""

    connection_id: str

    def apply(self, model: VisualModel) -> None:
        model.remove_connection(self.connection_id)