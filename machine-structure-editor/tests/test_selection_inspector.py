"""Tests for selection inspection and debug information."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from machine_builder.selection_inspector import (
    SelectionInspector,
)
from machine_builder.visual_model import (
    VisualConnection,
    VisualModel,
    VisualNode,
    VisualPort,
)


def _application() -> QApplication:
    application = QApplication.instance()

    if application is None:
        application = QApplication(
            sys.argv
        )

    return application


def make_model() -> VisualModel:
    model = VisualModel()

    controller = VisualNode(
        id="node-controller",
        node_type="controller",
        label="Controller",
        x=500,
        y=200,
        width=180,
        height=100,
        semantic_reference="controller-1",
    )

    controller.add_port(
        VisualPort(
            id="port-controller",
            node_id=controller.id,
            label="Stepper X",
            port_type="stepper",
            direction="input",
            side="left",
            order=0,
            semantic_reference="resource-1",
        )
    )

    motor = VisualNode(
        id="node-motor",
        node_type="motor",
        label="Motor X",
        x=100,
        y=200,
        width=180,
        height=100,
        semantic_reference="component-1",
    )

    motor.add_port(
        VisualPort(
            id="port-motor",
            node_id=motor.id,
            label="Driver",
            port_type="stepper",
            direction="output",
            side="right",
            order=0,
        )
    )

    model.add_node(
        controller
    )

    model.add_node(
        motor
    )

    model.add_connection(
        VisualConnection(
            id="connection-1",
            endpoint_a_id="port-motor",
            endpoint_b_id="port-controller",
            connection_type="stepper",
        )
    )

    return model


def test_inspector_starts_empty() -> None:
    _application()

    inspector = SelectionInspector()

    assert "Select a node" in (
        inspector.debug_text()
    )


def test_node_debug_text_contains_geometry() -> None:
    _application()

    model = make_model()

    inspector = SelectionInspector()

    inspector.set_node(
        model.nodes["node-controller"],
        model,
    )

    text = inspector.debug_text()

    assert "x: 500.000" in text
    assert "y: 200.000" in text
    assert "width: 180.000" in text
    assert "height: 100.000" in text
    assert "right: 680.000" in text
    assert "bottom: 300.000" in text


def test_node_debug_text_contains_ports() -> None:
    _application()

    model = make_model()

    inspector = SelectionInspector()

    inspector.set_node(
        model.nodes["node-controller"],
        model,
    )

    text = inspector.debug_text()

    assert "Stepper X" in text
    assert "port-controller" in text
    assert "side: left" in text
    assert "order: 0" in text


def test_node_debug_text_contains_connection() -> None:
    _application()

    model = make_model()

    inspector = SelectionInspector()

    inspector.set_node(
        model.nodes["node-controller"],
        model,
    )

    text = inspector.debug_text()

    assert "connection-1" in text
    assert "Motor X / Driver" in text


def test_connection_debug_text_contains_endpoints() -> None:
    _application()

    model = make_model()

    inspector = SelectionInspector()

    inspector.set_connection(
        model.connections["connection-1"],
        model,
    )

    text = inspector.debug_text()

    assert "connection-1" in text
    assert "Motor X" in text
    assert "Controller" in text
    assert "Driver" in text
    assert "Stepper X" in text


def test_multiple_selection_is_reported() -> None:
    _application()

    inspector = SelectionInspector()

    inspector.set_multiple_selection(
        3
    )

    assert (
        "3 items selected"
        in inspector._selection_label.text()
    )


def test_copy_debug_info_returns_displayed_text() -> None:
    _application()

    model = make_model()

    inspector = SelectionInspector()

    inspector.set_node(
        model.nodes["node-controller"],
        model,
    )

    copied = inspector.copy_debug_info()

    assert copied == (
        inspector.debug_text()
    )


def test_clear_removes_selection_details() -> None:
    _application()

    model = make_model()

    inspector = SelectionInspector()

    inspector.set_node(
        model.nodes["node-controller"],
        model,
    )

    inspector.clear()

    assert (
        inspector._selection_label.text()
        == "Nothing selected"
    )

    assert (
        inspector.debug_text()
        == "Select a node or connection to inspect it."
    )