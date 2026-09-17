"""Tests for component property editing."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from machine_builder.component_details import (
    ComponentDetailsDialog,
)
from machine_builder.component_properties import (
    ComponentPropertiesDialog,
)
from machine_builder.semantic_model import (
    MachineComponent,
)


def _application() -> QApplication:
    application = QApplication.instance()

    if application is None:
        application = QApplication(sys.argv)

    return application


def make_component() -> MachineComponent:
    return MachineComponent(
        id="component-1",
        role="motor",
        label="X Axis Motor",
        properties={
            "axis": "X",
            "voltage": 24,
        },
    )


def test_property_dialog_loads_existing_properties() -> None:
    _application()

    dialog = ComponentPropertiesDialog(
        make_component()
    )

    assert len(
        dialog._property_edits
    ) == 2


def test_property_dialog_returns_existing_properties() -> None:
    _application()

    dialog = ComponentPropertiesDialog(
        make_component()
    )

    properties = (
        dialog.result_properties()
    )

    assert properties == {
        "axis": "X",
        "voltage": "24",
    }


def test_property_dialog_can_add_property() -> None:
    _application()

    dialog = ComponentPropertiesDialog(
        make_component()
    )

    dialog._new_name_edit.setText(
        "current"
    )

    dialog._new_value_edit.setText(
        "2.0"
    )

    properties = (
        dialog.result_properties()
    )

    assert properties["current"] == "2.0"


def test_property_dialog_ignores_blank_new_property_name() -> None:
    _application()

    dialog = ComponentPropertiesDialog(
        make_component()
    )

    dialog._new_name_edit.setText(
        "   "
    )

    dialog._new_value_edit.setText(
        "ignored"
    )

    properties = (
        dialog.result_properties()
    )

    assert "ignored" not in properties.values()


def test_details_dialog_includes_properties_in_result() -> None:
    _application()

    dialog = ComponentDetailsDialog(
        make_component(),
        "Test Machine",
    )

    result = dialog.result_data()

    assert result.properties == {
        "axis": "X",
        "voltage": "24",
    }