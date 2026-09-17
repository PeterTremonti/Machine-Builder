"""Tests for the component-details dialog."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from machine_builder.component_details import (
    ComponentDetailsDialog,
    ComponentDetailsResult,
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
    )


def test_dialog_shows_component_id() -> None:
    _application()

    dialog = ComponentDetailsDialog(
        make_component(),
        "Test Machine",
    )

    assert dialog._id_value.text() == (
        "component-1"
    )


def test_dialog_shows_machine_name() -> None:
    _application()

    dialog = ComponentDetailsDialog(
        make_component(),
        "Promega",
    )

    assert dialog._machine_value.text() == (
        "Promega"
    )


def test_dialog_initializes_role() -> None:
    _application()

    dialog = ComponentDetailsDialog(
        make_component(),
        "Test Machine",
    )

    assert dialog._role_edit.text() == (
        "motor"
    )


def test_dialog_initializes_label() -> None:
    _application()

    dialog = ComponentDetailsDialog(
        make_component(),
        "Test Machine",
    )

    assert dialog._label_edit.text() == (
        "X Axis Motor"
    )


def test_dialog_returns_edited_values() -> None:
    _application()

    dialog = ComponentDetailsDialog(
        make_component(),
        "Test Machine",
    )

    dialog._role_edit.setText(
        "extruder drive motor"
    )

    dialog._label_edit.setText(
        "Extruder Motor"
    )

    assert dialog.result_data() == (
        ComponentDetailsResult(
            role="extruder drive motor",
            label="Extruder Motor",
            properties={},
        )
    )


def test_dialog_rejects_blank_role() -> None:
    _application()

    dialog = ComponentDetailsDialog(
        make_component(),
        "Test Machine",
    )

    dialog._role_edit.setText(
        "   "
    )

    dialog.accept()

    assert not dialog.result()


def test_dialog_can_accept_valid_values() -> None:
    _application()

    dialog = ComponentDetailsDialog(
        make_component(),
        "Test Machine",
    )

    dialog._role_edit.setText(
        "drive motor"
    )

    dialog._label_edit.setText(
        "Drive Motor"
    )

    dialog.accept()

    assert dialog.result()