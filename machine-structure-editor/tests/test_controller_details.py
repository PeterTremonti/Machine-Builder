"""Tests for the controller-details dialog."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from machine_builder.controller import Controller
from machine_builder.controller_details import (
    ControllerDetailsDialog,
    ControllerDetailsResult,
)


def _application() -> QApplication:
    application = QApplication.instance()

    if application is None:
        application = QApplication(sys.argv)

    return application


def make_controller() -> Controller:
    return Controller(
        id="controller-1",
        name="Main Controller",
        controller_type="motion_controller",
        version="3.5.4",
    )


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