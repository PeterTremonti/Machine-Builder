"""Core visual-model data structures for the Machine Structure Editor.

The visual model is intentionally independent of Qt and independent of the
canonical Machine Builder semantic model.

It describes what the editor needs to know in order to represent and arrange
machine-related objects visually. It does not decide what those objects
ultimately mean in the canonical machine model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class VisualPort:
    """A visual interface belonging to a visual node."""

    id: str
    node_id: str
    label: str = ""
    port_type: str = "unknown"
    direction: str = "unknown"
    semantic_reference: str | None = None
    side: str = "right"
    order: int = 0


@dataclass
class VisualNode:
    """A visual object displayed in the Machine Structure Editor."""

    id: str
    node_type: str
    label: str

    x: float = 0.0
    y: float = 0.0
    width: float = 180.0
    height: float = 100.0
    rotation: float = 0.0

    semantic_reference: str | None = None

    ports: dict[str, VisualPort] = field(
        default_factory=dict
    )

    properties: dict[str, Any] = field(
        default_factory=dict
    )

    def add_port(
        self,
        port: VisualPort,
    ) -> None:
        """Add a visual port to this node."""
        if port.node_id != self.id:
            raise ValueError(
                f"Port {port.id} does not belong to node {self.id}."
            )

        if port.id in self.ports:
            raise ValueError(
                f"Visual port already exists: {port.id}"
            )

        self.ports[port.id] = port


@dataclass
class VisualConnection:
    """A physical visual connection between two visual ports.

    Endpoint ordering has no physical meaning. Signal direction, when known,
    is represented by the ports and their semantic relationships rather than
    by the physical wire.
    """

    id: str

    endpoint_a_id: str
    endpoint_b_id: str

    connection_type: str = "unknown"

    geometry: dict[str, Any] = field(
        default_factory=dict
    )

    def contains_port(
        self,
        port_id: str,
    ) -> bool:
        """Return whether this connection uses the specified port."""
        return port_id in {
            self.endpoint_a_id,
            self.endpoint_b_id,
        }


@dataclass
class VisualGroup:
    """A visual grouping of nodes and/or other groups."""

    id: str
    label: str

    node_ids: list[str] = field(
        default_factory=list
    )
    group_ids: list[str] = field(
        default_factory=list
    )

    x: float = 0.0
    y: float = 0.0
    width: float = 300.0
    height: float = 200.0

    properties: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class VisualView:
    """Persistent presentation state for one view of the visual model."""

    id: str
    name: str

    visible_node_ids: list[str] = field(
        default_factory=list
    )
    visible_group_ids: list[str] = field(
        default_factory=list
    )
    visible_connection_ids: list[str] = field(
        default_factory=list
    )

    pan_x: float = 0.0
    pan_y: float = 0.0
    zoom: float = 1.0


@dataclass
class VisualModel:
    """The persistent visual representation of a Machine Builder project."""

    nodes: dict[str, VisualNode] = field(
        default_factory=dict
    )
    connections: dict[str, VisualConnection] = field(
        default_factory=dict
    )
    groups: dict[str, VisualGroup] = field(
        default_factory=dict
    )
    views: dict[str, VisualView] = field(
        default_factory=dict
    )

    def add_node(
        self,
        node: VisualNode,
    ) -> None:
        """Add a node to the model."""
        if node.id in self.nodes:
            raise ValueError(
                f"Visual node already exists: {node.id}"
            )

        self.nodes[node.id] = node

    def remove_node(
        self,
        node_id: str,
    ) -> VisualNode:
        """Remove a node and its attached connections."""
        node = self.nodes.pop(
            node_id,
            None,
        )

        if node is None:
            raise KeyError(
                f"Unknown visual node: {node_id}"
            )

        port_ids = set(
            node.ports
        )

        connections_to_remove = [
            connection_id
            for connection_id, connection
            in self.connections.items()
            if (
                connection.endpoint_a_id in port_ids
                or connection.endpoint_b_id in port_ids
            )
        ]

        for connection_id in connections_to_remove:
            del self.connections[
                connection_id
            ]

        for group in self.groups.values():
            if node_id in group.node_ids:
                group.node_ids.remove(
                    node_id
                )

        for view in self.views.values():
            if node_id in view.visible_node_ids:
                view.visible_node_ids.remove(
                    node_id
                )

        return node

    def add_connection(
        self,
        connection: VisualConnection,
    ) -> None:
        """Add a visual connection after endpoint validation."""
        if connection.id in self.connections:
            raise ValueError(
                f"Visual connection already exists: "
                f"{connection.id}"
            )

        if self.find_port(
            connection.endpoint_a_id
        ) is None:
            raise ValueError(
                f"Unknown endpoint: "
                f"{connection.endpoint_a_id}"
            )

        if self.find_port(
            connection.endpoint_b_id
        ) is None:
            raise ValueError(
                f"Unknown endpoint: "
                f"{connection.endpoint_b_id}"
            )

        if (
            connection.endpoint_a_id
            == connection.endpoint_b_id
        ):
            raise ValueError(
                "A connection cannot connect a port to itself."
            )

        self.connections[
            connection.id
        ] = connection

    def remove_connection(
        self,
        connection_id: str,
    ) -> VisualConnection:
        """Remove and return a visual connection."""
        connection = self.connections.pop(
            connection_id,
            None,
        )

        if connection is None:
            raise KeyError(
                f"Unknown visual connection: "
                f"{connection_id}"
            )

        for view in self.views.values():
            if connection_id in view.visible_connection_ids:
                view.visible_connection_ids.remove(
                    connection_id
                )

        return connection

    def find_port(
        self,
        port_id: str,
    ) -> VisualPort | None:
        """Find a port anywhere in the visual model."""
        for node in self.nodes.values():
            port = node.ports.get(
                port_id
            )

            if port is not None:
                return port

        return None

    def find_node_for_port(
        self,
        port_id: str,
    ) -> VisualNode | None:
        """Find the node owning a particular visual port."""
        for node in self.nodes.values():
            if port_id in node.ports:
                return node

        return None