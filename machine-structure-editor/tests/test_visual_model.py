from machine_builder.visual_model import (
    VisualConnection,
    VisualModel,
    VisualNode,
    VisualPort,
)


def make_node(
    node_id: str,
) -> VisualNode:
    """Create a simple test node with one port."""
    node = VisualNode(
        id=node_id,
        node_type="component",
        label=f"Node {node_id}",
    )

    node.add_port(
        VisualPort(
            id=f"{node_id}-port",
            node_id=node_id,
            label="Port",
        )
    )

    return node


def test_add_node() -> None:
    model = VisualModel()

    node = make_node(
        "node-1"
    )

    model.add_node(
        node
    )

    assert model.nodes["node-1"] is node


def test_duplicate_node_is_rejected() -> None:
    model = VisualModel()

    model.add_node(
        make_node("node-1")
    )

    try:
        model.add_node(
            make_node("node-1")
        )
    except ValueError as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError(
            "Expected duplicate node to raise ValueError."
        )


def test_port_must_belong_to_its_node() -> None:
    node = VisualNode(
        id="node-1",
        node_type="component",
        label="Component",
    )

    port = VisualPort(
        id="port-1",
        node_id="different-node",
        label="Interface",
    )

    try:
        node.add_port(
            port
        )
    except ValueError as exc:
        assert "belong to node" in str(exc)
    else:
        raise AssertionError(
            "Expected mismatched port ownership to raise ValueError."
        )


def test_duplicate_port_is_rejected() -> None:
    node = make_node(
        "node-1"
    )

    try:
        node.add_port(
            VisualPort(
                id="node-1-port",
                node_id="node-1",
                label="Duplicate",
            )
        )
    except ValueError as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError(
            "Expected duplicate port to raise ValueError."
        )


def test_find_port() -> None:
    model = VisualModel()

    node = make_node(
        "node-1"
    )

    model.add_node(
        node
    )

    assert model.find_port(
        "node-1-port"
    ) is node.ports[
        "node-1-port"
    ]

    assert model.find_port(
        "missing"
    ) is None


def test_find_node_for_port() -> None:
    model = VisualModel()

    node = make_node(
        "node-1"
    )

    model.add_node(
        node
    )

    assert model.find_node_for_port(
        "node-1-port"
    ) is node

    assert model.find_node_for_port(
        "missing"
    ) is None


def test_add_connection() -> None:
    model = VisualModel()

    model.add_node(
        make_node("node-a")
    )
    model.add_node(
        make_node("node-b")
    )

    connection = VisualConnection(
        id="connection-1",
        endpoint_a_id="node-a-port",
        endpoint_b_id="node-b-port",
    )

    model.add_connection(
        connection
    )

    assert (
        model.connections[
            "connection-1"
        ]
        is connection
    )


def test_connection_contains_port() -> None:
    connection = VisualConnection(
        id="connection-1",
        endpoint_a_id="port-a",
        endpoint_b_id="port-b",
    )

    assert connection.contains_port(
        "port-a"
    )

    assert connection.contains_port(
        "port-b"
    )

    assert not connection.contains_port(
        "port-c"
    )


def test_connection_endpoints_are_not_directional() -> None:
    connection_a = VisualConnection(
        id="connection-a",
        endpoint_a_id="port-a",
        endpoint_b_id="port-b",
    )

    connection_b = VisualConnection(
        id="connection-b",
        endpoint_a_id="port-b",
        endpoint_b_id="port-a",
    )

    assert {
        connection_a.endpoint_a_id,
        connection_a.endpoint_b_id,
    } == {
        connection_b.endpoint_a_id,
        connection_b.endpoint_b_id,
    }


def test_connection_cannot_use_same_endpoint_twice() -> None:
    model = VisualModel()

    model.add_node(
        make_node("node-a")
    )

    try:
        model.add_connection(
            VisualConnection(
                id="connection-1",
                endpoint_a_id="node-a-port",
                endpoint_b_id="node-a-port",
            )
        )
    except ValueError as exc:
        assert "cannot connect a port to itself" in str(exc)
    else:
        raise AssertionError(
            "Expected self-connection to raise ValueError."
        )


def test_delete_node_removes_its_ports_and_connections() -> None:
    model = VisualModel()

    model.add_node(
        make_node("node-a")
    )
    model.add_node(
        make_node("node-b")
    )

    model.add_connection(
        VisualConnection(
            id="connection-1",
            endpoint_a_id="node-a-port",
            endpoint_b_id="node-b-port",
        )
    )

    assert "connection-1" in model.connections

    model.remove_node(
        "node-a"
    )

    assert "node-a" not in model.nodes
    assert "connection-1" not in model.connections


def test_remove_connection() -> None:
    model = VisualModel()

    model.add_node(
        make_node("node-a")
    )
    model.add_node(
        make_node("node-b")
    )

    model.add_connection(
        VisualConnection(
            id="connection-1",
            endpoint_a_id="node-a-port",
            endpoint_b_id="node-b-port",
        )
    )

    connection = model.remove_connection(
        "connection-1"
    )

    assert connection.id == "connection-1"
    assert "connection-1" not in model.connections


def test_remove_unknown_connection_is_rejected() -> None:
    model = VisualModel()

    try:
        model.remove_connection(
            "missing"
        )
    except KeyError as exc:
        assert "Unknown visual connection" in str(exc)
    else:
        raise AssertionError(
            "Expected unknown connection removal to raise KeyError."
        )