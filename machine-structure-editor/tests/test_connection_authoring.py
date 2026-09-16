"""Tests for authoring connections across the visual and semantic models."""

import pytest

from machine_builder.mutations import (
    CreateConnection,
    CreateNode,
    DeleteConnection,
)
from machine_builder.store import ModelStore
from machine_builder.visual_model import (
    VisualNode,
    VisualPort,
)


def build_fan_node(
    node_id: str,
) -> VisualNode:
    """Build a simple visual fan node for connection tests."""
    node = VisualNode(
        id=node_id,
        node_type="part_cooling_fan",
        label="Part Cooling Fan",
    )

    node.ports[
        f"{node_id}-power"
    ] = VisualPort(
        id=f"{node_id}-power",
        node_id=node.id,
        label="Power",
        port_type="power",
        direction="input",
        side="left",
        order=0,
    )

    node.ports[
        f"{node_id}-ground"
    ] = VisualPort(
        id=f"{node_id}-ground",
        node_id=node.id,
        label="Ground",
        port_type="electrical",
        direction="input",
        side="left",
        order=1,
    )

    return node


def create_two_fans() -> ModelStore:
    """Create two canonical fan components for connection tests."""
    store = ModelStore()

    store.commit(
        CreateNode(
            build_fan_node("fan-a")
        )
    )

    store.commit(
        CreateNode(
            build_fan_node("fan-b")
        )
    )

    return store


def test_connection_creates_visual_and_semantic_connections() -> None:
    store = create_two_fans()

    store.commit(
        CreateConnection(
            connection_id="connection-1",
            endpoint_a_id="fan-a-power",
            endpoint_b_id="fan-b-ground",
        )
    )

    assert (
        "connection-1"
        in store.model.connections
    )

    assert (
        "connection-1"
        in store.semantic_model.connections
    )

    semantic_connection = (
        store.semantic_model.connections[
            "connection-1"
        ]
    )

    assert {
        semantic_connection.endpoint_a_id,
        semantic_connection.endpoint_b_id,
    } == {
        "component-fan-a-power",
        "component-fan-b-ground",
    }


def test_connection_preserves_visual_endpoint_identity() -> None:
    store = create_two_fans()

    store.commit(
        CreateConnection(
            connection_id="connection-1",
            endpoint_a_id="fan-a-power",
            endpoint_b_id="fan-b-ground",
        )
    )

    visual_connection = (
        store.model.connections[
            "connection-1"
        ]
    )

    assert (
        visual_connection.endpoint_a_id
        == "fan-a-power"
    )

    assert (
        visual_connection.endpoint_b_id
        == "fan-b-ground"
    )


def test_visual_only_connection_remains_supported() -> None:
    store = ModelStore()

    node_a = VisualNode(
        id="node-a",
        node_type="test",
        label="Node A",
    )

    node_a.ports[
        "node-a-port"
    ] = VisualPort(
        id="node-a-port",
        node_id=node_a.id,
        label="A",
        direction="unknown",
        side="right",
        order=0,
    )

    node_b = VisualNode(
        id="node-b",
        node_type="test",
        label="Node B",
    )

    node_b.ports[
        "node-b-port"
    ] = VisualPort(
        id="node-b-port",
        node_id=node_b.id,
        label="B",
        direction="unknown",
        side="left",
        order=0,
    )

    store.commit(
        CreateNode(
            node_a
        )
    )

    store.commit(
        CreateNode(
            node_b
        )
    )

    store.commit(
        CreateConnection(
            connection_id="connection-visual-only",
            endpoint_a_id="node-a-port",
            endpoint_b_id="node-b-port",
        )
    )

    assert (
        "connection-visual-only"
        in store.model.connections
    )

    assert (
        "connection-visual-only"
        not in store.semantic_model.connections
    )


def test_reverse_semantic_connection_is_rejected() -> None:
    store = create_two_fans()

    store.commit(
        CreateConnection(
            connection_id="connection-1",
            endpoint_a_id="fan-a-power",
            endpoint_b_id="fan-b-ground",
        )
    )

    with pytest.raises(
        ValueError,
        match="That canonical connection already exists",
    ):
        store.commit(
            CreateConnection(
                connection_id="connection-2",
                endpoint_a_id="fan-b-ground",
                endpoint_b_id="fan-a-power",
            )
        )

    assert (
        "connection-2"
        not in store.model.connections
    )

    assert (
        "connection-2"
        not in store.semantic_model.connections
    )


def test_invalid_canonical_reference_is_rejected_before_visual_connection_creation() -> None:
    store = create_two_fans()

    store.model.nodes[
        "fan-a"
    ].ports[
        "fan-a-power"
    ].semantic_reference = (
        "missing-canonical-port"
    )

    with pytest.raises(
        ValueError,
        match="Visual port references unknown canonical port",
    ):
        store.commit(
            CreateConnection(
                connection_id="connection-invalid",
                endpoint_a_id="fan-a-power",
                endpoint_b_id="fan-b-ground",
            )
        )

    assert (
        "connection-invalid"
        not in store.model.connections
    )

    assert (
        "connection-invalid"
        not in store.semantic_model.connections
    )


def test_delete_connection_removes_visual_and_semantic_connections() -> None:
    store = create_two_fans()

    store.commit(
        CreateConnection(
            connection_id="connection-1",
            endpoint_a_id="fan-a-power",
            endpoint_b_id="fan-b-ground",
        )
    )

    store.commit(
        DeleteConnection(
            connection_id="connection-1"
        )
    )

    assert (
        "connection-1"
        not in store.model.connections
    )

    assert (
        "connection-1"
        not in store.semantic_model.connections
    )


def test_connection_undo_restores_both_connections() -> None:
    store = create_two_fans()

    store.commit(
        CreateConnection(
            connection_id="connection-1",
            endpoint_a_id="fan-a-power",
            endpoint_b_id="fan-b-ground",
        )
    )

    assert (
        "connection-1"
        in store.model.connections
    )

    assert (
        "connection-1"
        in store.semantic_model.connections
    )

    store.undo()

    assert (
        "connection-1"
        not in store.model.connections
    )

    assert (
        "connection-1"
        not in store.semantic_model.connections
    )

    store.redo()

    assert (
        "connection-1"
        in store.model.connections
    )

    assert (
        "connection-1"
        in store.semantic_model.connections
    )


def test_deleting_connection_undo_restores_both_connections() -> None:
    store = create_two_fans()

    store.commit(
        CreateConnection(
            connection_id="connection-1",
            endpoint_a_id="fan-a-power",
            endpoint_b_id="fan-b-ground",
        )
    )

    store.commit(
        DeleteConnection(
            connection_id="connection-1"
        )
    )

    assert (
        "connection-1"
        not in store.model.connections
    )

    assert (
        "connection-1"
        not in store.semantic_model.connections
    )

    store.undo()

    assert (
        "connection-1"
        in store.model.connections
    )

    assert (
        "connection-1"
        in store.semantic_model.connections
    )

    store.redo()

    assert (
        "connection-1"
        not in store.model.connections
    )

    assert (
        "connection-1"
        not in store.semantic_model.connections
    )