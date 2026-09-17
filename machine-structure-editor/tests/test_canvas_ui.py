"""Tests for the canvas UI construction mixin."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

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