"""Tests for user-facing multi-entry provenance editing."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QDialog, QPushButton

from machine_builder.component_details import ComponentDetailsDialog
from machine_builder.port_details import PortDetailsDialog
from machine_builder.provenance_details import ProvenanceDialog
from machine_builder.semantic_model import (
    MachineComponent,
    Provenance,
    SemanticPort,
)


def _application() -> QApplication:
    application = QApplication.instance()
    if application is None:
        application = QApplication(sys.argv)
    return application


def _records() -> list[Provenance]:
    return [
        Provenance(
            source="Source A",
            evidence_type="documentation",
            method="manual transcription",
            context="Synthetic test context",
            date="2026-10-10",
            notes="Initial evidence note",
        ),
        Provenance(
            source="Source B",
            evidence_type="observation",
            method="visual inspection",
            context="Second synthetic test context",
            date="2026-10-10",
            notes="Second evidence note",
        ),
    ]


def test_provenance_dialog_edits_and_returns_multiple_records() -> None:
    _application()
    records = _records()
    dialog = ProvenanceDialog(records)

    assert dialog._table.rowCount() == 2
    assert dialog._table.columnCount() == 6

    dialog._table.item(0, 5).setText("Reviewed note")
    result = dialog.result_provenance()

    assert len(result) == 2
    assert result[0] == Provenance(
        source="Source A",
        evidence_type="documentation",
        method="manual transcription",
        context="Synthetic test context",
        date="2026-10-10",
        notes="Reviewed note",
    )
    assert result[1] == records[1]


def test_component_dialog_button_edits_provenance(monkeypatch) -> None:
    _application()
    records = _records()
    component = MachineComponent(
        id="component-unknown",
        role="generic-device",
        label="Unknown identity",
        hardware_definition_id=None,
        properties={"verification_status": "unknown"},
        provenance=records,
    )
    dialog = ComponentDetailsDialog(
        component=component,
        machine_name="Synthetic test machine",
    )

    button = dialog.findChild(QPushButton, "editProvenanceButton")
    assert button is not None

    def accept_with_edit(editor: ProvenanceDialog):
        editor._table.item(0, 0).setText("Updated component evidence")
        return QDialog.DialogCode.Accepted

    monkeypatch.setattr(ProvenanceDialog, "exec", accept_with_edit)
    button.click()

    result = dialog.result_data()
    assert result.role == "generic-device"
    assert result.label == "Unknown identity"
    assert result.provenance[0].source == "Updated component evidence"
    assert result.provenance[1] == records[1]
    assert component.hardware_definition_id is None


def test_component_owned_port_dialog_button_edits_provenance(
    monkeypatch,
) -> None:
    _application()
    records = _records()
    port = SemanticPort(
        id="port-unknown",
        component_id="component-unknown",
        purpose="fixture endpoint",
        direction="input",
        connector_id="fixture-connector",
        pin_id="fixture-contact",
        properties={"verification_status": "fixture-only"},
        provenance=records,
    )
    dialog = PortDetailsDialog(
        port=port,
        component_label="Synthetic generic component",
    )

    button = dialog.findChild(QPushButton, "editProvenanceButton")
    assert button is not None

    def accept_with_edit(editor: ProvenanceDialog):
        editor._table.item(0, 0).setText("Updated port evidence")
        return QDialog.DialogCode.Accepted

    monkeypatch.setattr(ProvenanceDialog, "exec", accept_with_edit)
    button.click()

    result = dialog.result_data()
    assert result.purpose == "fixture endpoint"
    assert result.connector_id == "fixture-connector"
    assert result.pin_id == "fixture-contact"
    assert result.provenance[0].source == "Updated port evidence"
    assert result.provenance[1] == records[1]
