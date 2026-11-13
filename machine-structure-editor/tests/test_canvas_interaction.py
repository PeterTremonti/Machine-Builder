"""Tests for canvas interaction state and helper behavior."""

from __future__ import annotations

from PySide6.QtCore import QPointF

from machine_builder.canvas_interaction import (
    ConnectionDragState,
    NodeDragState,
)


def test_node_drag_state_stores_group_positions() -> None:
    state = NodeDragState(
        node_ids=("node-1", "node-2"),
        start_positions={
            "node-1": (10.0, 20.0),
            "node-2": (30.0, 40.0),
        },
    )

    assert state.node_ids == (
        "node-1",
        "node-2",
    )

    assert (
        state.start_positions["node-1"]
        == (10.0, 20.0)
    )

    assert (
        state.start_positions["node-2"]
        == (30.0, 40.0)
    )


def test_connection_drag_state_stores_cursor_position() -> None:
    state = ConnectionDragState(
        source_port_id="port-a",
        current_scene_position=QPointF(
            125.0,
            240.0,
        ),
    )

    assert state.source_port_id == "port-a"

    assert (
        state.current_scene_position.x()
        == 125.0
    )

    assert (
        state.current_scene_position.y()
        == 240.0
    )

    assert state.target_port_id is None


def test_connection_drag_state_can_store_target() -> None:
    state = ConnectionDragState(
        source_port_id="port-a",
        current_scene_position=QPointF(
            125.0,
            240.0,
        ),
        target_port_id="port-b",
    )

    assert state.target_port_id == "port-b"

def test_node_position_changed_requests_preview_during_drag():
    from machine_builder.canvas_interaction import (
        CanvasInteractionMixin,
        NodeDragState,
    )

    class SceneControllerProbe:
        preview_requests = 0
        route_updates = 0

        def request_node_move_preview(self):
            self.preview_requests += 1

        def update_connection_graphics(self):
            self.route_updates += 1

    class Host(CanvasInteractionMixin):
        def __init__(self):
            self._scene_controller = SceneControllerProbe()
            self._synchronizing_scene = False
            self._active_node_drag = NodeDragState(
                node_ids=("moving-node",),
                start_positions={"moving-node": (0.0, 0.0)},
            )

    host = Host()
    host._node_position_changed("moving-node")

    assert host._scene_controller.preview_requests == 1
    assert host._scene_controller.route_updates == 0


def test_node_position_changed_keeps_full_refresh_outside_drag():
    from machine_builder.canvas_interaction import CanvasInteractionMixin

    class SceneControllerProbe:
        preview_requests = 0
        route_updates = 0

        def request_node_move_preview(self):
            self.preview_requests += 1

        def update_connection_graphics(self):
            self.route_updates += 1

    class Host(CanvasInteractionMixin):
        def __init__(self):
            self._scene_controller = SceneControllerProbe()
            self._synchronizing_scene = False
            self._active_node_drag = None

    host = Host()
    host._node_position_changed("stationary-node")

    assert host._scene_controller.preview_requests == 0
    assert host._scene_controller.route_updates == 1


def test_node_position_changed_ignores_scene_synchronization():
    from machine_builder.canvas_interaction import (
        CanvasInteractionMixin,
        NodeDragState,
    )

    class SceneControllerProbe:
        preview_requests = 0
        route_updates = 0

        def request_node_move_preview(self):
            self.preview_requests += 1

        def update_connection_graphics(self):
            self.route_updates += 1

    class Host(CanvasInteractionMixin):
        def __init__(self):
            self._scene_controller = SceneControllerProbe()
            self._synchronizing_scene = True
            self._active_node_drag = NodeDragState(
                node_ids=("moving-node",),
                start_positions={"moving-node": (0.0, 0.0)},
            )

    host = Host()
    host._node_position_changed("moving-node")

    assert host._scene_controller.preview_requests == 0
    assert host._scene_controller.route_updates == 0