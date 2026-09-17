from PySide6.QtWidgets import QApplication

from machine_builder.controller_resource import (
    ControllerResource,
)
from machine_builder.controller_resource_properties import (
    ControllerResourcePropertiesDialog,
)


def make_resource() -> ControllerResource:
    return ControllerResource(
        id="resource-1",
        name="Heater",
        resource_type="heater",
        properties={
            "max_current": 5,
            "channel": 3,
        },
    )


def get_app() -> QApplication:
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    return app


def test_dialog_starts_with_resource_properties():
    get_app()

    dialog = ControllerResourcePropertiesDialog(
        make_resource()
    )

    assert dialog.windowTitle() == (
        "Controller Resource Properties"
    )

    dialog.deleteLater()


def test_existing_properties_are_preserved():
    get_app()

    dialog = ControllerResourcePropertiesDialog(
        make_resource()
    )

    result = dialog.result()

    assert result == {
        "max_current": "5",
        "channel": "3",
    }

    dialog.deleteLater()


def test_existing_property_can_be_edited():
    get_app()

    dialog = ControllerResourcePropertiesDialog(
        make_resource()
    )

    dialog._property_edits[
        "max_current"
    ].setText("7")

    result = dialog.result()

    assert result["max_current"] == "7"

    dialog.deleteLater()


def test_new_property_can_be_added():
    get_app()

    dialog = ControllerResourcePropertiesDialog(
        make_resource()
    )

    dialog._new_name.setText(
        "voltage"
    )
    dialog._new_value.setText(
        "24"
    )

    result = dialog.result()

    assert result["voltage"] == "24"

    dialog.deleteLater()


def test_blank_new_property_is_ignored():
    get_app()

    dialog = ControllerResourcePropertiesDialog(
        make_resource()
    )

    dialog._new_name.setText(" ")
    dialog._new_value.setText("24")

    result = dialog.result()

    assert "24" not in result.values()

    dialog.deleteLater()


def test_duplicate_property_is_rejected():
    get_app()

    dialog = ControllerResourcePropertiesDialog(
        make_resource()
    )

    dialog._new_name.setText(
        "channel"
    )
    dialog._new_value.setText(
        "4"
    )

    dialog._accept()

    assert (
        "already exists"
        in dialog._status_label.text()
    )

    dialog.deleteLater()


def test_cancel_does_not_accept():
    get_app()

    dialog = ControllerResourcePropertiesDialog(
        make_resource()
    )

    assert dialog.result() == {
        "max_current": "5",
        "channel": "3",
    }

    dialog.deleteLater()