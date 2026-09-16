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