"""Read-only details dialog for controller-resource assignments."""

from __future__ import annotations

import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QPlainTextEdit,
    QVBoxLayout,
)

from .controller_resource_assignment import (
    ControllerResourceAssignment,
)


class ControllerResourceAssignmentDetailsDialog(QDialog):
    """Inspect one canonical controller-resource assignment."""

    def __init__(
        self,
        assignment: ControllerResourceAssignment,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(
            "Controller Resource Assignment Details"
        )

        resource_id_label = QLabel(
            assignment.resource_id
        )

        resource_id_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        source_id_label = QLabel(
            assignment.source_id
        )

        source_id_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        assignment_id_label = QLabel(
            assignment.id
        )

        assignment_id_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        form = QFormLayout()

        form.addRow(
            "Assignment ID:",
            assignment_id_label,
        )

        form.addRow(
            "Source ID:",
            source_id_label,
        )

        form.addRow(
            "Resource ID:",
            resource_id_label,
        )

        form.addRow(
            "Assignment Type:",
            QLabel(
                assignment.assignment_type
            ),
        )

        layout = QVBoxLayout(
            self
        )

        layout.addLayout(
            form
        )

        properties_label = QLabel(
            "Properties:"
        )

        layout.addWidget(
            properties_label
        )

        properties_view = QPlainTextEdit()

        properties_view.setReadOnly(
            True
        )

        properties_view.setMinimumHeight(
            100
        )

        properties_view.setPlainText(
            json.dumps(
                assignment.properties,
                indent=2,
                sort_keys=True,
            )
        )

        layout.addWidget(
            properties_view
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close
        )

        buttons.rejected.connect(
            self.reject
        )

        buttons.clicked.connect(
            lambda *_: self.accept()
        )

        layout.addWidget(
            buttons
        )