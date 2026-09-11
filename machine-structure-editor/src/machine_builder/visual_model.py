"""Core visual-model data structures for the Machine Structure Editor.

The visual model is intentionally independent of Qt and independent of the
canonical Machine Builder semantic model.

It describes what the editor needs to know in order to represent and arrange
machine-related objects visually.  It does not decide what those objects
ultimately mean in the canonical machine model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class VisualPort:
    """A visual interface belonging to a visual node.

    A port may optionally reference a future semantic/interface object, but
    the visual editor does not require that semantic identity to exist yet.
    """

    id: str
    node_id: str
    label: str = ""
    port_type: str = "unknown"
    direction: str = "unknown"
    semantic_reference: str | None = None


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

    ports: dict[str, VisualPort] = field(default_factory=dict)

    # Presentation properties that are persistent model data rather than
    # temporary interaction state.
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualConnection:
    """A relationship between two visual ports.

    The endpoints are port IDs rather than references to Qt objects or
    VisualPort instances.  This keeps connections stable when the renderer
    is rebuilt.
    """

    id: str
    source_port_id: str
    target_port_id: str
    connection_type: str = "unknown"

    # Renderer-specific geometry can eventually live here when routing needs
    # to be persisted.  The first milestone leaves it empty.
    geometry: dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualGroup:
    """A visual grouping of nodes and/or other groups."""

    id: str
    label: str

    node_ids: list[str] = field(default_factory=list)
    group_ids: list[str] = field(default_factory=list)

    x: float = 0.0
    y: float = 0.0
    width: float = 300.0
    height: float = 200.0

    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualView:
    """Persistent presentation state for one view of the visual model."""

    id: str
    name: str

    # Which visual objects are visible in this particular view.
    visible_node_ids: list[str] = field(default_factory=list)
    visible_group_ids: list[str] = field(default_factory=list)
    visible_connection_ids: list[str] = field(default_factory=list)

    # View transform.  These are deliberately presentation coordinates, not
    # machine coordinates.
    pan_x: float = 0.0
    pan_y: float = 0.0
    zoom: float = 1.0


@dataclass
class VisualModel:
    """The persistent visual representation of a Machine Builder project."""

    nodes: dict[str, VisualNode] = field(default_factory=dict)
    connections: dict[str, VisualConnection] = field(default_factory=dict)
    groups: dict[str, VisualGroup] = field(default_factory=dict)
    views: dict[str, VisualView] = field(default_factory=dict)

    def add_node(self, node: VisualNode) -> None:
        """Add a node to the model.

        Duplicate visual IDs are rejected because IDs are the stable identity
        used by connections, selection, persistence, and rendering.
        """
        if node.id in self.nodes:
            raise ValueError(f"Visual node already exists: {node.id}")

        self.nodes[node.id] = node

    def remove_node(self, node_id: str) -> VisualNode:
        """Remove a node and return it.

        Connections attached to ports belonging to this node are removed too.
        This keeps the visual model internally consistent when a node is
        deleted.
        """
        node = self.nodes.pop(node_id, None)
        if node is None:
            raise KeyError(f"Unknown visual node: {node_id}")

        port_ids = set(node.ports)

        connections_to_remove = [
            connection_id
            for connection_id, connection in self.connections.items()
            if (
                connection.source_port_id in port_ids
                or connection.target_port_id in port_ids
            )
        ]

        for connection_id in connections_to_remove:
            del self.connections[connection_id]

        for group in self.groups.values():
            if node_id in group.node_ids:
                group.node_ids.remove(node_id)

        for view in self.views.values():
            if node_id in view.visible_node_ids:
                view.visible_node_ids.remove(node_id)

        return node

    def add_connection(self, connection: VisualConnection) -> None:
        """Add a visual connection after endpoint validation."""
        if connection.id in self.connections:
            raise ValueError(
                f"Visual connection already exists: {connection.id}"
            )

        if not self.find_port(connection.source_port_id):
            raise ValueError(
                f"Unknown source port: {connection.source_port_id}"
            )

        if not self.find_port(connection.target_port_id):
            raise ValueError(
                f"Unknown target port: {connection.target_port_id}"
            )

        self.connections[connection.id] = connection

    def remove_connection(self, connection_id: str) -> VisualConnection:
        """Remove and return a visual connection."""
        connection = self.connections.pop(connection_id, None)
        if connection is None:
            raise KeyError(f"Unknown visual connection: {connection_id}")

        for view in self.views.values():
            if connection_id in view.visible_connection_ids:
                view.visible_connection_ids.remove(connection_id)

        return connection

    def find_port(self, port_id: str) -> VisualPort | None:
        """Find a port anywhere in the visual model."""
        for node in self.nodes.values():
            port = node.ports.get(port_id)
            if port is not None:
                return port

        return None

    def find_node_for_port(self, port_id: str) -> VisualNode | None:
        """Find the node owning a particular visual port."""
        for node in self.nodes.values():
            if port_id in node.ports:
                return node

        return None