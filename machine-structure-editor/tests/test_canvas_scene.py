"""Tests for canvas scene synchronization."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import (
    QApplication,
    QGraphicsScene,
)

from machine_builder.canvas_scene import (
    CanvasSceneController,
)
from machine_builder.visual_model import (
    VisualConnection,
    VisualModel,
    VisualNode,
    VisualPort,
)


def _application() -> QApplication:
    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    return app


class SceneCanvasStub:
    """Minimal canvas surface required by CanvasSceneController."""

    def __init__(
        self,
    ) -> None:
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

        self.port_edit_requests: list[
            str
        ] = []

    def _begin_node_move(
        self,
        node_id,
    ):
        pass

    def _finish_node_move(
        self,
        node_id,
    ):
        pass

    def _node_selected(
        self,
        node_id,
        selected,
    ):
        pass

    def _focus_node(
        self,
        node_id,
    ):
        pass

    def _node_position_changed(
        self,
        node_id,
    ):
        pass

    def _start_connection_drag(
        self,
        port_id,
        scene_position,
    ):
        pass

    def _move_connection_drag(
        self,
        port_id,
        scene_position,
    ):
        pass

    def _finish_connection_drag(
        self,
        port_id,
        scene_position,
    ):
        pass

    def _connection_selected(
        self,
        connection_id,
        selected,
    ):
        pass

    def _edit_semantic_port(
        self,
        port_id,
    ):
        self.port_edit_requests.append(
            port_id
        )


def test_scene_controller_syncs_nodes() -> None:
    _application()

    canvas = SceneCanvasStub()
    controller = CanvasSceneController(
        canvas
    )

    node = VisualNode(
        id="node-1",
        node_type="motor",
        label="Motor",
        x=100,
        y=200,
    )

    canvas.store.model.add_node(
        node
    )

    controller.synchronize(
        canvas.store.model
    )

    assert "node-1" in canvas._node_items
    assert len(
        canvas.scene.items()
    ) >= 1


def test_scene_controller_removes_deleted_nodes() -> None:
    _application()

    canvas = SceneCanvasStub()
    controller = CanvasSceneController(
        canvas
    )

    node = VisualNode(
        id="node-1",
        node_type="motor",
        label="Motor",
    )

    canvas.store.model.add_node(
        node
    )

    controller.synchronize(
        canvas.store.model
    )

    assert "node-1" in canvas._node_items

    del canvas.store.model.nodes[
        "node-1"
    ]

    controller.synchronize(
        canvas.store.model
    )

    assert (
        "node-1"
        not in canvas._node_items
    )


def test_scene_controller_finds_rendered_port() -> None:
    _application()

    canvas = SceneCanvasStub()
    controller = CanvasSceneController(
        canvas
    )

    node = VisualNode(
        id="node-1",
        node_type="motor",
        label="Motor",
    )

    node.add_port(
        VisualPort(
            id="port-1",
            node_id="node-1",
            label="Power",
            port_type="power",
            direction="input",
            side="left",
            order=0,
        )
    )

    canvas.store.model.add_node(
        node
    )

    controller.synchronize(
        canvas.store.model
    )

    port_item = (
        controller.find_port_graphics_item(
            "port-1"
        )
    )

    assert port_item is not None
    assert port_item.port_id == "port-1"


def test_scene_controller_syncs_connections() -> None:
    _application()

    canvas = SceneCanvasStub()
    controller = CanvasSceneController(
        canvas
    )

    node_a = VisualNode(
        id="node-a",
        node_type="motor",
        label="Motor A",
        x=100,
        y=100,
    )

    node_b = VisualNode(
        id="node-b",
        node_type="controller",
        label="Controller",
        x=400,
        y=100,
    )

    node_a.add_port(
        VisualPort(
            id="port-a",
            node_id="node-a",
            label="Signal",
            port_type="signal",
            direction="output",
            side="right",
            order=0,
        )
    )

    node_b.add_port(
        VisualPort(
            id="port-b",
            node_id="node-b",
            label="Signal",
            port_type="signal",
            direction="input",
            side="left",
            order=0,
        )
    )

    canvas.store.model.add_node(
        node_a
    )

    canvas.store.model.add_node(
        node_b
    )

    connection = VisualConnection(
        id="connection-1",
        endpoint_a_id="port-a",
        endpoint_b_id="port-b",
    )

    canvas.store.model.add_connection(
        connection
    )

    controller.synchronize(
        canvas.store.model
    )

    assert (
        "connection-1"
        in canvas._connection_items
    )


def test_scene_controller_removes_deleted_connections() -> None:
    _application()

    canvas = SceneCanvasStub()
    controller = CanvasSceneController(
        canvas
    )

    node_a = VisualNode(
        id="node-a",
        node_type="motor",
        label="Motor A",
    )

    node_b = VisualNode(
        id="node-b",
        node_type="controller",
        label="Controller",
    )

    node_a.add_port(
        VisualPort(
            id="port-a",
            node_id="node-a",
            label="Signal",
            port_type="signal",
            direction="output",
            side="right",
            order=0,
        )
    )

    node_b.add_port(
        VisualPort(
            id="port-b",
            node_id="node-b",
            label="Signal",
            port_type="signal",
            direction="input",
            side="left",
            order=0,
        )
    )

    canvas.store.model.add_node(
        node_a
    )

    canvas.store.model.add_node(
        node_b
    )

    canvas.store.model.add_connection(
        VisualConnection(
            id="connection-1",
            endpoint_a_id="port-a",
            endpoint_b_id="port-b",
        )
    )

    controller.synchronize(
        canvas.store.model
    )

    assert (
        "connection-1"
        in canvas._connection_items
    )

    del canvas.store.model.connections[
        "connection-1"
    ]

    controller.synchronize(
        canvas.store.model
    )

    assert (
        "connection-1"
        not in canvas._connection_items
    )