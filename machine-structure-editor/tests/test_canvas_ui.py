"""Tests for the canvas UI construction mixin."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QPushButton

from machine_builder.canvas import MachineCanvas
from machine_builder.canvas_ui import CanvasUIMixin


def _application() -> QApplication:
    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    return app


def test_canonical_canvas_uses_ui_mixin() -> None:
    _application()

    canvas = MachineCanvas()

    assert isinstance(
        canvas,
        CanvasUIMixin,
    )


def test_canonical_canvas_has_view() -> None:
    _application()

    canvas = MachineCanvas()

    assert canvas.view is not None
    assert canvas.scene is not None


def test_canonical_canvas_has_palette() -> None:
    _application()

    canvas = MachineCanvas()

    assert canvas.palette.count() >= 7


def test_canonical_canvas_has_status_bar() -> None:
    _application()

    canvas = MachineCanvas()

    assert canvas.statusBar() is not None


def test_canonical_canvas_has_editor_actions() -> None:
    _application()

    canvas = MachineCanvas()

    shortcuts = {
        action.shortcut().toString()
        for action in canvas.actions()
    }

    action_texts = {
        action.text()
        for action in canvas.actions()
    }

    assert "Delete" in action_texts
    assert "Edit Component..." in action_texts
    assert "Edit Controller..." in action_texts
    assert "Ctrl+Z" in shortcuts
    assert "Ctrl+Y" in shortcuts
    assert "F" in shortcuts
    assert "Ctrl+E" in shortcuts
    assert "Ctrl+Shift+E" in shortcuts


def test_canonical_canvas_has_selection_inspector() -> None:
    _application()

    canvas = MachineCanvas()

    assert (
        canvas.selection_inspector is not None
    )


def test_selection_inspector_has_precision_nudge_controls() -> None:
    _application()

    canvas = MachineCanvas()
    inspector = canvas.selection_inspector

    assert inspector._nudge_step.value() == 1.0

    buttons = {
        button.text()
        for button in inspector.findChildren(
            QPushButton
        )
    }

    assert {
        "?",
        "?",
        "?",
        "?",
    }.issubset(
        buttons
    )


def test_selection_inspector_is_not_the_scene_view() -> None:
    _application()

    canvas = MachineCanvas()

    assert (
        canvas.selection_inspector
        is not canvas.view
    )

def test_port_detail_selector_labels_match_per_port_filtering_before_and_after_refresh() -> None:
    _application()
    canvas = MachineCanvas()
    combo = canvas.controller_connector_focus_combo
    expected = (
        ("Functional interfaces", ""),
        ("Detailed ports (all ports)", "__all__::all::details"),
        ("Detailed ports (unused ports)", "__all__::unused::details"),
        ("Detailed ports (used ports)", "__all__::used::details"),
    )

    def first_four_options():
        return tuple(
            (combo.itemText(index), combo.itemData(index))
            for index in range(4)
        )

    assert first_four_options() == expected
    canvas._refresh_controller_connector_choices()
    assert first_four_options() == expected
