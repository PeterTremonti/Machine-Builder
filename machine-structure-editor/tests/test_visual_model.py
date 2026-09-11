from machine_builder.mutations import (
    CreateNode,
    DeleteNodes,
    MoveNodes,
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


def test_add_port_to_node() -> None:
    node = VisualNode(
        id="node-1",
        node_type="controller",
        label="Controller",
    )

    port = VisualPort(
        id="port-1",
        node_id="node-1",
        label="Power",
        port_type="power",
        direction="input",
        side="left",
        order=0,
    )

    node.add_port(port)

    assert "port-1" in node.ports
    assert node.ports["port-1"].label == "Power"
    assert node.ports["port-1"].port_type == "power"
    assert node.ports["port-1"].direction == "input"
    assert node.ports["port-1"].side == "left"


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
        node.add_port(port)
    except ValueError as exc:
        assert "belongs to node" in str(exc)
    else:
        raise AssertionError(
            "A port belonging to another node was accepted"
        )


def test_duplicate_port_ids_are_rejected() -> None:
    node = VisualNode(
        id="node-1",
        node_type="component",
        label="Component",
    )

    node.add_port(
        VisualPort(
            id="port-1",
            node_id="node-1",
        )
    )

    try:
        node.add_port(
            VisualPort(
                id="port-1",
                node_id="node-1",
            )
        )
    except ValueError as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError(
            "Duplicate port ID was not rejected"
        )


def test_find_port_and_owning_node() -> None:
    model = VisualModel()

    node = make_node("node-1")
    model.add_node(node)

    port = model.find_port("node-1-port")
    owner = model.find_node_for_port("node-1-port")

    assert port is not None
    assert port.node_id == "node-1"
    assert owner is node


def test_delete_node_removes_its_ports_and_connections() -> None:
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
    assert model.find_port("node-a-port") is None
    assert model.find_port("node-b-port") is not None
    assert "connection-1" not in model.connections


def test_store_undo_redo_for_node_creation() -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            make_node("node-1")
        )
    )

    assert "node-1" in store.model.nodes

    assert store.undo() is True

    assert "node-1" not in store.model.nodes

    assert store.redo() is True

    assert "node-1" in store.model.nodes


def test_move_nodes_is_atomic() -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            make_node("node-a")
        )
    )

    store.commit(
        CreateNode(
            make_node("node-b")
        )
    )

    store.commit(
        MoveNodes(
            positions={
                "node-a": (100.0, 200.0),
                "node-b": (300.0, 400.0),
            }
        )
    )

    assert store.model.nodes["node-a"].x == 100.0
    assert store.model.nodes["node-a"].y == 200.0
    assert store.model.nodes["node-b"].x == 300.0
    assert store.model.nodes["node-b"].y == 400.0

    assert store.undo() is True

    assert store.model.nodes["node-a"].x == 0.0
    assert store.model.nodes["node-a"].y == 0.0
    assert store.model.nodes["node-b"].x == 0.0
    assert store.model.nodes["node-b"].y == 0.0

    assert store.can_undo is True


def test_delete_nodes_is_atomic() -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            make_node("node-a")
        )
    )

    store.commit(
        CreateNode(
            make_node("node-b")
        )
    )

    store.commit(
        CreateNode(
            make_node("node-c")
        )
    )

    store.commit(
        DeleteNodes(
            node_ids=(
                "node-a",
                "node-b",
                "node-c",
            )
        )
    )

    assert store.model.nodes == {}

    assert store.undo() is True

    assert set(store.model.nodes) == {
        "node-a",
        "node-b",
        "node-c",
    }


def test_new_edit_clears_redo_history() -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            make_node("node-1")
        )
    )

    store.commit(
        MoveNodes(
            positions={
                "node-1": (100.0, 50.0),
            }
        )
    )

    assert store.undo() is True
    assert store.can_redo is True

    store.commit(
        MoveNodes(
            positions={
                "node-1": (200.0, 100.0),
            }
        )
    )

    assert store.can_redo is False


def test_delete_nodes_can_restore_everything_as_one_action() -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            make_node("node-a")
        )
    )

    store.commit(
        CreateNode(
            make_node("node-b")
        )
    )

    store.commit(
        MoveNodes(
            positions={
                "node-a": (100.0, 100.0),
                "node-b": (250.0, 150.0),
            }
        )
    )

    store.commit(
        DeleteNodes(
            node_ids=(
                "node-a",
                "node-b",
            )
        )
    )

    assert store.model.nodes == {}

    assert store.undo() is True

    assert set(store.model.nodes) == {
        "node-a",
        "node-b",
    }

    assert store.model.nodes["node-a"].x == 100.0
    assert store.model.nodes["node-a"].y == 100.0
    assert store.model.nodes["node-b"].x == 250.0
    assert store.model.nodes["node-b"].y == 150.0


def test_store_notifies_listeners_after_mutations() -> None:
    store = ModelStore()
    notifications: list[int] = []

    def listener(model: VisualModel) -> None:
        notifications.append(len(model.nodes))

    store.subscribe(listener)

    store.commit(
        CreateNode(
            make_node("node-1")
        )
    )

    store.commit(
        CreateNode(
            make_node("node-2")
        )
    )

    assert notifications == [1, 2]