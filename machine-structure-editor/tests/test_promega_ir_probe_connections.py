from __future__ import annotations

import re

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication

from machine_builder.canvas import MachineCanvas
from machine_builder.promega_fixtures import (
    add_promega_ir_probe_reference_connections,
)
from machine_builder.persistence import load_editor_state
from machine_builder.semantic_component_mutations import UpdateMachineComponent
from machine_builder.semantic_model import Provenance, SemanticPort

REFERENCE_WIRING_NOTE = (
    "Manufacturer-documented reference wiring, not verified as-built."
)

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


def _contact_position(port: SemanticPort) -> int:
    """Resolve a contact's position from its instantiated board identity."""
    explicit_position = port.properties.get("connector_position")
    if explicit_position is not None:
        return int(explicit_position)

    for identity in (port.pin_id, port.id):
        match = re.search(r"(?:^|[-_])(\d+)$", identity or "")
        if match:
            return int(match.group(1))

    raise AssertionError(
        f"No contact position metadata found for board port {port.id!r}"
    )


def _board_probe_port(model, controller_id, position, pin_label):
    matches = [
        port
        for port in model.ports.values()
        if port.controller_id == controller_id
        and port.component_id is None
        and port.connector_id == "z-probe"
        and _contact_position(port) == position
        and port.properties.get("pin_label") == pin_label
    ]
    assert len(matches) == 1, (
        f"Expected one controller-owned z-probe port at position "
        f"{position} labelled {pin_label!r}; found {len(matches)}"
    )
    return matches[0]


def test_promega_ir_z_probe_reference_connections_are_provenanced_and_persisted(
    tmp_path,
):
    if QApplication.instance() is None:
        application = QApplication([])
    else:
        application = QApplication.instance()

    canvas = MachineCanvas()
    canvas.create_node_from_template(
        "duet_2_maestro_v1_0", QPointF(100.0, 100.0)
    )
    controller = next(iter(canvas.store.semantic_model.controllers.values()))
    model = canvas.store.semantic_model

    assert controller.hardware_definition_id is not None
    assert controller.properties["physical_revision_status"] == (
        "not_verified_as_built"
    )

    # Build the established specimen using its normal palette and component
    # authoring path, then extend that specimen's existing IR Z probe role.
    created_roles = {}
    for index, (role, node_type) in enumerate(PROMEGA_ROLES, start=1):
        node_id = f"node-{len(canvas.store.model.nodes) + 1}"
        canvas.create_node_from_template(
            node_type,
            QPointF(100.0 + index * 80.0, 160.0 + index * 35.0),
        )
        component_node = canvas.store.model.nodes[node_id]
        component_id = component_node.semantic_reference
        assert component_id is not None

        component = model.components[component_id]
        assert component.hardware_definition_id is None
        assert component.port_ids == []

        evidence = Provenance(
            source="Planning milestone: First Promega Reference Specimen",
            evidence_type="authored",
            method="manual transcription",
            context=f"Planning-defined role only: {role}.",
            date="2026-10-10",
            notes=(
                "Exact installed identity, physical variant, inventory mapping, "
                "and wiring remain unverified. No part number, endpoint, or "
                "firmware resource is inferred from the role name."
            ),
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
        canvas.store.commit(
            UpdateMachineComponent(
                component_id=component_id,
                role=role,
                label=role,
                properties=properties,
                provenance_entries=[evidence],
            )
        )
        created_roles[role] = (node_id, component_id, evidence)

    assert len(created_roles) == 14
    assert len(model.components) == 14
    assert len(model.controllers) == 1
    assert len(model.machines["machine-1"].component_ids) == 14

    probe_node_id, probe_component_id, role_evidence = created_roles["IR Z probe"]
    probe_node = canvas.store.model.nodes[probe_node_id]
    probe_component = model.components[probe_component_id]
    assert probe_node.semantic_reference == probe_component_id
    assert probe_component.role == "IR Z probe"
    assert probe_component.hardware_definition_id is None
    assert probe_component.port_ids == []
    assert probe_component.properties["firmware_assignment_status"] == (
        "not_established"
    )

    probe_ports, expected = add_promega_ir_probe_reference_connections(
        canvas,
        probe_component_id=probe_component_id,
        controller_id=controller.id,
    )

    assert model.components[probe_component_id].port_ids == [
        port.id for port in probe_ports.values()
    ]
    for port in probe_ports.values():
        assert port.component_id == probe_component_id
        assert port.controller_id is None
        assert port.connector_id is None
        assert port.pin_id is None
    assert len(expected) == 3
    assert set(model.connections) == set(expected)
    assert len(canvas.store.model.connections) == 3

    for connection_id, expected_values in expected.items():
        probe_id, board_id, position, pin_label, cable_label, evidence = (
            expected_values
        )
        connection = model.connections[connection_id]
        assert {connection.endpoint_a_id, connection.endpoint_b_id} == {
            probe_id, board_id
        }
        assert connection.connection_type == "electrical"
        assert connection.properties["documented_cable_label"] == cable_label
        assert connection.properties["notes"] == REFERENCE_WIRING_NOTE
        assert connection.provenance == evidence
        assert connection.connects_same_ports(probe_id, board_id)
        assert connection.connects_same_ports(board_id, probe_id)
        assert not connection.is_self_connection()

    unused_contact_ids = {
        _board_probe_port(
            model, controller.id, 3, "Z_PROBE_MOD"
        ).id,
        _board_probe_port(
            model, controller.id, 5, "+5V"
        ).id,
    }
    assert all(
        not connection.contains_port(port_id)
        for connection in model.connections.values()
        for port_id in unused_contact_ids
    )
    assert model.components[probe_component_id].properties[
        "firmware_assignment_status"
    ] == "not_established"

    # Undo/redo must operate on the semantic and visual representations together.
    for remaining in (2, 1, 0):
        assert canvas.store.undo()
        assert len(canvas.store.semantic_model.connections) == remaining
        assert len(canvas.store.model.connections) == remaining

    for count in (1, 2, 3):
        assert canvas.store.redo()
        assert len(canvas.store.semantic_model.connections) == count
        assert len(canvas.store.model.connections) == count

    assert set(canvas.store.semantic_model.connections) == set(expected)

    path = tmp_path / "promega-ir-z-probe-connections.machine.json"
    canvas.store.save(path)
    restored = load_editor_state(path)
    restored_model = restored.semantic_model
    restored_controller = restored_model.controllers[controller.id]

    assert restored_controller.properties["physical_revision_status"] == (
        "not_verified_as_built"
    )
    assert len(restored_model.components) == 14
    assert len(restored_model.controllers) == 1
    assert len(restored_model.machines["machine-1"].component_ids) == 14
    assert {component.role for component in restored_model.components.values()} == {
        role for role, _node_type in PROMEGA_ROLES
    }
    assert len(restored_model.connections) == 3
    assert len(restored.visual_model.connections) == 3
    assert restored_model.components[probe_component_id].properties[
        "firmware_assignment_status"
    ] == "not_established"
    assert restored_model.components[probe_component_id].port_ids == [
        port.id for port in probe_ports.values()
    ]

    for connection_id, expected_values in expected.items():
        probe_id, board_id, position, pin_label, cable_label, evidence = (
            expected_values
        )
        connection = restored_model.connections[connection_id]
        assert {connection.endpoint_a_id, connection.endpoint_b_id} == {
            probe_id, board_id
        }
        assert connection.properties["documented_cable_label"] == cable_label
        assert connection.properties["notes"] == REFERENCE_WIRING_NOTE
        assert connection.provenance == evidence
        assert connection.connects_same_ports(probe_id, board_id)
        assert connection.connects_same_ports(board_id, probe_id)
        assert not connection.is_self_connection()

    restored_unused_contact_ids = {
        restored_model.ports[port_id].id for port_id in unused_contact_ids
    }
    assert all(
        not connection.contains_port(port_id)
        for connection in restored_model.connections.values()
        for port_id in restored_unused_contact_ids
    )

def test_promega_ir_probe_reference_connection_persistence_isolated(
    tmp_path,
):
    """Test round-trip persistence independently with the reusable wiring path."""
    application = QApplication.instance()
    if application is None:
        application = QApplication([])

    canvas = MachineCanvas()
    canvas.create_node_from_template(
        "duet_2_maestro_v1_0", QPointF(100.0, 100.0)
    )
    model = canvas.store.semantic_model
    controller = next(iter(model.controllers.values()))

    probe_node_id = f"node-{len(canvas.store.model.nodes) + 1}"
    canvas.create_node_from_template(
        "sensor", QPointF(220.0, 180.0)
    )
    probe_node = canvas.store.model.nodes[probe_node_id]
    probe_component_id = probe_node.semantic_reference
    assert probe_component_id is not None

    probe_component = model.components[probe_component_id]
    evidence = Provenance(
        source="Planning milestone: First Promega Reference Specimen",
        evidence_type="authored",
        method="manual transcription",
        context="IR Z probe role only; exact installed identity is unknown.",
        date="2026-10-10",
        notes=(
            "Manufacturer-reference wiring is not verification of the "
            "particular installed probe or physical harness."
        ),
    )
    properties = dict(probe_component.properties)
    properties.update({
        "specimen_scope": "promega_compound_reference",
        "verification_status": "role_only_identity_unverified",
        "physical_presence_status": "not_verified_as_built",
        "inventory_crosswalk_status": "not_established",
        "firmware_assignment_status": "not_established",
    })
    canvas.store.commit(
        UpdateMachineComponent(
            component_id=probe_component_id,
            role="IR Z probe",
            label="IR Z probe",
            properties=properties,
            provenance_entries=[evidence],
        )
    )

    probe_ports, expected = add_promega_ir_probe_reference_connections(
        canvas,
        probe_component_id=probe_component_id,
        controller_id=controller.id,
    )
    assert len(probe_ports) == 3
    assert len(expected) == 3

    destination = tmp_path / "promega-ir-probe-persistence-isolated.machine.json"
    canvas.store.save(destination)
    restored = load_editor_state(destination)
    restored_model = restored.semantic_model

    assert len(restored_model.connections) == 3
    assert len(restored.visual_model.connections) == 3
    assert restored_model.components[probe_component_id].properties[
        "physical_presence_status"
    ] == "not_verified_as_built"

    for connection_id, expected_values in expected.items():
        probe_id, board_id, position, pin_label, cable_label, evidence_entries = (
            expected_values
        )
        connection = restored_model.connections[connection_id]

        assert connection.connection_type == "electrical"
        assert connection.connects_same_ports(probe_id, board_id)
        assert connection.connects_same_ports(board_id, probe_id)
        assert not connection.is_self_connection()
        assert connection.properties["documented_cable_label"] == cable_label
        assert connection.properties["notes"] == REFERENCE_WIRING_NOTE
        assert connection.provenance == evidence_entries

        restored_probe = restored_model.ports[probe_id]
        restored_board = restored_model.ports[board_id]
        assert restored_probe.component_id == probe_component_id
        assert restored_probe.controller_id is None
        assert restored_probe.properties["physical_wiring_status"] == (
            "not_verified_as_built"
        )
        assert restored_board.controller_id == controller.id
        assert restored_board.component_id is None
        assert restored_board.connector_id == "z-probe"
        assert restored_board.properties["pin_label"] == pin_label
        assert _contact_position(restored_board) == position
