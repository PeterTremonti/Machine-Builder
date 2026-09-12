"""Explicit visual-model mutations.

User-visible editing operations are represented as mutations instead of
allowing UI code to directly manipulate the visual model.

The important V0.1 rule is that one meaningful user action should correspond
to one mutation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .visual_model import VisualConnection, VisualModel, VisualNode


class Mutation(Protocol):
    """Protocol implemented by all model mutations."""

    def apply(
        self,
        model: VisualModel,
    ) -> None:
        """Apply this mutation to the supplied visual model."""
        ...


@dataclass(frozen=True)
class CreateNode:
    """Create a new visual node."""

    node: VisualNode

    def apply(
        self,
        model: VisualModel,
    ) -> None:
        model.add_node(
            self.node
        )


@dataclass(frozen=True)
class MoveNodes:
    """Move one or more visual nodes as one atomic user action.

    The dictionary maps each visual node ID to its final presentation
    coordinates.
    """

    positions: dict[
        str,
        tuple[float, float],
    ]

    def apply(
        self,
        model: VisualModel,
    ) -> None:
        for node_id, (
            x,
            y,
        ) in self.positions.items():
            node = model.nodes.get(
                node_id
            )

            if node is None:
                raise KeyError(
                    f"Unknown visual node: {node_id}"
                )

            node.x = x
            node.y = y


@dataclass(frozen=True)
class DeleteNodes:
    """Delete one or more visual nodes as one atomic user action."""

    node_ids: tuple[str, ...]

    def apply(
        self,
        model: VisualModel,
    ) -> None:
        for node_id in self.node_ids:
            model.remove_node(
                node_id
            )


@dataclass(frozen=True)
class CreateConnection:
    """Create a physical visual connection between two ports."""

    connection_id: str
    endpoint_a_id: str
    endpoint_b_id: str
    connection_type: str = "unknown"

    def apply(
        self,
        model: VisualModel,
    ) -> None:
        connection = VisualConnection(
            id=self.connection_id,
            endpoint_a_id=self.endpoint_a_id,
            endpoint_b_id=self.endpoint_b_id,
            connection_type=self.connection_type,
        )

        model.add_connection(
            connection
        )


@dataclass(frozen=True)
class DeleteConnection:
    """Delete an existing visual connection."""

    connection_id: str

    def apply(
        self,
        model: VisualModel,
    ) -> None:
        model.remove_connection(
            self.connection_id
        )