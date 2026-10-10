from __future__ import annotations

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication

from machine_builder.canvas import MachineCanvas
from machine_builder.persistence import load_editor_state
from machine_builder.semantic_component_mutations import UpdateMachineComponent
from machine_builder.semantic_model import Provenance
from machine_builder.semantic_port_mutations import UpdateSemanticPort


PROMEGA_ROLES = (
    ("X motion motor", "motor"),
    ("Y motion motor", "motor"),
    ("Z motion motor", "motor"),
    ("Compound left-drive motor", "motor"),
    ("Compound right-drive motor", "motor"),
    ("Compound mixing nozzle/tool assembly", "component"),
    ("Compound hotend heater", "component"),
    ("Compound hotend temperature sensor", "temperature_sensor"),
    ("Bed heater", "component"),
    ("Bed temperature sensor", "temperature_sensor"),
    ("Part-cooling/nozzle fan", "component"),
    ("Hotend heatsink/cold-section fan", "component"),
    ("X homing endstop", "sensor"),
    ("IR Z probe", "sensor"),
)


def test_promega_roles_use_existing_authoring_and_persistence_paths(tmp_path):
    application = QApplication.instance()
    if application is None:
        application = QApplication([])

    canvas = MachineCanvas()
    canvas.create_node_from_template(
        "duet_2_maestro_v1_0", QPointF(100.0, 100.0)
    )
    model = canvas.store.semantic_model

    assert len(model.controllers) == 1
    controller = next(iter(model.controllers.values()))
    assert controller.hardware_definition_id is not None
    assert controller.properties["physical_revision_status"] == (
        "not_verified_as_built"
    )

    controller_node = next(
        node for node in canvas.store.model.nodes.values()
        if node.semantic_reference == controller.id
    )
    assert controller_node.node_type == "controller"

    # Record evidence on an existing board endpoint without assigning
    # a Promega component, harness, or verified physical connection.
    board_port = next(
        port for port in model.ports.values()
        if port.controller_id == controller.id and port.component_id is None
    )
    port_note = Provenance(
        source="Machine Builder Duet 2 Maestro reference-board definition",
        evidence_type="authored",
        method="manual review",
        context="Controller-owned endpoint; no component or harness assignment.",
        date="2026-10-10",
        notes=(
            "Does not verify physical continuity, the installed board revision, "
            "harness mapping, or firmware resource use."
        ),
    )
    expected_port_evidence = list(board_port.provenance) + [port_note]
    canvas.store.commit(
        UpdateSemanticPort(
            port_id=board_port.id,
            provenance_entries=expected_port_evidence,
        )
    )

    created = []
    last_original = None
    last_evidence = None

    for index, (role, node_type) in enumerate(PROMEGA_ROLES, start=1):
        node_id = f"node-{len(canvas.store.model.nodes) + 1}"
        canvas.create_node_from_template(
            node_type,
            QPointF(100.0 + index * 80.0, 160.0 + index * 35.0),
        )
        node = canvas.store.model.nodes[node_id]
        component = model.components[node.semantic_reference]

        assert component.hardware_definition_id is None
        assert component.port_ids == []

        if index == len(PROMEGA_ROLES):
            last_original = (
                component.role,
                component.label,
                dict(component.properties),
                list(component.provenance),
            )

        properties = dict(component.properties)
        properties.update({
            "specimen_scope": "promega_compound_reference",
            "verification_status": "role_only_identity_unverified",
            "physical_presence_status": "not_verified_as_built",
            "inventory_crosswalk_status": "not_established",
            "firmware_assignment_status": "not_established",
            "verification_notes": (
                "Role only; exact installed identity, physical variant, "
                "and wiring remain unverified."
            ),
            "inventory_crosswalk_notes": (
                "No product identity or inventory identifier inferred."
            ),
        })
        evidence = Provenance(
            source="Planning milestone: First Promega Reference Specimen",
            evidence_type="authored",
            method="manual transcription",
            context=f"Planning-defined role only: {role}.",
            date="2026-10-10",
            notes=(
                "The checkpoint lists an accepted inventory deliverable but "
                "does not contain its detailed table. Do not infer a part "
                "number, hardware definition, physical endpoint, or connection."
            ),
        )
        canvas.store.commit(
            UpdateMachineComponent(
                component_id=component.id,
                role=role,
                label=role,
                properties=properties,
                provenance_entries=[evidence],
            )
        )
        created.append((role, node_id, component.id, evidence))
        if index == len(PROMEGA_ROLES):
            last_evidence = evidence

    assert len(created) == 14
    assert len(model.components) == 14
    assert len(model.controllers) == 1
    assert len(model.machines["machine-1"].component_ids) == 14
    assert len({role for role, *_ in created}) == 14

    for role, node_id, component_id, evidence in created:
        component = model.components[component_id]
        node = canvas.store.model.nodes[node_id]
        assert component.role == role
        assert component.label == role == node.label
        assert node.semantic_reference == component.id
        assert component.hardware_definition_id is None
        assert component.port_ids == []
        assert component.provenance == [evidence]
        assert component.properties["inventory_crosswalk_status"] == (
            "not_established"
        )
        assert component.properties["firmware_assignment_status"] == (
            "not_established"
        )

    # The last edit must undo and redo without duplicating evidence.
    assert last_original is not None and last_evidence is not None
    last_role, _, last_id, _ = created[-1]
    assert canvas.store.undo()
    undone = canvas.store.semantic_model.components[last_id]
    assert (undone.role, undone.label) == last_original[:2]
    assert undone.properties == last_original[2]
    assert undone.provenance == last_original[3]

    assert canvas.store.redo()
    redone = canvas.store.semantic_model.components[last_id]
    assert redone.role == last_role
    assert redone.provenance == [last_evidence]
    assert redone.hardware_definition_id is None

    path = tmp_path / "promega-reference-specimen.machine.json"
    canvas.store.save(path)
    restored = load_editor_state(path)
    restored_model = restored.semantic_model

    assert len(restored_model.controllers) == 1
    assert len(restored_model.components) == 14
    assert len(restored.visual_model.nodes) == 15
    assert len(restored_model.machines["machine-1"].component_ids) == 14

    restored_controller = next(iter(restored_model.controllers.values()))
    assert restored_controller.properties["physical_revision_status"] == (
        "not_verified_as_built"
    )
    restored_roles = {
        component.role: component
        for component in restored_model.components.values()
    }
    assert set(restored_roles) == {role for role, _ in PROMEGA_ROLES}

    for role, node_id, component_id, evidence in created:
        component = restored_model.components[component_id]
        node = restored.visual_model.nodes[node_id]
        assert restored_roles[role].id == component_id
        assert component.label == role
        assert component.hardware_definition_id is None
        assert component.port_ids == []
        assert component.provenance == [evidence]
        assert node.label == role
        assert node.semantic_reference == component_id

    restored_port = restored_model.ports[board_port.id]
    assert restored_port.controller_id == restored_controller.id
    assert restored_port.component_id is None
    assert restored_port.provenance == expected_port_evidence