"""Reusable editor for canonical provenance records."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from .semantic_model import Provenance


class ProvenanceDialog(QDialog):
    """Edit a list of provenance records without changing canonical schema."""

    _COLUMNS = (
        "Source",
        "Evidence type",
        "Method",
        "Context",
        "Date",
        "Notes",
    )

    def __init__(
        self,
        provenance: list[Provenance],
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle("Edit Provenance")
        self.setModal(True)
        self.resize(900, 360)

        layout = QVBoxLayout(self)
        self._table = QTableWidget(0, len(self._COLUMNS), self)
        self._table.setObjectName("provenanceTable")
        self._table.setHorizontalHeaderLabels(list(self._COLUMNS))
        self._table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self._table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self._table)

        row_buttons = QHBoxLayout()
        self._add_button = QPushButton("Add Evidence")
        self._add_button.setObjectName("addProvenanceRecordButton")
        self._add_button.clicked.connect(self._add_record)
        row_buttons.addWidget(self._add_button)

        self._remove_button = QPushButton("Remove Selected")
        self._remove_button.setObjectName("removeProvenanceRecordButton")
        self._remove_button.clicked.connect(self._remove_selected_record)
        row_buttons.addWidget(self._remove_button)
        layout.addLayout(row_buttons)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        for record in provenance:
            self._append_record(record)

    def _append_record(
        self,
        record: Provenance | None = None,
    ) -> None:
        """Add one editable evidence row."""
        row = self._table.rowCount()
        self._table.insertRow(row)

        if record is None:
            values = ("", "authored", "", "", "", "")
        else:
            values = (
                record.source,
                record.evidence_type or "authored",
                record.method or "",
                record.context or "",
                record.date or "",
                record.notes or "",
            )

        for column, value in enumerate(values):
            self._table.setItem(
                row,
                column,
                QTableWidgetItem(value),
            )

        self._table.setCurrentCell(row, 0)

    def _add_record(self) -> None:
        """Add a blank evidence row for the user to complete."""
        self._append_record()

    def _remove_selected_record(self) -> None:
        """Remove the currently selected evidence row."""
        row = self._table.currentRow()
        if row >= 0:
            self._table.removeRow(row)

    def result_provenance(self) -> list[Provenance]:
        """Return all complete-source records in table order."""
        records: list[Provenance] = []

        for row in range(self._table.rowCount()):
            values = [
                self._table.item(row, column).text()
                if self._table.item(row, column) is not None
                else ""
                for column in range(len(self._COLUMNS))
            ]

            source = values[0].strip()
            if not source:
                # An empty-source row is a blank draft, not evidence.
                continue

            evidence_type = values[1].strip() or "authored"

            def optional_value(value: str) -> str | None:
                return value if value.strip() else None

            records.append(
                Provenance(
                    source=source,
                    evidence_type=evidence_type,
                    method=optional_value(values[2]),
                    context=optional_value(values[3]),
                    date=optional_value(values[4]),
                    notes=optional_value(values[5]),
                )
            )

        return records
