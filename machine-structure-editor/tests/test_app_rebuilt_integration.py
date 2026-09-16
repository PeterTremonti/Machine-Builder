"""Integration tests for the canonical MachineCanvas module."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QApplication

from machine_builder import app
from machine_builder.canvas import MachineCanvas
from machine_builder.document_controller import (
    DocumentController,
)


def test_application_uses_canonical_canvas_module() -> None:
    assert app.MachineCanvas is MachineCanvas


def test_canonical_canvas_has_document_store() -> None:
    application = QApplication.instance()

    if application is None:
        application = QApplication()

    window = MachineCanvas()

    controller = DocumentController(
        window.store
    )

    assert controller.store is window.store


def test_canonical_canvas_document_round_trip(
    tmp_path: Path,
) -> None:
    application = QApplication.instance()

    if application is None:
        application = QApplication()

    window = MachineCanvas()

    controller = DocumentController(
        window.store
    )

    window.create_node_from_template(
        node_type="motor",
        scene_position=(
            window._last_edit_position
        ),
    )

    path = (
        tmp_path
        / "canonical.machine.json"
    )

    controller.save_as(path)

    controller.new_document()

    assert window.store.model.nodes == {}

    controller.open(path)

    assert len(
        window.store.model.nodes
    ) == 1

    node = next(
        iter(
            window.store.model.nodes.values()
        )
    )

    assert node.node_type == "motor"


def test_canonical_canvas_undo_redo() -> None:
    application = QApplication.instance()

    if application is None:
        application = QApplication()

    window = MachineCanvas()

    window.create_node_from_template(
        node_type="sensor",
        scene_position=(
            window._last_edit_position
        ),
    )

    assert len(
        window.store.model.nodes
    ) == 1

    assert window.store.undo()

    assert (
        window.store.model.nodes
        == {}
    )

    assert window.store.redo()

    assert len(
        window.store.model.nodes
    ) == 1