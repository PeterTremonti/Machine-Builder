"""Tests for ModelStore.new_document()."""

from pathlib import Path

from machine_builder.mutations import CreateNode
from machine_builder.store import ModelStore
from machine_builder.visual_model import VisualNode


def make_node(
    node_id: str = "node-1",
) -> VisualNode:
    return VisualNode(
        id=node_id,
        node_type="fan",
        label="Fan",
    )


def test_new_document_clears_visual_model() -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            make_node()
        )
    )

    assert store.model.nodes

    store.new_document()

    assert store.model.nodes == {}


def test_new_document_clears_semantic_model() -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            make_node()
        )
    )

    assert store.semantic_model.components

    store.new_document()

    assert store.semantic_model.machines == {}
    assert store.semantic_model.components == {}


def test_new_document_clears_file_path(
    tmp_path: Path,
) -> None:
    store = ModelStore()

    path = tmp_path / "machine.json"

    store.save(path)

    assert store.file_path == path

    store.new_document()

    assert store.file_path is None


def test_new_document_clears_modified_state() -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            make_node()
        )
    )

    assert store.is_modified

    store.new_document()

    assert not store.is_modified


def test_new_document_clears_history() -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            make_node()
        )
    )

    assert store.can_undo

    store.new_document()

    assert not store.can_undo
    assert not store.can_redo


def test_new_document_prevents_undo_of_previous_document() -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            make_node()
        )
    )

    store.new_document()

    assert not store.undo()
    assert store.model.nodes == {}


def test_new_document_notifies_listeners() -> None:
    store = ModelStore()

    notifications: list[object] = []

    def listener(model: object) -> None:
        notifications.append(model)

    store.subscribe(listener)

    store.new_document()

    assert len(notifications) == 1
    assert notifications[0] is store.model


def test_new_document_can_be_used_after_loading(
    tmp_path: Path,
) -> None:
    source = ModelStore()

    source.commit(
        CreateNode(
            make_node("saved-node")
        )
    )

    path = tmp_path / "machine.json"
    source.save(path)

    target = ModelStore()
    target.load(path)

    assert "saved-node" in target.model.nodes
    assert target.file_path == path
    assert not target.is_modified

    target.new_document()

    assert target.model.nodes == {}
    assert target.file_path is None
    assert not target.is_modified
    assert not target.can_undo
    assert not target.can_redo