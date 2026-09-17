"""Tests for semantic port property editing."""

from __future__ import annotations

from PySide6.QtWidgets import QApplication

from machine_builder.port_properties import (
    PortPropertiesDialog,
)
from machine_builder.semantic_model import (
    SemanticPort,
)


def _application() -> QApplication:
    application = QApplication.instance()

    if application is None:
        application = QApplication()

    return application


def make_port() -> SemanticPort:
    return SemanticPort(
        id="port-1",
        component_id="component-1",
        purpose="Motor Command",
        direction="output",
        properties={
            "voltage": 24,
            "protocol": "PWM",
        },
    )


def test_property_dialog_loads_existing_properties() -> None:
    _application()

    dialog = PortPropertiesDialog(
        make_port()
    )

    assert len(
        dialog._property_edits
    ) == 2


def test_property_dialog_returns_existing_properties() -> None:
    _application()

    dialog = PortPropertiesDialog(
        make_port()
    )

    assert dialog.result_properties() == {
        "protocol": "PWM",
        "voltage": "24",
    }


def test_property_dialog_can_add_property() -> None:
    _application()

    dialog = PortPropertiesDialog(
        make_port()
    )

    dialog._new_name_edit.setText(
        "current"
    )

    dialog._new_value_edit.setText(
        "2.0"
    )

    properties = dialog.result_properties()

    assert properties["current"] == "2.0"


def test_property_dialog_ignores_blank_new_property_name() -> None:
    _application()

    dialog = PortPropertiesDialog(
        make_port()
    )

    dialog._new_name_edit.setText(
        "   "
    )

    dialog._new_value_edit.setText(
        "ignored"
    )

    properties = dialog.result_properties()

    assert "ignored" not in properties.values()


def test_port_details_includes_properties() -> None:
    from machine_builder.port_details import (
        PortDetailsDialog,
    )

    _application()

    dialog = PortDetailsDialog(
        make_port(),
        "X Axis Motor",
    )

    assert dialog.result_data().properties == {
        "protocol": "PWM",
        "voltage": "24",
    }