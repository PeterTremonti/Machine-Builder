from __future__ import annotations

import re

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication

from machine_builder.canvas import MachineCanvas
from machine_builder.persistence import load_editor_state
from machine_builder.promega_fixtures import (
    REFERENCE_WIRING_NOTE,
    _contact_position,
    XY_MOTOR_CONTACT_LABELS,
    add_promega_xy_motor_reference_connections,
)
from machine_builder.semantic_component_mutations import UpdateMachineComponent
from machine_builder.semantic_model import Provenance


def _create_role_component(
    canvas,
    node_type: str,
    role: str,
    position: QPointF,
) -> str:
    before = set(canvas.store.model.nodes)
    canvas.create_node_from_template(node_type, position)
    new_nodes = [
        node for node in canvas.store.model.nodes.values()
        if node.id not in before and node.node_type == node_type
    ]
    assert len(new_nodes) == 1
    component_id = new_nodes[0].semantic_reference
    assert component_id is not None

    component = canvas.store.semantic_model.components[component_id]
    reference_evidence = Provenance(
        source="Planning milestone: Promega X/Y motor reference wiring",
        evidence_type="authored",
        method="reference specimen assembly",
        context=(
            f"{role} is represented for manufacturer-reference wiring only."
        ),
        date="2026-10-11",
        notes=(
            "This is not verification that the individual cable or motor "
            "is installed on the user's machine."
        ),
    )
    properties = dict(component.properties)
    properties.update({
        "specimen_scope": "promega_compound_reference",
        "physical_presence_status": "not_verified_as_built",
        "physical_wiring_status": "not_verified_as_built",
        "firmware_assignment_status": "not_established",
    })
    canvas.store.commit(
        UpdateMachineComponent(
            component_id=component_id,
            role=role,
            label=role,
            properties=properties,
            provenance_entries=list(component.provenance) + [reference_evidence],
        )
    )
    return component_id


def _position(port) -> int:
    explicit = port.properties.get("connector_position")
    if explicit is not None:
        return int(explicit)
    match = re.search(r"(?:^|[-_])(\d+)$", port.pin_id or port.id)
    assert match is not None
    return int(match.group(1))


def test_promega_xy_motor_reference_connections_are_mating_position_based_and_persisted(
    tmp_path,
):
    if QApplication.instance() is None:
        QApplication([])

    canvas = MachineCanvas()
    canvas.create_node_from_template(
        "duet_2_maestro_v1_0", QPointF(100.0, 100.0)
    )
    controller = next(iter(canvas.store.semantic_model.controllers.values()))

    x_motor_id = _create_role_component(
        canvas, "motor", "X motion motor", QPointF(410.0, 100.0)
    )
    y_motor_id = _create_role_component(
        canvas, "motor", "Y motion motor", QPointF(410.0, 260.0)
    )
    x_cable_id = _create_role_component(
        canvas, "component", "X motor cable reference", QPointF(270.0, 100.0)
    )
    y_cable_id = _create_role_component(
        canvas, "component", "Y motor cable reference", QPointF(270.0, 260.0)
    )

    baseline_semantic = set(canvas.store.semantic_model.connections)
    baseline_visual = set(canvas.store.model.connections)

    ports, expected = add_promega_xy_motor_reference_connections(
        canvas,
        x_cable_component_id=x_cable_id,
        y_cable_component_id=y_cable_id,
        controller_id=controller.id,
    )

    assert set(ports) == {"X", "Y"}
    assert len(ports["X"]) == len(ports["Y"]) == 4
    assert len(expected) == 8
    assert len(canvas.store.semantic_model.connections) == len(baseline_semantic) + 8
    assert len(canvas.store.model.connections) == len(baseline_visual) + 8

    axis_specs = {
        "X": (x_cable_id, "x-motor", "J9 / X MOT"),
        "Y": (y_cable_id, "y-motor", "J8 / Y MOT"),
    }
    model = canvas.store.semantic_model

    for axis, (cable_component_id, connector_id, designator) in axis_specs.items():
        component = model.components[cable_component_id]
        assert set(component.port_ids) == {
            port.id for port in ports[axis].values()
        }
        board_contacts = [
            port for port in model.ports.values()
            if port.controller_id == controller.id
            and port.component_id is None
            and port.connector_id == connector_id
        ]
        assert len(board_contacts) == 4
        assert {
            port.properties.get("pin_label") for port in board_contacts
        } == set(XY_MOTOR_CONTACT_LABELS)

    for connection_id, values in expected.items():
        axis, cable_port_id, board_port_id, position, pin_label, evidence = values
        cable_component_id, connector_id, designator = axis_specs[axis]
        connection = model.connections[connection_id]
        cable_port = model.ports[cable_port_id]
        board_port = model.ports[board_port_id]

        assert connection.connection_type == "electrical"
        assert connection.connects_same_ports(cable_port_id, board_port_id)
        assert connection.connects_same_ports(board_port_id, cable_port_id)
        assert not connection.is_self_connection()
        assert connection.provenance == evidence
        expected_note = (
            f"{REFERENCE_WIRING_NOTE} Reference motor cable {axis}: "
            f"{designator} ({connector_id}), board contact {pin_label}, "
            f"mating position {position}. Position-based mating only; "
            "wire-colour-to-contact mapping and motor-coil terminal "
            "mapping are not established. Firmware drive assignment is "
            "not established."
        )
        assert connection.properties["notes"] == expected_note
        assert connection.properties["reference_board_designator"] == designator
        assert connection.properties["reference_board_connector_id"] == connector_id
        assert connection.properties["board_contact_label"] == pin_label
        assert connection.properties["mating_contact_position"] == str(position)
        assert connection.properties["mapping_basis"] == (
            "mated_connector_position_not_wire_colour"
        )
        assert connection.properties["wire_colour_to_contact_mapping_status"] == (
            "not_established"
        )
        assert connection.properties["motor_coil_terminal_mapping_status"] == (
            "not_established"
        )
        assert connection.properties["physical_wiring_status"] == (
            "not_verified_as_built"
        )
        assert connection.properties["firmware_drive_assignment_status"] == (
            "not_established"
        )

        assert cable_port.component_id == cable_component_id
        assert cable_port.controller_id is None
        assert cable_port.connector_id is None
        assert cable_port.pin_id is None
        assert cable_port.properties["reference_axis"] == axis
        assert cable_port.properties["cable_contact_position"] == str(position)
        assert cable_port.properties["reference_board_contact_label"] == pin_label
        assert cable_port.properties["motor_coil_terminal_mapping_status"] == (
            "not_established"
        )
        assert len(cable_port.provenance) == 2

        assert board_port.controller_id == controller.id
        assert board_port.component_id is None
        assert board_port.connector_id == connector_id
        assert board_port.properties["pin_label"] == pin_label
        assert _position(board_port) == position

    # No connection jumps directly to either motor component.
    motor_ids = {x_motor_id, y_motor_id}
    for connection in model.connections.values():
        endpoint_a = model.ports[connection.endpoint_a_id]
        endpoint_b = model.ports[connection.endpoint_b_id]
        assert endpoint_a.component_id not in motor_ids
        assert endpoint_b.component_id not in motor_ids

    last_connection_id = next(reversed(expected))
    assert canvas.store.undo()
    assert last_connection_id not in canvas.store.semantic_model.connections
    assert len(canvas.store.semantic_model.connections) == len(baseline_semantic) + 7
    assert canvas.store.redo()
    assert last_connection_id in canvas.store.semantic_model.connections
    assert len(canvas.store.model.connections) == len(baseline_visual) + 8

    destination = tmp_path / "promega-xy-motor-reference.machine.json"
    canvas.store.save(destination)
    restored = load_editor_state(destination)
    restored_model = restored.semantic_model

    assert len(restored_model.connections) == len(baseline_semantic) + 8
    assert len(restored.visual_model.connections) == len(baseline_visual) + 8

    for connection_id, values in expected.items():
        axis, cable_port_id, board_port_id, position, pin_label, evidence = values
        cable_component_id, connector_id, designator = axis_specs[axis]
        connection = restored_model.connections[connection_id]

        assert connection.connects_same_ports(cable_port_id, board_port_id)
        assert connection.provenance == evidence
        expected_note = (
            f"{REFERENCE_WIRING_NOTE} Reference motor cable {axis}: "
            f"{designator} ({connector_id}), board contact {pin_label}, "
            f"mating position {position}. Position-based mating only; "
            "wire-colour-to-contact mapping and motor-coil terminal "
            "mapping are not established. Firmware drive assignment is "
            "not established."
        )
        assert connection.properties["notes"] == expected_note
        assert connection.properties["reference_board_designator"] == designator
        assert connection.properties["reference_board_connector_id"] == connector_id
        assert connection.properties["board_contact_label"] == pin_label
        assert connection.properties["mating_contact_position"] == str(position)
        assert connection.properties["mapping_basis"] == (
            "mated_connector_position_not_wire_colour"
        )
        assert connection.properties["wire_colour_to_contact_mapping_status"] == (
            "not_established"
        )
        assert connection.properties["motor_coil_terminal_mapping_status"] == (
            "not_established"
        )
        assert connection.properties["physical_wiring_status"] == (
            "not_verified_as_built"
        )
        assert connection.properties["firmware_drive_assignment_status"] == (
            "not_established"
        )

        restored_cable = restored_model.ports[cable_port_id]
        restored_board = restored_model.ports[board_port_id]
        assert restored_cable.component_id == cable_component_id
        assert restored_cable.properties["reference_axis"] == axis
        assert restored_cable.properties["cable_contact_position"] == str(position)
        assert restored_cable.properties["reference_board_contact_label"] == pin_label
        assert restored_cable.properties["motor_coil_terminal_mapping_status"] == (
            "not_established"
        )
        assert len(restored_cable.provenance) == 2
        assert restored_board.connector_id == connector_id
        assert restored_board.properties["pin_label"] == pin_label

def test_contact_position_fallback_parses_numeric_pin_id_suffix():
    port = type(
        "PortWithoutExplicitPosition",
        (),
        {"properties": {}, "pin_id": "pin-1", "id": "fallback-id"},
    )()
    assert _contact_position(port) == 1
    assert _position(port) == 1
