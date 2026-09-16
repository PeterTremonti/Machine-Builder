"""Tests for ModelStore document path and modified state."""

from pathlib import Path

import pytest

from machine_builder.mutations import CreateNode
from machine_builder.semantic_model import CanonicalMachineModel
from machine_builder.store import ModelStore
from machine_builder.visual_model import VisualModel, VisualNode


def make_node(
    node_id: str = "node-1",
) -> VisualNode:
    return VisualNode(
        id=node_id,
        node_type="fan",
        label="Fan",
    )


def test_new_store_has_no_document_path() -> None:
    store = ModelStore()

    assert store.file_path is None
    assert not store.is_modified


def test_commit_marks_document_modified() -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            make_node()
        )
    )

    assert store.is_modified
    assert store.file_path is None


def test_save_sets_path_and_clears_modified(
    tmp_path: Path,
) -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            make_node()
        )
    )

    path = tmp_path / "machine.json"

    store.save(path)

    assert store.file_path == path
    assert not store.is_modified


def test_save_without_path_uses_current_document_path(
    tmp_path: Path,
) -> None:
    path = tmp_path / "machine.json"

    store = ModelStore()

    store.commit(
        CreateNode(
            make_node()
        )
    )

    store.save(path)

    store.commit(
        CreateNode(
            make_node("node-2")
        )
    )

    assert store.is_modified

    store.save()

    assert store.file_path == path
    assert not store.is_modified


def test_save_without_path_requires_existing_document_path() -> None:
    store = ModelStore()

    with pytest.raises(
        ValueError,
        match="No document path specified",
    ):
        store.save()


def test_load_sets_path_and_clears_modified(
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

    target.commit(
        CreateNode(
            make_node("old-node")
        )
    )

    assert target.is_modified

    target.load(path)

    assert target.file_path == path
    assert not target.is_modified


def test_undo_marks_document_modified(
    tmp_path: Path,
) -> None:
    store = ModelStore()

    path = tmp_path / "machine.json"

    store.save(path)

    assert not store.is_modified

    store.commit(
        CreateNode(
            make_node()
        )
    )

    assert store.is_modified

    assert store.undo()

    assert store.is_modified
    assert store.file_path == path


def test_redo_marks_document_modified(
    tmp_path: Path,
) -> None:
    store = ModelStore()

    path = tmp_path / "machine.json"

    store.save(path)

    store.commit(
        CreateNode(
            make_node()
        )
    )

    store.undo()

    store.save()

    assert not store.is_modified

    store.commit(
        CreateNode(
            make_node("node-2")
        )
    )

    assert store.undo()
    assert store.is_modified

    assert store.redo()
    assert store.is_modified


def test_replace_visual_model_marks_document_modified(
    tmp_path: Path,
) -> None:
    store = ModelStore()

    path = tmp_path / "machine.json"

    store.save(path)

    store.replace_model(
        VisualModel()
    )

    assert store.is_modified
    assert store.file_path == path


def test_replace_semantic_model_marks_document_modified(
    tmp_path: Path,
) -> None:
    store = ModelStore()

    path = tmp_path / "machine.json"

    store.save(path)

    store.replace_semantic_model(
        CanonicalMachineModel()
    )

    assert store.is_modified
    assert store.file_path == path