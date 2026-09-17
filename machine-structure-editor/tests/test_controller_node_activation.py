"""Tests for direct controller-node activation."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import (
    QApplication,
    QGraphicsScene,
)

from machine_builder.canvas_scene import (
    CanvasSceneController,
)
from machine_builder.graphics.node import (
    NodeGraphicsItem,
)
from machine_builder.visual_model import (
    VisualModel,
    VisualNode,
)


def _application() -> QApplication:
    application = QApplication.instance()

    if application is None:
        application = QApplication(
            sys.argv
        )

    return application


def _make_node_item(
    node: VisualNode,
    callback,
) -> NodeGraphicsItem:
    return NodeGraphicsItem(
        node=node,
        move_started_callback=lambda *_: None,
        move_finished_callback=lambda *_: None,
        selection_callback=lambda *_: None,
        focus_callback=lambda *_: None,
        position_changed_callback=lambda *_: None,
        connection_drag_started=lambda *_: None,
        connection_drag_moved=lambda *_: None,
        connection_drag_finished=lambda *_: None,
        port_edit_requested=lambda *_: None,
        double_click_callback=callback,
    )


class SceneCanvasStub:
    def __init__(self) -> None:
        self.scene = QGraphicsScene()
        self._node_items = {}
        self._connection_items = {}
        self._synchronizing_scene = False

        self.store = type(
            "StoreStub",
            (),
            {
                "model": VisualModel(),
            },
        )()

        self.controller_edit_count = 0

    def _begin_node_move(self, *_):
        pass

    def _finish_node_move(self, *_):
        pass

    def _node_selected(self, *_):
        pass

    def _focus_node(self, *_):
        pass

    def _node_position_changed(self, *_):
        pass

    def _start_connection_drag(self, *_):
        pass

    def _move_connection_drag(self, *_):
        pass

    def _finish_connection_drag(self, *_):
        pass

    def _connection_selected(self, *_):
        pass

    def _edit_semantic_port(self, *_):
        pass

    def _edit_selected_controller(self) -> None:
        self.controller_edit_count += 1


def test_controller_double_click_invokes_callback() -> None:
    _application()

    calls: list[int] = []

    node = VisualNode(
        id="node-1",
        node_type="controller",
        label="Controller",
    )

    item = _make_node_item(
        node,
        lambda: calls.append(1),
    )

    item._activate_double_click()

    assert calls == [1]


def test_controller_double_click_selects_node() -> None:
    _application()

    node = VisualNode(
        id="node-1",
        node_type="controller",
        label="Controller",
    )

    item = _make_node_item(
        node,
        lambda: None,
    )

    item._activate_double_click()

    assert item.isSelected()


def test_non_controller_double_click_does_not_invoke_controller_callback() -> None:
    _application()

    calls: list[int] = []

    node = VisualNode(
        id="node-1",
        node_type="motor",
        label="Motor",
    )

    item = _make_node_item(
        node,
        lambda: calls.append(1),
    )

    item._activate_double_click()

    assert calls == []
    assert not item.isSelected()


def test_scene_controller_connects_controller_nodes_to_editor() -> None:
    _application()

    canvas = SceneCanvasStub()
    scene_controller = CanvasSceneController(
        canvas
    )

    node = VisualNode(
        id="node-1",
        node_type="controller",
        label="Controller",
    )

    canvas.store.model.add_node(
        node
    )

    scene_controller.synchronize(
        canvas.store.model
    )

    item = canvas._node_items[
        "node-1"
    ]

    assert (
        item._double_click_callback
        == canvas._edit_selected_controller
    )