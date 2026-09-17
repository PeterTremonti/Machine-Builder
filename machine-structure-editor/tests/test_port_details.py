"""Tests for the semantic port-details dialog."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from machine_builder.port_details import (
    PortDetailsDialog,
    PortDetailsResult,
)
from machine_builder.semantic_model import (
    SemanticPort,
)


def _application() -> QApplication:
    application = QApplication.instance()

    if application is None:
        application = QApplication(sys.argv)

    return application


def make_port() -> SemanticPort:
    return SemanticPort(
        id="port-1",
        component_id="component-1",
        purpose="Motor Command",
        direction="output",
        connector_id="J4",
        pin_id="PA7",
        properties={
            "protocol": "PWM",
            "voltage": 24,
        },
    )


def test_dialog_shows_port_id() -> None:
    _application()

    dialog = PortDetailsDialog(
        make_port(),
        "X Axis Motor",
    )

    assert dialog._id_value.text() == (
        "port-1"
    )


def test_dialog_shows_component_label() -> None:
    _application()

    dialog = PortDetailsDialog(
        make_port(),
        "X Axis Motor",
    )

    assert (
        dialog._component_value.text()
        == "X Axis Motor"
    )


def test_dialog_initializes_purpose() -> None:
    _application()

    dialog = PortDetailsDialog(
        make_port(),
        "X Axis Motor",
    )

    assert (
        dialog._purpose_edit.text()
        == "Motor Command"
    )


def test_dialog_initializes_direction() -> None:
    _application()

    dialog = PortDetailsDialog(
        make_port(),
        "X Axis Motor",
    )

    assert (
        dialog._direction_edit.text()
        == "output"
    )


def test_dialog_initializes_connector() -> None:
    _application()

    dialog = PortDetailsDialog(
        make_port(),
        "X Axis Motor",
    )

    assert (
        dialog._connector_edit.text()
        == "J4"
    )


def test_dialog_initializes_pin() -> None:
    _application()

    dialog = PortDetailsDialog(
        make_port(),
        "X Axis Motor",
    )

    assert (
        dialog._pin_edit.text()
        == "PA7"
    )


def test_dialog_returns_edited_values() -> None:
    _application()

    dialog = PortDetailsDialog(
        make_port(),
        "X Axis Motor",
    )

    dialog._purpose_edit.setText(
        "Heater Control"
    )

    dialog._direction_edit.setText(
        "input"
    )

    dialog._connector_edit.setText(
        "J8"
    )

    dialog._pin_edit.setText(
        "PB3"
    )

    assert dialog.result_data() == (
        PortDetailsResult(
            purpose="Heater Control",
            direction="input",
            connector_id="J8",
            pin_id="PB3",
            properties={
                "protocol": "PWM",
                "voltage": "24",
            },
        )
    )


def test_dialog_converts_blank_connector_to_none() -> None:
    _application()

    dialog = PortDetailsDialog(
        make_port(),
        "X Axis Motor",
    )

    dialog._connector_edit.clear()

    result = dialog.result_data()

    assert result.connector_id is None


def test_dialog_converts_blank_pin_to_none() -> None:
    _application()

    dialog = PortDetailsDialog(
        make_port(),
        "X Axis Motor",
    )

    dialog._pin_edit.clear()

    result = dialog.result_data()

    assert result.pin_id is None


def test_dialog_rejects_blank_purpose() -> None:
    _application()

    dialog = PortDetailsDialog(
        make_port(),
        "X Axis Motor",
    )

    dialog._purpose_edit.setText(
        "   "
    )

    dialog.accept()

    assert not dialog.result()


def test_dialog_rejects_blank_direction() -> None:
    _application()

    dialog = PortDetailsDialog(
        make_port(),
        "X Axis Motor",
    )

    dialog._direction_edit.setText(
        "   "
    )

    dialog.accept()

    assert not dialog.result()


def test_dialog_accepts_valid_values() -> None:
    _application()

    dialog = PortDetailsDialog(
        make_port(),
        "X Axis Motor",
    )

    dialog._purpose_edit.setText(
        "Temperature"
    )

    dialog._direction_edit.setText(
        "input"
    )

    dialog.accept()

    assert dialog.result()