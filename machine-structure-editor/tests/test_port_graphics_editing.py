"""Tests for semantic editing interaction on port graphics."""

from __future__ import annotations

import sys

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication, QGraphicsScene

from machine_builder.graphics.port import (
    PortGraphicsItem,
)
from machine_builder.visual_model import VisualPort


def _application() -> QApplication:
    application = QApplication.instance()

    if application is None:
        application = QApplication(sys.argv)

    return application


def make_port() -> VisualPort:
    return VisualPort(
        id="port-1",
        node_id="node-1",
        label="Motor Command",
        port_type="signal",
        direction="output",
        semantic_reference="semantic-port-1",
    )


def test_port_graphics_accepts_edit_callback() -> None:
    _application()

    calls: list[str] = []

    item = PortGraphicsItem(
        port=make_port(),
        connection_drag_started=lambda *_: None,
        connection_drag_moved=lambda *_: None,
        connection_drag_finished=lambda *_: None,
        port_edit_requested=lambda port_id: (
            calls.append(port_id)
        ),
    )

    assert item.port_id == "port-1"

    assert calls == []


def test_port_graphics_can_be_added_to_scene() -> None:
    _application()

    scene = QGraphicsScene()

    item = PortGraphicsItem(
        port=make_port(),
        connection_drag_started=lambda *_: None,
        connection_drag_moved=lambda *_: None,
        connection_drag_finished=lambda *_: None,
        port_edit_requested=lambda *_: None,
    )

    scene.addItem(
        item
    )

    assert item in scene.items()


def test_port_double_click_requests_edit() -> None:
    _application()

    calls: list[str] = []

    item = PortGraphicsItem(
        port=make_port(),
        connection_drag_started=lambda *_: None,
        connection_drag_moved=lambda *_: None,
        connection_drag_finished=lambda *_: None,
        port_edit_requested=lambda port_id: (
            calls.append(port_id)
        ),
    )

    scene = QGraphicsScene()
    scene.addItem(item)

    class FakeEvent:
        def button(self):
            from PySide6.QtCore import Qt

            return Qt.MouseButton.LeftButton

        def scenePos(self):
            return QPointF(0, 0)

        def accept(self):
            return None

        def ignore(self):
            return None

    item.mouseDoubleClickEvent(
        FakeEvent()
    )

    assert calls == [
        "port-1"
    ]