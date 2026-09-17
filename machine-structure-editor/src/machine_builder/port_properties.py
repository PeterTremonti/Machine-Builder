"""Property editing for semantic port data."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)

from .semantic_model import SemanticPort


class PortPropertiesDialog(QDialog):
    """Edit the string representation of semantic-port properties."""

    def __init__(
        self,
        port: SemanticPort,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(
            "Port Properties"
        )

        self.setModal(True)

        self._property_edits: list[
            tuple[QLineEdit, QLineEdit]
        ] = []

        self._build_ui(
            port
        )

    def _build_ui(
        self,
        port: SemanticPort,
    ) -> None:
        layout = QVBoxLayout(
            self
        )

        form = QFormLayout()

        for (
            name,
            value,
        ) in sorted(
            port.properties.items()
        ):
            name_edit = QLineEdit(
                str(name)
            )

            value_edit = QLineEdit(
                ""
                if value is None
                else str(value)
            )

            name_edit.setReadOnly(
                True
            )

            form.addRow(
                name_edit,
                value_edit,
            )

            self._property_edits.append(
                (
                    name_edit,
                    value_edit,
                )
            )

        new_name = QLineEdit()
        new_value = QLineEdit()

        new_name.setPlaceholderText(
            "Property name"
        )

        new_value.setPlaceholderText(
            "Property value"
        )

        form.addRow(
            new_name,
            new_value,
        )

        self._new_name_edit = new_name
        self._new_value_edit = new_value

        layout.addLayout(
            form
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

    def result_properties(
        self,
    ) -> dict[str, str]:
        """Return the edited property values."""
        properties: dict[str, str] = {}

        for (
            name_edit,
            value_edit,
        ) in self._property_edits:
            name = name_edit.text().strip()

            if not name:
                continue

            properties[name] = (
                value_edit.text()
            )

        new_name = (
            self._new_name_edit.text().strip()
        )

        if new_name:
            properties[new_name] = (
                self._new_value_edit.text()
            )

        return properties