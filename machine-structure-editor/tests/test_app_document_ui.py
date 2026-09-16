"""Tests for application-level document UI wiring."""

from __future__ import annotations

import sys

import pytest
from PySide6.QtWidgets import QApplication

from machine_builder.app import (
    WINDOW_TITLE,
    _create_document_actions,
    _update_window_title,
)
from machine_builder.canvas import MachineCanvas
from machine_builder.document_controller import (
    DocumentController,
)


@pytest.fixture
def qt_app() -> QApplication:
    """Provide one QApplication for the test session."""
    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    return app


@pytest.fixture
def window_and_controller(
    qt_app: QApplication,
) -> tuple[
    MachineCanvas,
    DocumentController,
]:
    window = MachineCanvas()

    controller = DocumentController(
        window.store
    )

    return window, controller


def test_window_title_starts_with_base_title(
    window_and_controller,
) -> None:
    window, controller = window_and_controller

    _update_window_title(
        window,
        controller,
    )

    assert window.windowTitle() == WINDOW_TITLE


def test_window_title_includes_document_name(
    window_and_controller,
    tmp_path,
) -> None:
    window, controller = window_and_controller

    path = tmp_path / "promega.machine.json"

    controller.save_as(path)

    _update_window_title(
        window,
        controller,
    )

    assert (
        window.windowTitle()
        == f"{WINDOW_TITLE} — promega.machine.json"
    )


def test_window_title_marks_modified_document(
    window_and_controller,
    tmp_path,
) -> None:
    window, controller = window_and_controller

    path = tmp_path / "promega.machine.json"

    controller.save_as(path)

    controller.store.commit(
        _create_test_node_mutation()
    )

    _update_window_title(
        window,
        controller,
    )

    assert (
        window.windowTitle()
        == f"{WINDOW_TITLE} — "
        "promega.machine.json *"
    )


def test_window_title_drops_modified_marker_after_save(
    window_and_controller,
    tmp_path,
) -> None:
    window, controller = window_and_controller

    path = tmp_path / "promega.machine.json"

    controller.save_as(path)

    controller.store.commit(
        _create_test_node_mutation()
    )

    assert controller.is_modified

    controller.save()

    _update_window_title(
        window,
        controller,
    )

    assert (
        window.windowTitle()
        == f"{WINDOW_TITLE} — promega.machine.json"
    )


def test_file_menu_contains_document_actions(
    window_and_controller,
) -> None:
    window, controller = window_and_controller

    _create_document_actions(
        window,
        controller,
    )

    menus = window.menuBar().actions()

    file_menu_action = next(
        action
        for action in menus
        if action.text() == "File"
    )

    file_menu = file_menu_action.menu()

    assert file_menu is not None

    action_texts = [
        action.text()
        for action in file_menu.actions()
    ]

    assert "New" in action_texts
    assert "Open..." in action_texts
    assert "Save" in action_texts
    assert "Save As..." in action_texts


def test_document_controller_is_connected_to_existing_store(
    window_and_controller,
) -> None:
    window, controller = window_and_controller

    assert controller.store is window.store


def _create_test_node_mutation():
    from machine_builder.mutations import CreateNode
    from machine_builder.visual_model import VisualNode

    return CreateNode(
        VisualNode(
            id="test-node",
            node_type="fan",
            label="Fan",
        )
    )