"""Tests for the application document controller."""

from pathlib import Path

import pytest

from machine_builder.document_controller import (
    DocumentController,
)
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


def test_new_controller_is_untitled() -> None:
    controller = DocumentController()

    assert controller.file_path is None
    assert controller.document_name == "Untitled"
    assert not controller.is_modified


def test_save_as_establishes_document_path(
    tmp_path: Path,
) -> None:
    controller = DocumentController()

    controller.store.commit(
        CreateNode(
            make_node()
        )
    )

    path = tmp_path / "machine.json"

    controller.save_as(path)

    assert controller.file_path == path
    assert controller.document_name == "machine.json"
    assert not controller.is_modified


def test_save_uses_existing_document_path(
    tmp_path: Path,
) -> None:
    controller = DocumentController()

    controller.store.commit(
        CreateNode(
            make_node()
        )
    )

    path = tmp_path / "machine.json"

    controller.save_as(path)

    controller.store.commit(
        CreateNode(
            make_node("node-2")
        )
    )

    controller.save()

    assert controller.file_path == path
    assert not controller.is_modified


def test_save_without_path_raises() -> None:
    controller = DocumentController()

    with pytest.raises(
        ValueError,
        match="No document path specified",
    ):
        controller.save()


def test_open_replaces_current_document(
    tmp_path: Path,
) -> None:
    source = DocumentController()

    source.store.commit(
        CreateNode(
            make_node("saved-node")
        )
    )

    path = tmp_path / "saved.json"

    source.save_as(path)

    target = DocumentController()

    target.store.commit(
        CreateNode(
            make_node("old-node")
        )
    )

    target.open(path)

    assert "saved-node" in target.store.model.nodes
    assert "old-node" not in target.store.model.nodes
    assert target.file_path == path
    assert not target.is_modified


def test_new_document_resets_name_and_state(
    tmp_path: Path,
) -> None:
    controller = DocumentController()

    controller.store.commit(
        CreateNode(
            make_node()
        )
    )

    path = tmp_path / "machine.json"

    controller.save_as(path)

    controller.new_document()

    assert controller.file_path is None
    assert controller.document_name == "Untitled"
    assert not controller.is_modified
    assert controller.store.model.nodes == {}


def test_save_as_can_change_document_path(
    tmp_path: Path,
) -> None:
    controller = DocumentController()

    first = tmp_path / "first.json"
    second = tmp_path / "second.json"

    controller.store.commit(
        CreateNode(
            make_node()
        )
    )

    controller.save_as(first)
    controller.save_as(second)

    assert controller.file_path == second
    assert controller.document_name == "second.json"
    assert first.exists()
    assert second.exists()


def test_document_listener_is_notified() -> None:
    controller = DocumentController()

    notifications: list[int] = []

    def listener() -> None:
        notifications.append(1)

    controller.subscribe(listener)

    controller.new_document()

    assert notifications == [1]


def test_document_listener_is_notified_on_open(
    tmp_path: Path,
) -> None:
    source = DocumentController()

    source.store.commit(
        CreateNode(
            make_node()
        )
    )

    path = tmp_path / "machine.json"
    source.save_as(path)

    target = DocumentController()

    notifications: list[int] = []

    target.subscribe(
        lambda: notifications.append(1)
    )

    target.open(path)

    assert notifications == [1]


def test_document_listener_is_notified_on_save(
    tmp_path: Path,
) -> None:
    controller = DocumentController()

    path = tmp_path / "machine.json"

    notifications: list[int] = []

    controller.subscribe(
        lambda: notifications.append(1)
    )

    controller.save_as(path)

    assert notifications == [1]

    controller.store.commit(
        CreateNode(
            make_node("node-2")
        )
    )

    controller.save()

    assert notifications == [1, 1]


def test_document_listener_can_be_removed() -> None:
    controller = DocumentController()

    notifications: list[int] = []

    def listener() -> None:
        notifications.append(1)

    controller.subscribe(listener)
    controller.unsubscribe(listener)

    controller.new_document()

    assert notifications == []


def test_injected_store_is_used() -> None:
    store = ModelStore()
    controller = DocumentController(store)

    assert controller.store is store