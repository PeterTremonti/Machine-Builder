"""Tests for the controller-details dialog."""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from machine_builder.controller import Controller
from machine_builder.controller_details import (
    ControllerDetailsDialog,
    ControllerDetailsResult,
)
from machine_builder.controller_resource import (
    ControllerResource,
)


def _application() -> QApplication:
    application = QApplication.instance()

    if application is None:
        application = QApplication(
            sys.argv
        )

    return application


def make_controller() -> Controller:
    return Controller(
        id="controller-1",
        name="Main Controller",
        controller_type="motion_controller",
        version="3.5.4",
    )


def make_resources() -> list[ControllerResource]:
    return [
        ControllerResource(
            id="resource-1",
            name="Stepper X",
            resource_type="stepper_output",
            controller_id="controller-1",
        ),
        ControllerResource(
            id="resource-2",
            name="Heater 0",
            resource_type="heater_output",
            controller_id="controller-1",
        ),
        ControllerResource(
            id="resource-3",
            name="Thermistor 0",
            resource_type="temperature_input",
            controller_id="controller-1",
        ),
    ]


def test_dialog_shows_controller_id() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
    )

    assert dialog._id_value.text() == (
        "controller-1"
    )


def test_dialog_shows_machine_name() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
    )

    assert (
        dialog._machine_value.text()
        == "Promega"
    )


def test_dialog_initializes_name() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
    )

    assert dialog._name_edit.text() == (
        "Main Controller"
    )


def test_dialog_initializes_type() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
    )

    assert (
        dialog._type_edit.text()
        == "motion_controller"
    )


def test_dialog_initializes_version() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
    )

    assert (
        dialog._version_edit.text()
        == "3.5.4"
    )


def test_dialog_returns_edited_values() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
    )

    dialog._name_edit.setText(
        "Duet 2 Maestro"
    )

    dialog._type_edit.setText(
        "RRF Controller"
    )

    dialog._version_edit.setText(
        "3.5.4"
    )

    assert dialog.result_data() == (
        ControllerDetailsResult(
            name="Duet 2 Maestro",
            controller_type="RRF Controller",
            version="3.5.4",
        )
    )


def test_dialog_blank_version_becomes_none() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
    )

    dialog._version_edit.clear()

    assert (
        dialog.result_data().version
        is None
    )


def test_dialog_rejects_blank_name() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
    )

    dialog._name_edit.setText(
        "   "
    )

    dialog.accept()

    assert not dialog.result()


def test_dialog_rejects_blank_type() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
    )

    dialog._type_edit.setText(
        "   "
    )

    dialog.accept()

    assert not dialog.result()


def test_dialog_accepts_valid_values() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
    )

    dialog._name_edit.setText(
        "Octopus V1.1"
    )

    dialog._type_edit.setText(
        "Klipper Controller"
    )

    dialog.accept()

    assert dialog.result()


def test_dialog_shows_controller_resources() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
        resources=make_resources(),
    )

    assert dialog._resource_list.count() == 3

    assert (
        dialog._resource_list.item(0).text()
        == "Stepper X — stepper_output"
    )

    assert (
        dialog._resource_list.item(1).text()
        == "Heater 0 — heater_output"
    )

    assert (
        dialog._resource_list.item(2).text()
        == "Thermistor 0 — temperature_input"
    )


def test_dialog_stores_resource_ids_on_items() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
        resources=make_resources(),
    )

    assert (
        dialog._resource_list.item(0).data(
            Qt.ItemDataRole.UserRole
        )
        == "resource-1"
    )

    assert (
        dialog._resource_list.item(2).data(
            Qt.ItemDataRole.UserRole
        )
        == "resource-3"
    )


def test_dialog_handles_controller_without_resources() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
    )

    assert dialog._resource_list.count() == 1

    assert (
        dialog._resource_list.item(0).text()
        == "No controller resources."
    )


def test_dialog_emits_resource_edit_request() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
        resources=make_resources(),
    )

    requested: list[str] = []

    dialog.resource_edit_requested.connect(
        requested.append
    )

    dialog._resource_item_double_clicked(
        dialog._resource_list.item(0)
    )

    assert requested == [
        "resource-1"
    ]


def test_dialog_refreshes_resource_row() -> None:
    _application()

    dialog = ControllerDetailsDialog(
        make_controller(),
        "Promega",
        resources=make_resources(),
    )

    resource = make_resources()[0]

    resource.name = "X Motor"
    resource.resource_type = "stepper_driver"

    assert dialog.refresh_resource(
        resource
    )

    assert (
        dialog._resource_list.item(0).text()
        == "X Motor — stepper_driver"
    )