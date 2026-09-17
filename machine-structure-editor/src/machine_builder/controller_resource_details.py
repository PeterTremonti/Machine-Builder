"""Dialog for editing canonical controller-resource details."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from .controller_resource import ControllerResource
from .controller_resource_assignment import (
    ControllerResourceAssignment,
)


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
        assignments: list[
            ControllerResourceAssignment
        ] | None = None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(
            "Controller Resource Details"
        )

        self._result: (
            ControllerResourceDetailsResult | None
        ) = None

        self._assignments = list(
            assignments or []
        )

        self._name_edit = QLineEdit(
            resource.name
        )

        self._resource_type_edit = QLineEdit(
            resource.resource_type
        )

        self._controller_id = (
            resource.controller_id
        )

        resource_id_label = QLabel(
            resource.id
        )

        resource_id_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        controller_text = (
            controller_name
            if controller_name is not None
            else resource.controller_id
            or "Unassigned"
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

        layout = QVBoxLayout(
            self
        )

        layout.addLayout(
            form
        )

        assignments_label = QLabel(
            f"Assignments ({len(self._assignments)})"
        )

        layout.addWidget(
            assignments_label
        )

        self._assignment_list = QListWidget()

        self._assignment_list.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )

        self._assignment_list.setMinimumHeight(
            90
        )

        if self._assignments:
            for assignment in self._assignments:
                item = QListWidgetItem(
                    self._assignment_text(
                        assignment
                    )
                )

                item.setData(
                    Qt.ItemDataRole.UserRole,
                    assignment.id,
                )

                self._assignment_list.addItem(
                    item
                )
        else:
            self._assignment_list.addItem(
                "No assignments."
            )

        layout.addWidget(
            self._assignment_list
        )

        layout.addWidget(
            buttons
        )

    @staticmethod
    def _assignment_text(
        assignment: ControllerResourceAssignment,
    ) -> str:
        return (
            f"{assignment.assignment_type} — "
            f"{assignment.source_id}"
        )

    def _accept(self) -> None:
        name = (
            self._name_edit.text().strip()
        )

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
                controller_id=self._controller_id,
            )
        )

        self.accept()

    def result(
        self,
    ) -> ControllerResourceDetailsResult | None:
        """Return the accepted dialog result."""

        return self._result