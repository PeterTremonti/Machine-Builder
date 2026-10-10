from __future__ import annotations

import re

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication

from machine_builder.canvas import MachineCanvas
from machine_builder.mutations import CreateConnection
from machine_builder.persistence import load_editor_state
from machine_builder.semantic_component_mutations import UpdateMachineComponent
from machine_builder.semantic_model import Provenance, SemanticPort
from machine_builder.semantic_port_mutations import CreateSemanticPort


GUIDE_TITLE = "Promega - Duet Maestro Wiring"
GUIDE_URL = (
    "https://promega.printm3d.com/documentation/electronics/"
    "duet-maestro-wiring"
)
BOARD_CROSSWALK_SOURCE = (
    "Machine Builder #3 Controller/Board crosswalk: Duet 2 Maestro J28"
)
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


def _visual_port_id(node, canonical_port_id):
    matches = [
        port.id
        for port in node.ports.values()
        if port.semantic_reference == canonical_port_id
    ]
    assert len(matches) == 1, (
        f"Expected one visual projection for {canonical_port_id!r}; "
        f"found {len(matches)}"
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

    probe_specs = (
        ("signal", "IR Z probe signal", "signal", 1, "Z_PROBE_IN", "S10"),
        ("ground", "IR Z probe ground", "ground_reference", 2, "GND", "P5"),
        (
            "power-3v3",
            "IR Z probe 3.3 V supply",
            "power_supply_3v3",
            4,
            "+3.3V",
            "S9",
        ),
    )

    probe_ports = {}
    for suffix, purpose, functional_role, position, pin_label, cable_label in (
        probe_specs
    ):
        port_id = f"{probe_component_id}-ir-z-probe-{suffix}"
        evidence = Provenance(
            source=GUIDE_TITLE,
            evidence_type="documentation",
            method="manual source review",
            context=(
                f"IR Z probe functional endpoint {purpose}; the cited "
                f"reference associates it with cable lead {cable_label}."
            ),
            date="2026-10-10",
            notes=(
                f"Source: {GUIDE_URL}. Functional endpoint only. The probe-side "
                "connector/pin identity and installed wiring are not verified."
            ),
        )
        port = SemanticPort(
            id=port_id,
            component_id=probe_component_id,
            controller_id=None,
            purpose=purpose,
            direction="unknown",
            connector_id=None,
            pin_id=None,
            properties={
                "functional_role": functional_role,
                "physical_wiring_status": "not_verified_as_built",
                "firmware_assignment_status": "not_established",
                "evidence_source_url": GUIDE_URL,
            },
            provenance=[evidence],
        )
        canvas.store.commit(CreateSemanticPort(port))
        probe_ports[suffix] = port

    assert model.components[probe_component_id].port_ids == [
        port.id for port in probe_ports.values()
    ]
    for port in probe_ports.values():
        assert port.component_id == probe_component_id
        assert port.controller_id is None
        assert port.connector_id is None
        assert port.pin_id is None

    controller_node = next(
        node
        for node in canvas.store.model.nodes.values()
        if node.semantic_reference == controller.id
    )

    expected = {}
    for suffix, purpose, functional_role, position, pin_label, cable_label in (
        probe_specs
    ):
        probe_port = probe_ports[suffix]
        board_port = _board_probe_port(
            model, controller.id, position, pin_label
        )
        connection_id = (
            f"{probe_component_id}-ir-z-probe-connection-{suffix}"
        )
        evidence = [
            Provenance(
                source=GUIDE_TITLE,
                evidence_type="documentation",
                method="manual source review",
                context=(
                    f"Promega documents cable lead {cable_label} at J28 "
                    f"contact {position}, labelled {pin_label}."
                ),
                date="2026-10-10",
                notes=f"Source: {GUIDE_URL}. {REFERENCE_WIRING_NOTE}",
            ),
            Provenance(
                source=BOARD_CROSSWALK_SOURCE,
                evidence_type="authored",
                method="controller-port crosswalk review",
                context=(
                    f"Resolved from this instantiated controller's z-probe "
                    f"port at contact position {position}, labelled {pin_label}."
                ),
                date="2026-10-10",
                notes=(
                    "This endpoint represents the reference-board definition, "
                    "not verification of the installed board revision or "
                    f"physical wiring. {REFERENCE_WIRING_NOTE}"
                ),
            ),
        ]

        canvas.store.commit(
            CreateConnection(
                connection_id=connection_id,
                endpoint_a_id=_visual_port_id(probe_node, probe_port.id),
                endpoint_b_id=_visual_port_id(controller_node, board_port.id),
                connection_type="electrical",
                connection_properties={
                    "documented_cable_label": cable_label,
                    "notes": REFERENCE_WIRING_NOTE,
                },
                provenance_entries=evidence,
            )
        )
        expected[connection_id] = (
            probe_port.id,
            board_port.id,
            position,
            pin_label,
            cable_label,
            evidence,
        )

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

    restored_unused_contact_ids = {
        restored_model.ports[port_id].id for port_id in unused_contact_ids
    }
    assert all(
        not connection.contains_port(port_id)
        for connection in restored_model.connections.values()
        for port_id in restored_unused_contact_ids
    )