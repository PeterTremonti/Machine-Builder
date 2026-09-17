"""Tests for controller-resource detail editing."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from machine_builder.controller_resource import (
    ControllerResource,
)
from machine_builder.controller_resource_details import (
    ControllerResourceDetailsDialog,
    ControllerResourceDetailsResult,
)


def _application() -> QApplication:
    application = QApplication.instance()

    if application is None:
        application = QApplication(
            sys.argv
        )

    return application


def make_resource() -> ControllerResource:
    return ControllerResource(
        id="resource-1",
        name="Stepper X",
        resource_type="stepper_output",
        controller_id="controller-1",
        properties={
            "channel": 0
        },
    )


def test_dialog_initializes_resource_fields() -> None:
    _application()

    dialog = ControllerResourceDetailsDialog(
        resource=make_resource(),
        controller_name="Main Controller",
    )

    assert dialog._name_edit.text() == (
        "Stepper X"
    )

    assert (
        dialog._resource_type_edit.text()
        == "stepper_output"
    )


def test_dialog_accept_returns_edited_values() -> None:
    _application()

    dialog = ControllerResourceDetailsDialog(
        resource=make_resource(),
        controller_name="Main Controller",
    )

    dialog._name_edit.setText(
        "X Stepper"
    )

    dialog._resource_type_edit.setText(
        "stepper_driver"
    )

    dialog._accept()

    assert dialog.result() == (
        ControllerResourceDetailsResult(
            name="X Stepper",
            resource_type="stepper_driver",
            controller_id="controller-1",
        )
    )


def test_dialog_preserves_controller_assignment() -> None:
    _application()

    resource = make_resource()

    dialog = ControllerResourceDetailsDialog(
        resource=resource,
        controller_name="Main Controller",
    )

    dialog._accept()

    result = dialog.result()

    assert result is not None
    assert (
        result.controller_id
        == "controller-1"
    )


def test_dialog_supports_unassigned_resource() -> None:
    _application()

    resource = make_resource()
    resource.controller_id = None

    dialog = ControllerResourceDetailsDialog(
        resource=resource,
    )

    dialog._accept()

    result = dialog.result()

    assert result is not None
    assert result.controller_id is None


def test_dialog_rejects_blank_name() -> None:
    _application()

    dialog = ControllerResourceDetailsDialog(
        resource=make_resource(),
    )

    dialog._name_edit.setText(
        "   "
    )

    dialog._accept()

    assert dialog.result() is None


def test_dialog_rejects_blank_resource_type() -> None:
    _application()

    dialog = ControllerResourceDetailsDialog(
        resource=make_resource(),
    )

    dialog._resource_type_edit.setText(
        "   "
    )

    dialog._accept()

    assert dialog.result() is None