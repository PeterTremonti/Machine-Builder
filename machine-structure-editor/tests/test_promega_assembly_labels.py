from __future__ import annotations

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication

from machine_builder.canvas import MachineCanvas
from machine_builder.persistence import load_editor_state
from machine_builder.semantic_component_mutations import UpdateMachineComponent
from machine_builder.semantic_model import Provenance, SemanticPort
from machine_builder.semantic_port_mutations import CreateSemanticPort


GUIDE_TITLE = "PrintM3D Promega — Extruder Assembly Wiring"
GUIDE_URL = (
    "https://promega.printm3d.com/documentation/electronics/"
    "extruder-assembly-wiring"
)

# These are printed labels on the assembly-side cables, not Maestro
# connector IDs, pin IDs, firmware resources, or established wire joins.
PORT_SPECS = (
    (
        "P2",
        "Extruder motor cable connector",
        "new_black_and_old_silver_sections",
        (
            "The new black assembly instructions and old silver assembly "
            "section identify P2/P4 as extruder motor cable connectors. "
            "They do not establish a universal left/right or controller-drive "
            "mapping for this machine."
        ),
    ),
    (
        "P4",
        "Extruder motor cable connector",
        "new_black_and_old_silver_sections",
        (
            "The new black assembly instructions and old silver assembly "
            "section identify P2/P4 as extruder motor cable connectors. "
            "They do not establish a universal left/right or controller-drive "
            "mapping for this machine."
        ),
    ),
    (
        "H2",
        "Heater cable connector",
        "new_black_and_old_silver_sections",
        (
            "The new black section identifies H2/H4 as heater cables. The "
            "old silver section calls H2 the right heater cable for that old "
            "assembly only. Do not equate cable label H2 with firmware heater "
            "H2, or generalize the old side assignment."
        ),
    ),
    (
        "H4",
        "Heater cable connector",
        "new_black_and_old_silver_sections",
        (
            "The new black section identifies H2/H4 as heater cables. The "
            "old silver section calls H4 the left heater cable for that old "
            "assembly only. Do not equate cable label H4 with a firmware "
            "heater resource, or generalize the old side assignment."
        ),
    ),
    (
        "S8",
        "PT1000 temperature-sensor cable connector",
        "new_black_and_old_silver_sections",
        (
            "The new black section identifies S8 as a temperature-sensor "
            "cable and warns that the illustrated wire colour is wrong: "
            "match labels, not colours. The old silver section associates "
            "S8 with the left sensor for that old assembly only. No firmware "
            "temperature-channel mapping is established here."
        ),
    ),
    (
        "S6",
        "PT1000 temperature-sensor cable connector",
        "new_black_and_old_silver_sections",
        (
            "The new black section identifies S6 as a temperature-sensor "
            "cable and warns that the illustrated wire colour is wrong: "
            "match labels, not colours. The old silver section associates "
            "S6 with the right sensor for that old assembly only. No firmware "
            "temperature-channel mapping is established here."
        ),
    ),
    (
        "P9",
        "Fan cable connector; fan role unresolved",
        "new_black_and_old_silver_sections; assignment_varies_by_printer",
        (
            "The new black assembly instructions say the nozzle-fan "
            "connector varies by printer and may be P9 or P11. The old silver "
            "section also says there is no universal P9/P11 role assignment. "
            "Do not infer nozzle versus cold-section role, board endpoint, "
            "or firmware fan index."
        ),
    ),
    (
        "P11",
        "Fan cable connector; fan role unresolved",
        "new_black_and_old_silver_sections; assignment_varies_by_printer",
        (
            "The new black assembly instructions say the nozzle-fan "
            "connector varies by printer and may be P9 or P11. The old silver "
            "section also says there is no universal P9/P11 role assignment. "
            "Do not infer nozzle versus cold-section role, board endpoint, "
            "or firmware fan index."
        ),
    ),
)


def _records_in_model(model):
    """Yield stored records without depending on a particular registry name."""
    for value in vars(model).values():
        if isinstance(value, dict):
            yield from value.values()


def test_promega_assembly_labels_are_component_owned_and_persisted(
    tmp_path,
) -> None:
    application = QApplication.instance()
    if application is None:
        application = QApplication([])

    canvas = MachineCanvas()

    canvas.create_node_from_template(
        node_type="duet_2_maestro_v1_0",
        scene_position=QPointF(100.0, 100.0),
    )
    controller = next(
        iter(canvas.store.semantic_model.controllers.values())
    )
    assert controller.hardware_definition_id is not None
    assert controller.properties["physical_revision_status"] == (
        "not_verified_as_built"
    )

    canvas.create_node_from_template(
        node_type="component",
        scene_position=QPointF(500.0, 180.0),
    )
    component_node = next(
        node
        for node in canvas.store.model.nodes.values()
        if node.node_type == "component"
    )
    component_id = component_node.semantic_reference
    assert component_id is not None

    component = canvas.store.semantic_model.components[component_id]
    assert component.hardware_definition_id is None

    component_evidence = Provenance(
        source=GUIDE_TITLE,
        evidence_type="documentation",
        method="manual source review",
        context=(
            "Compound mixing nozzle/tool assembly: reference evidence for "
            "printed assembly-side cable labels only."
        ),
        date="2026-10-10",
        notes=(
            f"Source: {GUIDE_URL}. The guide distinguishes a new black "
            "assembly section and an older silver assembly section. The "
            "installed cable-assembly version, physical machine variant, "
            "and actual wiring are not verified by this reference."
        ),
    )

    component_properties = dict(component.properties)
    component_properties.update({
        "specimen_scope": "promega_compound_reference",
        "assembly_variant_status": "not_verified",
        "physical_wiring_status": "not_verified_as_built",
        "firmware_assignment_status": "not_established",
        "physical_machine_variant_status": "not_verified",
    })

    canvas.store.commit(
        UpdateMachineComponent(
            component_id=component_id,
            role="Compound mixing nozzle/tool assembly",
            label="Compound mixing nozzle/tool assembly",
            properties=component_properties,
            provenance_entries=list(component.provenance) + [
                component_evidence
            ],
        )
    )

    created_port_ids = []

    for label, purpose, assembly_scope, evidence_context in PORT_SPECS:
        port_id = f"{component_id}-assembly-label-{label.lower()}"

        port_evidence = Provenance(
            source=GUIDE_TITLE,
            evidence_type="documentation",
            method="manual source review",
            context=evidence_context,
            date="2026-10-10",
            notes=(
                f"Source: {GUIDE_URL}. Section applicability: "
                f"{assembly_scope}. This documents an assembly-side printed "
                "label only. It does not establish the user's installed "
                "assembly, a controller connector/contact, a firmware "
                "resource, or an end-to-end physical connection."
            ),
        )

        port = SemanticPort(
            id=port_id,
            component_id=component_id,
            controller_id=None,
            purpose=f"{purpose} (printed label {label})",
            direction="unknown",
            connector_id=None,
            pin_id=None,
            properties={
                "printed_connector_label": label,
                "endpoint_kind": "assembly_cable_connector",
                "assembly_evidence_scope": assembly_scope,
                "assembly_variant_status": "not_verified",
                "machine_endpoint_mapping_status": "unresolved",
                "physical_wiring_status": "not_verified_as_built",
                "firmware_resource_mapping_status": "not_established",
                "evidence_source_url": GUIDE_URL,
            },
            provenance=[port_evidence],
        )

        canvas.store.commit(CreateSemanticPort(port))
        created_port_ids.append(port_id)

    current_model = canvas.store.semantic_model
    component = current_model.components[component_id]

    assert len(created_port_ids) == 8
    assert len(set(created_port_ids)) == 8
    assert component.role == "Compound mixing nozzle/tool assembly"
    assert component.hardware_definition_id is None
    assert component.port_ids == created_port_ids
    assert component.provenance == [component_evidence]

    # Confirm the newly created endpoints are owned by this component,
    # not by the controller, and are not falsely identified as board contacts.
    for (
        port_id,
        (label, purpose, assembly_scope, evidence_context),
    ) in zip(created_port_ids, PORT_SPECS, strict=True):
        port = current_model.ports[port_id]
        assert port.component_id == component_id
        assert port.controller_id is None
        assert port.direction == "unknown"
        assert port.connector_id is None
        assert port.pin_id is None
        assert port.properties["printed_connector_label"] == label
        assert port.properties["endpoint_kind"] == "assembly_cable_connector"
        assert port.properties["assembly_evidence_scope"] == assembly_scope
        assert port.properties["machine_endpoint_mapping_status"] == (
            "unresolved"
        )
        assert port.properties["physical_wiring_status"] == (
            "not_verified_as_built"
        )
        assert port.properties["firmware_resource_mapping_status"] == (
            "not_established"
        )
        assert port.provenance == [
            Provenance(
                source=GUIDE_TITLE,
                evidence_type="documentation",
                method="manual source review",
                context=evidence_context,
                date="2026-10-10",
                notes=(
                    f"Source: {GUIDE_URL}. Section applicability: "
                    f"{assembly_scope}. This documents an assembly-side "
                    "printed label only. It does not establish the user's "
                    "installed assembly, a controller connector/contact, "
                    "a firmware resource, or an end-to-end physical connection."
                ),
            )
        ]

    # This step adds cable-label evidence only. It creates neither canonical
    # physical connections nor resource-assignment records.
    current_records = list(_records_in_model(current_model))
    assert not any(
        type(record).__name__ == "SemanticConnection"
        for record in current_records
    )
    assert not any(
        "Assignment" in type(record).__name__
        for record in current_records
    )

    # Undo/redo of the final endpoint must not leave duplicates or stale ports.
    last_port_id = created_port_ids[-1]
    assert canvas.store.undo()

    undone_model = canvas.store.semantic_model
    assert last_port_id not in undone_model.ports
    assert len(undone_model.components[component_id].port_ids) == 7

    assert canvas.store.redo()
    redone_model = canvas.store.semantic_model
    redone_component = redone_model.components[component_id]
    assert len(redone_component.port_ids) == 8
    assert len(set(redone_component.port_ids)) == 8
    assert set(redone_component.port_ids) == set(created_port_ids)
    assert redone_model.ports[last_port_id].properties[
        "printed_connector_label"
    ] == "P11"

    # Persist and reopen the canonical model, retaining component ownership,
    # printed labels, provenance, and old/new assembly qualifications.
    path = tmp_path / "promega-assembly-labels.machine.json"
    canvas.store.save(path)
    restored = load_editor_state(path)
    restored_model = restored.semantic_model
    restored_component = restored_model.components[component_id]

    assert len(restored_model.controllers) == 1
    assert restored_model.controllers[controller.id].properties[
        "physical_revision_status"
    ] == "not_verified_as_built"
    assert restored_component.hardware_definition_id is None
    assert restored_component.role == "Compound mixing nozzle/tool assembly"
    assert restored_component.provenance == [component_evidence]
    assert set(restored_component.port_ids) == set(created_port_ids)
    assert len(restored_component.port_ids) == 8

    restored_by_label = {
        restored_model.ports[port_id].properties["printed_connector_label"]:
        restored_model.ports[port_id]
        for port_id in restored_component.port_ids
    }
    assert set(restored_by_label) == {
        "P2", "P4", "H2", "H4", "S8", "S6", "P9", "P11"
    }

    for label, purpose, assembly_scope, evidence_context in PORT_SPECS:
        port = restored_by_label[label]
        assert port.component_id == component_id
        assert port.controller_id is None
        assert port.direction == "unknown"
        assert port.connector_id is None
        assert port.pin_id is None
        assert port.purpose == f"{purpose} (printed label {label})"
        assert port.properties["assembly_evidence_scope"] == assembly_scope
        assert port.properties["machine_endpoint_mapping_status"] == (
            "unresolved"
        )
        assert port.properties["physical_wiring_status"] == (
            "not_verified_as_built"
        )
        assert port.properties["firmware_resource_mapping_status"] == (
            "not_established"
        )
        assert port.provenance[0].source == GUIDE_TITLE
        assert port.provenance[0].evidence_type == "documentation"
        assert port.provenance[0].method == "manual source review"
        assert port.provenance[0].context == evidence_context
        assert GUIDE_URL in (port.provenance[0].notes or "")

    restored_records = list(_records_in_model(restored_model))
    assert not any(
        type(record).__name__ == "SemanticConnection"
        for record in restored_records
    )
    assert not any(
        "Assignment" in type(record).__name__
        for record in restored_records
    )