"""Visual editor for basic semantic port details."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from .port_properties import (
    PortPropertiesDialog,
)
from .semantic_model import SemanticPort


@dataclass(frozen=True)
class PortDetailsResult:
    """Editable semantic values returned by the dialog."""

    purpose: str
    direction: str
    connector_id: str | None
    pin_id: str | None
    properties: dict[str, str]


class PortDetailsDialog(QDialog):
    """Edit the basic semantic identity of one port."""

    def __init__(
        self,
        port: SemanticPort,
        component_label: str,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(
            "Port Details"
        )

        self.setModal(True)

        self._port = port

        self._properties = {
            str(name): (
                ""
                if value is None
                else str(value)
            )
            for name, value
            in port.properties.items()
        }

        self._build_ui(
            port,
            component_label,
        )

    def _build_ui(
        self,
        port: SemanticPort,
        component_label: str,
    ) -> None:
        layout = QVBoxLayout(
            self
        )

        form = QFormLayout()

        self._id_value = QLabel(
            port.id
        )

        self._id_value.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self._component_value = QLabel(
            component_label
        )

        self._component_value.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self._purpose_edit = QLineEdit(
            port.purpose
        )

        self._direction_edit = QLineEdit(
            port.direction
        )

        self._connector_edit = QLineEdit(
            ""
            if port.connector_id is None
            else port.connector_id
        )

        self._pin_edit = QLineEdit(
            ""
            if port.pin_id is None
            else port.pin_id
        )

        form.addRow(
            "ID:",
            self._id_value,
        )

        form.addRow(
            "Component:",
            self._component_value,
        )

        form.addRow(
            "Purpose:",
            self._purpose_edit,
        )

        form.addRow(
            "Direction:",
            self._direction_edit,
        )

        form.addRow(
            "Connector:",
            self._connector_edit,
        )

        form.addRow(
            "Pin:",
            self._pin_edit,
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
        """Open the port property editor."""
        working_port = SemanticPort(
            id=self._port.id,
            component_id=(
                self._port.component_id
            ),
            purpose=(
                self._purpose_edit.text()
            ),
            direction=(
                self._direction_edit.text()
            ),
            connector_id=(
                self._connector_edit.text()
                or None
            ),
            pin_id=(
                self._pin_edit.text()
                or None
            ),
            properties=self._properties.copy(),
            provenance=(
                self._port.provenance.copy()
            ),
        )

        dialog = PortPropertiesDialog(
            working_port,
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
    ) -> PortDetailsResult:
        """Return the edited port values."""
        connector = (
            self._connector_edit.text().strip()
        )

        pin = (
            self._pin_edit.text().strip()
        )

        return PortDetailsResult(
            purpose=self._purpose_edit.text(),
            direction=self._direction_edit.text(),
            connector_id=(
                connector
                if connector
                else None
            ),
            pin_id=(
                pin
                if pin
                else None
            ),
            properties=self._properties.copy(),
        )

    def accept(self) -> None:
        """Validate required fields before accepting."""
        purpose = (
            self._purpose_edit.text().strip()
        )

        direction = (
            self._direction_edit.text().strip()
        )

        if not purpose:
            self._purpose_edit.setFocus()
            return

        if not direction:
            self._direction_edit.setFocus()
            return

        super().accept()