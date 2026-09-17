"""Dialog for editing canonical controller-resource details."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)

from .controller_resource import ControllerResource


@dataclass(frozen=True)
class ControllerResourceDetailsResult:
    """Editable controller-resource fields returned by the dialog."""

    name: str
    resource_type: str
    controller_id: str | None


class ControllerResourceDetailsDialog(QDialog):
    """Edit the basic authored details of a controller resource."""

    def __init__(
        self,
        resource: ControllerResource,
        controller_name: str | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(
            "Controller Resource Details"
        )

        self._result: ControllerResourceDetailsResult | None = None

        self._name_edit = QLineEdit(
            resource.name
        )
        self._resource_type_edit = QLineEdit(
            resource.resource_type
        )

        resource_id_label = QLabel(
            resource.id
        )
        resource_id_label.setTextInteractionFlags(
            resource_id_label.textInteractionFlags()
        )

        controller_text = (
            controller_name
            if controller_name is not None
            else resource.controller_id or "Unassigned"
        )

        controller_label = QLabel(
            controller_text
        )

        form = QFormLayout()
        form.addRow(
            "Resource ID:",
            resource_id_label,
        )
        form.addRow(
            "Name:",
            self._name_edit,
        )
        form.addRow(
            "Resource Type:",
            self._resource_type_edit,
        )
        form.addRow(
            "Controller:",
            controller_label,
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
        name = self._name_edit.text().strip()
        resource_type = (
            self._resource_type_edit.text().strip()
        )

        if not name:
            self._name_edit.setFocus()
            return

        if not resource_type:
            self._resource_type_edit.setFocus()
            return

        self._result = (
            ControllerResourceDetailsResult(
                name=name,
                resource_type=resource_type,
                controller_id=None,
            )
        )

        self.accept()

    def result(self) -> ControllerResourceDetailsResult | None:
        """Return the accepted dialog result."""
        return self._result