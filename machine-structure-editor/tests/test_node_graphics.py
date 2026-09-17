"""Tests for node graphics synchronization."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from machine_builder.graphics.node import (
    NodeGraphicsItem,
)
from machine_builder.visual_model import (
    VisualNode,
)


def make_application() -> QApplication:
    application = QApplication.instance()

    if application is None:
        application = QApplication(
            sys.argv
        )

    return application


def make_node(
    node_type: str = "controller",
) -> VisualNode:
    return VisualNode(
        id="node-1",
        node_type=node_type,
        label="Original Controller",
    )


def make_graphics_item(
    node: VisualNode,
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
    )


def test_node_graphics_starts_with_visual_node_label() -> None:
    make_application()

    node = make_node()

    item = make_graphics_item(
        node
    )

    assert (
        item._label_item.text()
        == "Original Controller"
    )


def test_node_graphics_refreshes_label_from_visual_node() -> None:
    make_application()

    node = make_node()

    item = make_graphics_item(
        node
    )

    node.label = "Renamed Controller"

    item._rebuild_ports(
        node=node,
        connection_drag_started=lambda *_: None,
        connection_drag_moved=lambda *_: None,
        connection_drag_finished=lambda *_: None,
        port_edit_requested=lambda *_: None,
    )

    assert (
        item._label_item.text()
        == "Renamed Controller"
    )


def test_node_graphics_keeps_node_identity_when_label_changes() -> None:
    make_application()

    node = make_node()

    item = make_graphics_item(
        node
    )

    node.label = "BTT Octopus V1.1"

    item._rebuild_ports(
        node=node,
        connection_drag_started=lambda *_: None,
        connection_drag_moved=lambda *_: None,
        connection_drag_finished=lambda *_: None,
        port_edit_requested=lambda *_: None,
    )

    assert item.node_id == "node-1"

    assert (
        item._label_item.text()
        == "BTT Octopus V1.1"
    )


def test_controller_node_has_distinct_border() -> None:
    make_application()

    node = make_node(
        node_type="controller"
    )

    item = make_graphics_item(
        node
    )

    assert (
        item.pen().widthF()
        == NodeGraphicsItem._CONTROLLER_PEN_WIDTH
    )


def test_controller_node_uses_bold_label() -> None:
    make_application()

    node = make_node(
        node_type="controller"
    )

    item = make_graphics_item(
        node
    )

    assert item._label_item.font().bold()


def test_non_controller_node_uses_standard_border() -> None:
    make_application()

    node = make_node(
        node_type="motor"
    )

    node.label = "Motor"

    item = make_graphics_item(
        node
    )

    assert (
        item.pen().widthF()
        == NodeGraphicsItem._DEFAULT_PEN_WIDTH
    )


def test_non_controller_node_uses_standard_label_weight() -> None:
    make_application()

    node = make_node(
        node_type="sensor"
    )

    node.label = "Sensor"

    item = make_graphics_item(
        node
    )

    assert not item._label_item.font().bold()