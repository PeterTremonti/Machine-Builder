"""Dialogs for authoring physical connection details and limitations."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QVBoxLayout,
)


@dataclass(frozen=True)
class ConnectionEndpointSummary:
    """Read-only endpoint identity shown while authoring a connection."""

    owner_label: str
    port_purpose: str
    connector_id: str
    pin_id: str


class PhysicalConnectionDetailsDialog(QDialog):
    """Collect optional physical wire details before creating a connection."""

    def __init__(
        self,
        endpoint_a: ConnectionEndpointSummary,
        endpoint_b: ConnectionEndpointSummary,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle("Physical Connection Details")
        self.setModal(True)
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)
        intro = QLabel(
            "Review both endpoints and record any known wire details. "
            "Leave fields blank when the information is unknown or "
            "unverified. Blank fields are saved as unspecified."
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        self._add_endpoint_group(layout, "Endpoint A", endpoint_a)
        self._add_endpoint_group(layout, "Endpoint B", endpoint_b)

        endpoint_note = QLabel(
            "Endpoint A and Endpoint B are labels for this dialog only. "
            "Physical connections are not directional."
        )
        endpoint_note.setWordWrap(True)
        layout.addWidget(endpoint_note)

        fields = QFormLayout()
        self.wire_color_edit = QLineEdit(self)
        self.wire_color_edit.setPlaceholderText(
            "Optional; leave blank if unknown."
        )
        fields.addRow("Wire color", self.wire_color_edit)

        self.harness_id_edit = QLineEdit(self)
        self.harness_id_edit.setPlaceholderText(
            "Optional; leave blank if unknown."
        )
        fields.addRow("Harness ID", self.harness_id_edit)

        self.notes_edit = QPlainTextEdit(self)
        self.notes_edit.setPlaceholderText(
            "Optional; leave blank if unknown."
        )
        self.notes_edit.setFixedHeight(80)
        fields.addRow("Notes", self.notes_edit)
        layout.addLayout(fields)

        helper = QLabel(
            "Leave any field blank if unknown. Blank or whitespace-only "
            "fields are saved as unspecified, not as confirmed absence."
        )
        helper.setWordWrap(True)
        layout.addWidget(helper)

        buttons = QDialogButtonBox(self)
        buttons.addButton(
            "Create Connection",
            QDialogButtonBox.ButtonRole.AcceptRole,
        )
        buttons.addButton(
            "Cancel",
            QDialogButtonBox.ButtonRole.RejectRole,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    @staticmethod
    def _add_endpoint_group(
        layout: QVBoxLayout,
        title: str,
        endpoint: ConnectionEndpointSummary,
    ) -> None:
        """Add a read-only group describing one canonical physical port."""
        group = QGroupBox(title)
        form = QFormLayout(group)
        values = (
            ("Component / controller", endpoint.owner_label),
            ("Port purpose", endpoint.port_purpose),
            ("Connector", endpoint.connector_id),
            ("Pin", endpoint.pin_id),
        )
        for label_text, value_text in values:
            label = QLabel(value_text or "Unspecified")
            label.setWordWrap(True)
            form.addRow(label_text, label)
        layout.addWidget(group)

    def result_data(self) -> dict[str, str]:
        """Return entered values without modifying nonblank user input."""
        return {
            "wire_color": self.wire_color_edit.text(),
            "harness_id": self.harness_id_edit.text(),
            "notes": self.notes_edit.toPlainText(),
        }


def _confirm_with_buttons(
    parent,
    title: str,
    message: str,
    confirm_label: str,
) -> bool:
    """Return True only when the explicit non-default choice is accepted."""
    dialog = QMessageBox(parent)
    dialog.setIcon(QMessageBox.Icon.Warning)
    dialog.setWindowTitle(title)
    dialog.setText(message)
    confirm_button = dialog.addButton(
        confirm_label,
        QMessageBox.ButtonRole.AcceptRole,
    )
    dialog.addButton(
        "Cancel",
        QMessageBox.ButtonRole.RejectRole,
    )
    dialog.exec()
    return dialog.clickedButton() is confirm_button


def confirm_unknown_compatibility(parent) -> bool:
    """Ask for explicit confirmation when compatibility is unknown."""
    return _confirm_with_buttons(
        parent,
        "Compatibility Could Not Be Established",
        "Machine Builder cannot determine whether these endpoints are "
        "compatible from the available information. Continue only if you "
        "are satisfied that this physical connection is appropriate.",
        "Continue",
    )


def confirm_conditional_compatibility(parent) -> bool:
    """Ask for explicit confirmation when compatibility is conditional."""
    return _confirm_with_buttons(
        parent,
        "Conditional Compatibility",
        "The available information indicates that a condition or "
        "qualification applies. This connection has not been established "
        "as unconditionally compatible. Continue only if the condition "
        "is understood and acceptable.",
        "Continue",
    )


def confirm_visual_only_connection(parent) -> bool:
    """Ask before drawing a connection without two canonical physical ports."""
    return _confirm_with_buttons(
        parent,
        "Visual-Only Connection",
        "At least one endpoint has no canonical physical-port record. "
        "You can draw this connection visually, but its wire color, "
        "harness ID, and notes cannot be retained as physical connection "
        "metadata. No canonical physical connection will be created.",
        "Draw Visual Connection",
    )


def show_incompatible_connection(parent) -> None:
    """Explain why a known-incompatible connection cannot be created."""
    QMessageBox.warning(
        parent,
        "Connection Not Allowed",
        "These endpoints are known to be incompatible. Machine Builder "
        "cannot create this connection.",
        QMessageBox.StandardButton.Ok,
    )


def show_invalid_canonical_reference(parent) -> None:
    """Report a stale or invalid canonical port reference without mutating."""
    QMessageBox.warning(
        parent,
        "Connection Not Created",
        "At least one endpoint refers to a canonical physical port that "
        "does not exist. No connection was created.",
        QMessageBox.StandardButton.Ok,
    )