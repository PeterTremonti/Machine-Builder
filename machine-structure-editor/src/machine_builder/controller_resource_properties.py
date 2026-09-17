"""Property editing dialog for controller resources."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from .controller_resource import ControllerResource


class ControllerResourcePropertiesDialog(QDialog):
    """Edit controller-resource properties.

    Existing property names are displayed but cannot be renamed or removed.
    One additional property row is available for adding a new property.
    """

    def __init__(
        self,
        resource: ControllerResource,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(
            "Controller Resource Properties"
        )

        self._property_edits: dict[str, QLineEdit] = {}

        form = QFormLayout()

        resource_id_label = QLabel(resource.id)
        form.addRow(
            "Resource ID:",
            resource_id_label,
        )

        for name, value in sorted(
            resource.properties.items()
        ):
            edit = QLineEdit(str(value))
            self._property_edits[name] = edit

            name_label = QLabel(name)
            form.addRow(
                name_label,
                edit,
            )

        self._new_name = QLineEdit()
        self._new_value = QLineEdit()

        form.addRow(
            "New property:",
            self._new_name,
        )
        form.addRow(
            "New value:",
            self._new_value,
        )

        self._status_label = QLabel()
        form.addRow(
            "",
            self._status_label,
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(
            self._accept
        )
        buttons.rejected.connect(
            self.reject
        )

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def _accept(self) -> None:
        new_name = self._new_name.text().strip()

        if new_name and new_name in self._property_edits:
            self._status_label.setText(
                "That property name already exists."
            )
            self._new_name.setFocus()
            return

        self.accept()

    def result(self) -> dict[str, str]:
        """Return the edited properties."""
        properties = {
            name: edit.text()
            for name, edit
            in self._property_edits.items()
        }

        new_name = self._new_name.text().strip()

        if new_name:
            properties[new_name] = (
                self._new_value.text()
            )

        return properties