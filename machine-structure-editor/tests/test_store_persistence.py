"""Tests for ModelStore persistence integration."""

from pathlib import Path

from machine_builder.mutations import CreateNode
from machine_builder.persistence import load_editor_state
from machine_builder.store import ModelStore
from machine_builder.visual_model import VisualNode


def test_store_save_preserves_complete_state(
    tmp_path: Path,
) -> None:
    store = ModelStore()

    node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Part Cooling Fan",
        x=120.0,
        y=240.0,
    )

    store.commit(
        CreateNode(
            node
        )
    )

    path = tmp_path / "machine.json"

    store.save(path)

    loaded = load_editor_state(path)

    assert (
        loaded.visual_model.nodes["node-1"].label
        == "Part Cooling Fan"
    )

    assert (
        loaded.visual_model.nodes["node-1"].x
        == 120.0
    )

    assert (
        loaded.visual_model.nodes["node-1"].y
        == 240.0
    )

    assert (
        "component-node-1"
        in loaded.semantic_model.components
    )


def test_store_save_does_not_change_history(
    tmp_path: Path,
) -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            VisualNode(
                id="node-1",
                node_type="fan",
                label="Fan",
            )
        )
    )

    assert store.can_undo
    assert not store.can_redo

    path = tmp_path / "machine.json"

    store.save(path)

    assert store.can_undo
    assert not store.can_redo


def test_store_load_replaces_complete_state(
    tmp_path: Path,
) -> None:
    source = ModelStore()

    source.commit(
        CreateNode(
            VisualNode(
                id="saved-node",
                node_type="heater",
                label="Saved Heater",
                x=50.0,
                y=75.0,
            )
        )
    )

    path = tmp_path / "machine.json"
    source.save(path)

    target = ModelStore()

    target.commit(
        CreateNode(
            VisualNode(
                id="old-node",
                node_type="fan",
                label="Old Fan",
            )
        )
    )

    assert "old-node" in target.model.nodes
    assert target.can_undo

    target.load(path)

    assert "saved-node" in target.model.nodes
    assert "old-node" not in target.model.nodes

    assert (
        target.model.nodes[
            "saved-node"
        ].label
        == "Saved Heater"
    )

    assert (
        target.semantic_model.components[
            "component-saved-node"
        ].label
        == "Saved Heater"
    )


def test_store_load_clears_history(
    tmp_path: Path,
) -> None:
    source = ModelStore()

    source.commit(
        CreateNode(
            VisualNode(
                id="saved-node",
                node_type="motor",
                label="Saved Motor",
            )
        )
    )

    path = tmp_path / "machine.json"
    source.save(path)

    target = ModelStore()

    target.commit(
        CreateNode(
            VisualNode(
                id="old-node",
                node_type="fan",
                label="Old Fan",
            )
        )
    )

    assert target.can_undo

    target.load(path)

    assert not target.can_undo
    assert not target.can_redo

    assert not target.undo()


def test_store_load_notifies_listeners(
    tmp_path: Path,
) -> None:
    source = ModelStore()

    source.commit(
        CreateNode(
            VisualNode(
                id="saved-node",
                node_type="heater",
                label="Saved Heater",
            )
        )
    )

    path = tmp_path / "machine.json"
    source.save(path)

    target = ModelStore()

    notifications: list[object] = []

    def listener(model: object) -> None:
        notifications.append(model)

    target.subscribe(listener)

    target.load(path)

    assert len(notifications) == 1
    assert notifications[0] is target.model


def test_store_save_creates_parent_directory(
    tmp_path: Path,
) -> None:
    store = ModelStore()

    path = (
        tmp_path
        / "projects"
        / "machine"
        / "machine.json"
    )

    store.save(path)

    assert path.exists()