"""Visual editor for basic semantic machine-component details."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from .component_properties import (
    ComponentPropertiesDialog,
)
from .semantic_model import MachineComponent


@dataclass(frozen=True)
class ComponentDetailsResult:
    """Editable semantic values returned by the dialog."""

    role: str
    label: str
    properties: dict[str, str]


class ComponentDetailsDialog(QDialog):
    """Edit the basic semantic identity of one machine component."""

    def __init__(
        self,
        component: MachineComponent,
        machine_name: str,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(
            "Component Details"
        )

        self.setModal(True)

        self._component = component

        self._properties = {
            str(name): (
                ""
                if value is None
                else str(value)
            )
            for name, value
            in component.properties.items()
        }

        self._build_ui(
            component,
            machine_name,
        )

    def _build_ui(
        self,
        component: MachineComponent,
        machine_name: str,
    ) -> None:
        layout = QVBoxLayout(
            self
        )

        form = QFormLayout()

        self._id_value = QLabel(
            component.id
        )

        self._id_value.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self._machine_value = QLabel(
            machine_name
        )

        self._machine_value.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self._role_edit = QLineEdit(
            component.role
        )

        self._label_edit = QLineEdit(
            component.label
        )

        form.addRow(
            "ID:",
            self._id_value,
        )

        form.addRow(
            "Machine:",
            self._machine_value,
        )

        form.addRow(
            "Role:",
            self._role_edit,
        )

        form.addRow(
            "Label:",
            self._label_edit,
        )

        layout.addLayout(
            form
        )

        self._properties_button = QPushButton(
            "Edit Properties..."
        )

        self._properties_button.clicked.connect(
            self._edit_properties
        )

        layout.addWidget(
            self._properties_button
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(
            self.accept
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(
            buttons
        )

    def _edit_properties(
        self,
    ) -> None:
        """Open the property editor."""
        working_component = MachineComponent(
            id=self._component.id,
            role=self._role_edit.text(),
            label=self._label_edit.text(),
            hardware_definition_id=(
                self._component.hardware_definition_id
            ),
            port_ids=(
                self._component.port_ids.copy()
            ),
            properties=self._properties.copy(),
            provenance=(
                self._component.provenance.copy()
            ),
        )

        dialog = ComponentPropertiesDialog(
            working_component,
            parent=self,
        )

        if (
            dialog.exec()
            != dialog.DialogCode.Accepted
        ):
            return

        self._properties = (
            dialog.result_properties()
        )

        count = len(
            self._properties
        )

        self._properties_button.setText(
            f"Edit Properties... ({count})"
        )

    def result_data(
        self,
    ) -> ComponentDetailsResult:
        """Return the edited component values."""
        return ComponentDetailsResult(
            role=self._role_edit.text(),
            label=self._label_edit.text(),
            properties=self._properties.copy(),
        )

    def accept(self) -> None:
        """Validate the editable fields before accepting."""
        role = self._role_edit.text().strip()

        if not role:
            self._role_edit.setFocus()
            return

        super().accept()