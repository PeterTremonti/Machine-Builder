from machine_builder.mutations import (
    CreateConnection,
    CreateNode,
    DeleteNode,
    MoveNode,
)
from machine_builder.store import ModelStore
from machine_builder.visual_model import (
    VisualConnection,
    VisualModel,
    VisualNode,
    VisualPort,
)


def make_node(
    node_id: str,
    node_type: str = "component",
    label: str = "Component",
) -> VisualNode:
    """Create a small test node with one port."""
    port_id = f"{node_id}-port"

    return VisualNode(
        id=node_id,
        node_type=node_type,
        label=label,
        ports={
            port_id: VisualPort(
                id=port_id,
                node_id=node_id,
                label="Interface",
                port_type="unknown",
                direction="unknown",
            )
        },
    )


def test_create_node() -> None:
    model = VisualModel()
    node = make_node("node-1")

    model.add_node(node)

    assert "node-1" in model.nodes
    assert model.nodes["node-1"].label == "Component"
    assert "node-1-port" in model.nodes["node-1"].ports


def test_duplicate_node_ids_are_rejected() -> None:
    model = VisualModel()

    model.add_node(make_node("node-1"))

    try:
        model.add_node(make_node("node-1"))
    except ValueError as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError("Duplicate node ID was not rejected")


def test_connection_uses_port_ids() -> None:
    model = VisualModel()

    node_a = make_node("node-a")
    node_b = make_node("node-b")

    model.add_node(node_a)
    model.add_node(node_b)

    connection = VisualConnection(
        id="connection-1",
        source_port_id="node-a-port",
        target_port_id="node-b-port",
        connection_type="unknown",
    )

    model.add_connection(connection)

    assert model.connections["connection-1"] is connection
    assert connection.source_port_id == "node-a-port"
    assert connection.target_port_id == "node-b-port"


def test_invalid_connection_endpoint_is_rejected() -> None:
    model = VisualModel()
    model.add_node(make_node("node-a"))

    connection = VisualConnection(
        id="connection-1",
        source_port_id="node-a-port",
        target_port_id="does-not-exist",
        connection_type="unknown",
    )

    try:
        model.add_connection(connection)
    except ValueError as exc:
        assert "Unknown target port" in str(exc)
    else:
        raise AssertionError("Invalid connection endpoint was not rejected")


def test_delete_node_removes_attached_connections() -> None:
    model = VisualModel()

    model.add_node(make_node("node-a"))
    model.add_node(make_node("node-b"))

    model.add_connection(
        VisualConnection(
            id="connection-1",
            source_port_id="node-a-port",
            target_port_id="node-b-port",
        )
    )

    model.remove_node("node-a")

    assert "node-a" not in model.nodes
    assert "connection-1" not in model.connections
    assert model.find_port("node-a-port") is None
    assert model.find_port("node-b-port") is not None


def test_store_move_and_undo_redo() -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            make_node(
                "node-1",
                node_type="motor",
                label="Motor",
            )
        )
    )

    assert store.model.nodes["node-1"].x == 0.0
    assert store.model.nodes["node-1"].y == 0.0

    store.commit(MoveNode("node-1", 250.0, 125.0))

    assert store.model.nodes["node-1"].x == 250.0
    assert store.model.nodes["node-1"].y == 125.0

    assert store.undo() is True

    assert store.model.nodes["node-1"].x == 0.0
    assert store.model.nodes["node-1"].y == 0.0

    assert store.redo() is True

    assert store.model.nodes["node-1"].x == 250.0
    assert store.model.nodes["node-1"].y == 125.0


def test_new_edit_clears_redo_history() -> None:
    store = ModelStore()

    store.commit(CreateNode(make_node("node-1")))
    store.commit(MoveNode("node-1", 100.0, 50.0))

    assert store.undo() is True
    assert store.can_redo is True

    store.commit(MoveNode("node-1", 200.0, 100.0))

    assert store.can_redo is False


def test_delete_node_can_be_undone() -> None:
    store = ModelStore()

    store.commit(CreateNode(make_node("node-1")))

    assert "node-1" in store.model.nodes

    store.commit(DeleteNode("node-1"))

    assert "node-1" not in store.model.nodes

    assert store.undo() is True

    assert "node-1" in store.model.nodes


def test_store_notifies_listeners_after_mutations() -> None:
    store = ModelStore()
    notifications: list[int] = []

    def listener(model: VisualModel) -> None:
        notifications.append(len(model.nodes))

    store.subscribe(listener)

    store.commit(CreateNode(make_node("node-1")))
    store.commit(CreateNode(make_node("node-2")))

    assert notifications == [1, 2]