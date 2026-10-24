"""Promega manufacturer-reference wiring fixture.

Connections describe documented reference mappings, not inspected wiring
on an individual installed machine.
"""

from __future__ import annotations

import re
from typing import Any

from .controller_resource import ControllerResource
from .controller_resource_assignment import ControllerResourceAssignment
from .semantic_relationship import SemanticRelationship
from .mutations import CreateConnection
from .semantic_component_mutations import UpdateMachineComponent
from .semantic_model import Provenance, SemanticPort
from .semantic_port_mutations import CreateSemanticPort


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

PROBE_SPECS = (
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


def _contact_position(port: SemanticPort) -> int:
    explicit_position = port.properties.get("connector_position")
    if explicit_position is not None:
        return int(explicit_position)

    for identity in (port.pin_id, port.id):
        match = re.search(r"(?:^|[-_])(\d+)$", identity or "")
        if match:
            return int(match.group(1))

    raise ValueError(
        f"No contact position metadata found for board port {port.id!r}"
    )


def _promega_diagram_view_position(port: SemanticPort) -> int:
    """Resolve the J28 position only from its source-qualified Promega guide identity."""
    position = port.properties.get("promega_diagram_view_position")
    source = port.properties.get("promega_diagram_view_source")
    if position is None or source != GUIDE_URL:
        raise ValueError(
            f"Board port {port.id!r} has no source-qualified Promega guide-view position"
        )
    return int(position)


def _visual_node(canvas: Any, semantic_reference: str) -> Any:
    matches = [
        node
        for node in canvas.store.model.nodes.values()
        if node.semantic_reference == semantic_reference
    ]
    if len(matches) != 1:
        raise ValueError(
            f"Expected one visual node for {semantic_reference!r}; "
            f"found {len(matches)}"
        )
    return matches[0]


def _visual_port_id(node: Any, canonical_port_id: str) -> str:
    matches = [
        port.id
        for port in node.ports.values()
        if port.semantic_reference == canonical_port_id
    ]
    if len(matches) != 1:
        raise ValueError(
            f"Expected one visual projection for {canonical_port_id!r}; "
            f"found {len(matches)}"
        )
    return matches[0]


def _board_probe_port(
    model: Any,
    controller_id: str,
    position: int,
    pin_label: str,
) -> SemanticPort:
    matches = [
        port
        for port in model.ports.values()
        if port.controller_id == controller_id
        and port.component_id is None
        and port.connector_id == "z-probe"
        and _promega_diagram_view_position(port) == position
        and port.properties.get("pin_label") == pin_label
    ]
    if len(matches) != 1:
        raise ValueError(
            f"Expected one controller-owned J28 contact {position} "
            f"labelled {pin_label!r}; found {len(matches)}"
        )
    return matches[0]


def add_promega_ir_probe_reference_connections(
    canvas: Any,
    probe_component_id: str,
    controller_id: str,
) -> tuple[
    dict[str, SemanticPort],
    dict[str, tuple[str, str, int, str, str, list[Provenance]]],
]:
    """Add the three documented IR-probe-to-Maestro J28 connections.

    The existing specimen, probe component, and controller interfaces must
    already exist. Probe-side connector identity and physical installation
    are not inferred or marked as verified.
    """
    model = canvas.store.semantic_model
    probe_component = model.components.get(probe_component_id)
    if probe_component is None:
        raise ValueError(f"Unknown IR Z probe component: {probe_component_id}")
    if probe_component.role != "IR Z probe":
        raise ValueError(
            f"Component {probe_component_id!r} is not the IR Z probe role"
        )
    if probe_component.port_ids:
        raise ValueError(
            f"IR Z probe component already has ports: {probe_component_id}"
        )
    if controller_id not in model.controllers:
        raise ValueError(f"Unknown controller: {controller_id}")

    probe_node = _visual_node(canvas, probe_component_id)
    controller_node = _visual_node(canvas, controller_id)

    # Resolve all board contacts before mutating the specimen.
    board_ports = {
        suffix: _board_probe_port(model, controller_id, position, pin_label)
        for suffix, _purpose, _role, position, pin_label, _cable
        in PROBE_SPECS
    }

    port_ids = [
        f"{probe_component_id}-ir-z-probe-{suffix}"
        for suffix, *_rest in PROBE_SPECS
    ]
    connection_ids = [
        f"{probe_component_id}-ir-z-probe-connection-{suffix}"
        for suffix, *_rest in PROBE_SPECS
    ]
    if any(port_id in model.ports for port_id in port_ids):
        raise ValueError("One or more IR-probe port IDs already exist")
    if any(connection_id in model.connections for connection_id in connection_ids):
        raise ValueError("One or more IR-probe connection IDs already exist")

    probe_ports: dict[str, SemanticPort] = {}
    for suffix, purpose, functional_role, _position, _pin_label, cable_label in PROBE_SPECS:
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
                f"Source: {GUIDE_URL}. Functional endpoint only. The "
                "probe-side connector/pin identity and installed wiring "
                "are not verified."
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

    expected: dict[
        str, tuple[str, str, int, str, str, list[Provenance]]
    ] = {}

    for suffix, _purpose, _role, position, pin_label, cable_label in PROBE_SPECS:
        probe_port = probe_ports[suffix]
        board_port = board_ports[suffix]
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
                    f"Resolved from the instantiated controller's z-probe "
                    f"port at contact position {position}, labelled {pin_label}."
                ),
                date="2026-10-10",
                notes=(
                    "This is the reference-board definition, not verification "
                    "of the installed board revision or physical wiring. "
                    f"{REFERENCE_WIRING_NOTE}"
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

    return probe_ports, expected

XY_MOTOR_CONTACT_LABELS = ("B1", "B2", "A1", "A2")
XY_MOTOR_BOARD_SOURCE = (
    "Machine Builder #3 Controller/Board crosswalk: "
    "Duet 2 Maestro J9/J8 motor contacts"
)
XY_MOTOR_REFERENCE_SPECS: dict[str, tuple[str, str, str]] = {
    "X": ("x-motor", "J9 / X MOT", "X motor cable reference"),
    "Y": ("y-motor", "J8 / Y MOT", "Y motor cable reference"),
}


def _xy_motor_visual_node(canvas: Any, semantic_reference: str) -> Any:
    """Resolve one visual node for the supplied component/controller reference."""
    model = canvas.store.semantic_model
    matches = [
        node
        for node in canvas.store.model.nodes.values()
        if node.semantic_reference == semantic_reference
        or any(
            visual_port.semantic_reference in model.ports
            and model.ports[visual_port.semantic_reference].controller_id
            == semantic_reference
            for visual_port in node.ports.values()
        )
    ]
    if len(matches) != 1:
        raise ValueError(
            f"Expected one visual node for semantic reference "
            f"{semantic_reference!r}; found {len(matches)}"
        )
    return matches[0]


def _xy_motor_board_contact_ports(
    canvas: Any,
    controller_id: str,
    connector_id: str,
) -> dict[int, SemanticPort]:
    """Resolve the four controller-owned labelled contacts of a motor connector."""
    matches = [
        port
        for port in canvas.store.semantic_model.ports.values()
        if port.controller_id == controller_id
        and port.component_id is None
        and port.connector_id == connector_id
        and port.pin_id is not None
    ]
    if len(matches) != 4:
        raise ValueError(
            f"Expected four controller-owned contacts on {connector_id!r}; "
            f"found {len(matches)}"
        )

    by_position: dict[int, SemanticPort] = {}
    for port in matches:
        position = _contact_position(port)
        if position in by_position:
            raise ValueError(
                f"Duplicate position {position} on connector {connector_id!r}"
            )
        by_position[position] = port

    if set(by_position) != {1, 2, 3, 4}:
        raise ValueError(
            f"Connector {connector_id!r} does not expose positions 1 through 4"
        )

    for position, expected_label in enumerate(XY_MOTOR_CONTACT_LABELS, start=1):
        actual_label = by_position[position].properties.get("pin_label")
        if actual_label != expected_label:
            raise ValueError(
                f"Connector {connector_id!r} position {position} should be "
                f"labelled {expected_label!r}; found {actual_label!r}"
            )
    return by_position


def add_promega_xy_motor_reference_connections(
    canvas: Any,
    x_cable_component_id: str,
    y_cable_component_id: str,
    controller_id: str,
) -> tuple[
    dict[str, dict[int, SemanticPort]],
    dict[str, tuple[str, str, str, int, str, list[Provenance]]],
]:
    """Create reference-only X/Y cable-contact-to-Maestro mating connections.

    Connections are based on documented connector position. Wire-colour mapping,
    motor-coil terminals, firmware drive assignments, and as-built wiring remain
    unresolved.
    """
    if x_cable_component_id == y_cable_component_id:
        raise ValueError("X and Y reference cables must be separate components")

    model = canvas.store.semantic_model
    if controller_id not in model.controllers:
        raise ValueError(f"Unknown controller: {controller_id}")

    controller_node = _xy_motor_visual_node(canvas, controller_id)
    component_ids = {"X": x_cable_component_id, "Y": y_cable_component_id}
    created_ports: dict[str, dict[int, SemanticPort]] = {}
    expected: dict[
        str, tuple[str, str, str, int, str, list[Provenance]]
    ] = {}

    for axis, (connector_id, designator, required_role) in XY_MOTOR_REFERENCE_SPECS.items():
        component_id = component_ids[axis]
        component = model.components.get(component_id)
        if component is None:
            raise ValueError(f"Unknown {axis} motor cable reference component: {component_id}")
        if component.role != required_role:
            raise ValueError(
                f"{axis} cable component must have role {required_role!r}; "
                f"found {component.role!r}"
            )
        if component.port_ids:
            raise ValueError(
                f"{axis} cable reference component already has ports; "
                "refusing to duplicate reference contacts"
            )

        cable_node = _xy_motor_visual_node(canvas, component_id)
        board_ports = _xy_motor_board_contact_ports(
            canvas, controller_id, connector_id
        )
        created_ports[axis] = {}

        for position, pin_label in enumerate(XY_MOTOR_CONTACT_LABELS, start=1):
            board_port = board_ports[position]
            cable_port_id = (
                f"{component_id}-promega-{axis.lower()}-motor-cable-contact-{position}"
            )
            evidence = [
                Provenance(
                    source=GUIDE_TITLE,
                    evidence_type="documentation",
                    method="manual source review",
                    context=(
                        f"Promega identifies the {axis} motor connection as a "
                        f"four-position plug. Position {position} is modelled as "
                        f"mating to {designator} contact {pin_label}; no conductor "
                        "colour or motor-coil terminal is assigned."
                    ),
                    date="2026-10-11",
                    notes=(
                        f"Source: {GUIDE_URL}. The guide does not establish "
                        "wire-colour-to-contact or motor-coil terminal mapping. "
                        f"{REFERENCE_WIRING_NOTE}"
                    ),
                ),
                Provenance(
                    source=XY_MOTOR_BOARD_SOURCE,
                    evidence_type="authored",
                    method="controller-port crosswalk review",
                    context=(
                        f"Resolved connector {connector_id}, position {position}, "
                        f"labelled {pin_label} on {designator}. Mating is positional "
                        "only, not an inferred internal conductor mapping."
                    ),
                    date="2026-10-11",
                    notes=(
                        "Reference-board identity only; not verification of the "
                        "installed board, cable termination, motor-coil pinout, "
                        "or firmware assignment."
                    ),
                ),
            ]

            cable_port = SemanticPort(
                id=cable_port_id,
                component_id=component_id,
                controller_id=None,
                purpose=f"{axis} motor cable contact at mating position {position}",
                direction="unknown",
                connector_id=None,
                pin_id=None,
                properties={
                    "reference_axis": axis,
                    "connector_position": str(position),
                    "cable_contact_position": str(position),
                    "reference_board_designator": designator,
                    "reference_board_connector_id": connector_id,
                    "reference_board_contact_label": pin_label,
                    "mapping_basis": "mated_connector_position_not_wire_colour",
                    "wire_colour_to_contact_mapping_status": "not_established",
                    "motor_coil_terminal_mapping_status": "not_established",
                    "physical_wiring_status": "not_verified_as_built",
                    "firmware_drive_assignment_status": "not_established",
                },
                provenance=evidence,
            )
            canvas.store.commit(CreateSemanticPort(cable_port))
            created_ports[axis][position] = cable_port

            connection_id = (
                f"{component_id}-promega-{axis.lower()}-motor-reference-{position}"
            )
            connection_evidence = list(cable_port.provenance)
            connection_note = (
                f"{REFERENCE_WIRING_NOTE} Reference motor cable {axis}: "
                f"{designator} ({connector_id}), board contact {pin_label}, "
                f"mating position {position}. Position-based mating only; "
                "wire-colour-to-contact mapping and motor-coil terminal "
                "mapping are not established. Firmware drive assignment is "
                "not established."
            )

            canvas.store.commit(
                CreateConnection(
                    connection_id=connection_id,
                    endpoint_a_id=_visual_port_id(cable_node, cable_port.id),
                    endpoint_b_id=_visual_port_id(controller_node, board_port.id),
                    connection_type="electrical",
                    connection_properties={
                        "reference_board_designator": designator,
                        "reference_board_connector_id": connector_id,
                        "board_contact_label": pin_label,
                        "mating_contact_position": str(position),
                        "mapping_basis": "mated_connector_position_not_wire_colour",
                        "wire_colour_to_contact_mapping_status": "not_established",
                        "motor_coil_terminal_mapping_status": "not_established",
                        "physical_wiring_status": "not_verified_as_built",
                        "firmware_drive_assignment_status": "not_established",
                        "notes": connection_note,
                    },
                    provenance_entries=connection_evidence,
                )
            )

            expected[connection_id] = (
                axis,
                cable_port.id,
                board_port.id,
                position,
                pin_label,
                connection_evidence,
            )

    return created_ports, expected


PROMEGA_OPERATIONAL_FAN_ASSIGNMENTS = {
    "Hotend heatsink/cold-section fan": (
        "fan0",
        "0",
        "hotend heatsink/cold-section fan",
    ),
    "Part-cooling/nozzle fan": (
        "fan2",
        "2",
        "paired side part-cooling fans",
    ),
}

PROMEGA_FAN_OUTPUT_RESOURCE_SPECS = (
    ("fan0", "fan-0", "Fan 0", "FAN0/P0", "controlled_fan_output", "controlled"),
    ("fan1", "fan-1", "Fan 1", "FAN1/P1", "controlled_fan_output", "controlled"),
    ("fan2", "fan-2", "Fan 2", "FAN2/P2", "controlled_fan_output", "controlled"),
    ("always-on-fan", "always-on-fan", "Always-on fan", "Always-on fan output", "always_on_fan_output", "always_on"),
)


def add_promega_operational_fan_assignments(
    canvas: Any,
    fan_component_ids: dict[str, str],
    controller_id: str,
) -> dict[str, Provenance]:
    """Record user-reported assignments to canonical controller fan resources."""
    model = canvas.store.semantic_model
    if controller_id not in model.controllers:
        raise ValueError(f"Unknown controller: {controller_id}")

    machine_ids = [
        machine.id
        for machine in model.machines.values()
        if controller_id in machine.controller_ids
    ]
    if len(machine_ids) != 1:
        raise ValueError(
            f"Expected one owning machine for controller {controller_id!r}; "
            f"found {len(machine_ids)}"
        )
    machine_id = machine_ids[0]

    components = {}
    for role in PROMEGA_OPERATIONAL_FAN_ASSIGNMENTS:
        component_id = fan_component_ids.get(role)
        component = model.components.get(component_id or "")
        if component is None or component.role != role:
            raise ValueError(f"Missing Promega fan component for role {role!r}")
        if component.properties.get("operational_assignment_status") == "user_reported_operational":
            raise ValueError(f"Operational fan assignment already recorded for {role!r}")
        source_machine_id = model._machine_for_canonical_object(component.id)
        if source_machine_id is not None and source_machine_id != machine_id:
            raise ValueError(f"Fan component belongs to another machine: {component.id}")
        components[role] = component

    ports_by_connector = {}
    for connector_id, _suffix, _name, _label, _electrical_role, mode in PROMEGA_FAN_OUTPUT_RESOURCE_SPECS:
        ports = [
            port
            for port in model.ports.values()
            if port.controller_id == controller_id
            and port.component_id is None
            and port.connector_id == connector_id
        ]
        if len(ports) != 2:
            raise ValueError(
                f"Expected two board contacts for {connector_id!r}; found {len(ports)}"
            )
        contact_roles = {
            port.properties.get("electrical_role")
            for port in ports
        }
        if mode == "controlled":
            valid_roles = contact_roles == {"controlled_fan_output"}
        else:
            valid_roles = (
                "always_on_fan_output" in contact_roles
                and "ground_reference" in contact_roles
            )
        if not valid_roles:
            raise ValueError(
                f"Unexpected contact roles for {connector_id!r}: {contact_roles}"
            )
        ports_by_connector[connector_id] = ports

    resource_ids = {}
    for connector_id, suffix, _name, _label, _electrical_role, _mode in PROMEGA_FAN_OUTPUT_RESOURCE_SPECS:
        resource_id = f"{controller_id}-{suffix}"
        existing = model.controller_resources.get(resource_id)
        if existing is not None and (
            existing.controller_id != controller_id
            or existing.resource_type != "fan_output"
            or existing.properties.get("board_connector_id") != connector_id
        ):
            raise ValueError(f"Conflicting existing fan resource {resource_id!r}")
        if existing is not None and model._machine_for_canonical_object(resource_id) != machine_id:
            raise ValueError(f"Fan resource belongs to another machine: {resource_id}")
        resource_ids[connector_id] = resource_id

    assignment_ids = {
        role: f"{components[role].id}-promega-operational-fan-assignment"
        for role in PROMEGA_OPERATIONAL_FAN_ASSIGNMENTS
    }
    for assignment_id in assignment_ids.values():
        if assignment_id in model.controller_resource_assignments:
            raise ValueError(f"Fan assignment already exists: {assignment_id}")

    for connector_id, suffix, name, output_label, electrical_role, mode in PROMEGA_FAN_OUTPUT_RESOURCE_SPECS:
        resource_id = resource_ids[connector_id]
        if resource_id not in model.controller_resources:
            resource_evidence = Provenance(
                source="Machine Builder Duet 2 Maestro reference-board definition",
                evidence_type="authored",
                method="board connector inventory",
                context=(
                    f"Controller resource for {output_label}, exposed through "
                    f"the existing {connector_id!r} board connector contacts."
                ),
                date="2026-10-23",
                notes=(
                    "Board resource/contact exposure only. No fan, installed harness, "
                    "or conductor-to-contact mapping is asserted."
                ),
            )
            model.add_controller_resource(
                machine_id,
                ControllerResource(
                    id=resource_id,
                    name=name,
                    resource_type="fan_output",
                    controller_id=controller_id,
                    properties={
                        "board_connector_id": connector_id,
                        "board_output_label": output_label,
                        "electrical_role": electrical_role,
                        "output_mode": mode,
                        "physical_conductor_mapping_status": "not_established",
                    },
                    provenance=[resource_evidence],
                ),
            )

        for port in ports_by_connector[connector_id]:
            relationship_id = f"{resource_id}-exposed-through-{port.id}"
            existing_relationship = model.relationships.get(relationship_id)
            if existing_relationship is not None:
                if (
                    existing_relationship.source_id != resource_id
                    or existing_relationship.target_id != port.id
                    or existing_relationship.relationship_type != "exposed_through"
                ):
                    raise ValueError(f"Conflicting resource exposure {relationship_id!r}")
                continue

            model.add_relationship(
                SemanticRelationship(
                    id=relationship_id,
                    source_id=resource_id,
                    target_id=port.id,
                    relationship_type="exposed_through",
                    properties={
                        "board_connector_id": connector_id,
                        "physical_conductor_mapping_status": "not_established",
                    },
                    provenance=[
                        Provenance(
                            source="Machine Builder Duet 2 Maestro reference-board definition",
                            evidence_type="authored",
                            method="board connector inventory",
                            context=(
                                f"The {output_label} resource is exposed through "
                                "this board contact; no fan conductor is assigned."
                            ),
                            date="2026-10-23",
                            notes=(
                                "Contact exposure does not verify a connected fan or "
                                "the Promega P9/P11 physical cable crosswalk."
                            ),
                        )
                    ],
                )
            )

    assigned: dict[str, Provenance] = {}
    for role, (connector_id, fan_index, description) in PROMEGA_OPERATIONAL_FAN_ASSIGNMENTS.items():
        component = components[role]
        resource_id = resource_ids[connector_id]
        evidence = Provenance(
            source="User-reported installed Promega operational configuration",
            evidence_type="user_report",
            method="user report",
            context=(
                f"User reports the {description} operates from the Duet 2 Maestro "
                f"controlled output FAN{fan_index}/P{fan_index}."
            ),
            date="2026-10-23",
            notes=(
                "Operational assignment only; not independent physical inspection. "
                "Promega P9/P11 cable-to-output crosswalk, conductor-to-contact "
                "mapping, polarity, and installed SD-card configuration remain "
                "unverified."
            ),
        )
        model.add_controller_resource_assignment(
            machine_id,
            ControllerResourceAssignment(
                id=assignment_ids[role],
                source_id=component.id,
                resource_id=resource_id,
                assignment_type="controls",
                properties={
                    "semantic_role": "fan",
                    "operational_assignment_status": "user_reported_operational",
                    "operational_assignment_basis": "user_reported_working_installation",
                    "board_connector_id": connector_id,
                    "output_label": f"FAN{fan_index}/P{fan_index}",
                    "physical_output_contact_mapping_status": "not_established",
                    "physical_cable_crosswalk_status": "not_established",
                },
                provenance=[evidence],
            ),
        )

        properties = dict(component.properties)
        properties.update({
            "operational_assignment_status": "user_reported_operational",
            "operational_assignment_basis": "user_reported_working_installation",
            "operational_controller_id": controller_id,
            "operational_output_connector_id": connector_id,
            "operational_output_index": fan_index,
            "operational_output_label": f"FAN{fan_index}/P{fan_index}",
            "operational_output_resource_id": resource_id,
            "physical_output_contact_mapping_status": "not_established",
            "physical_cable_crosswalk_status": "not_established",
        })
        canvas.store.commit(
            UpdateMachineComponent(
                component_id=component.id,
                role=component.role,
                label=component.label,
                properties=properties,
                provenance_entries=list(component.provenance) + [evidence],
            )
        )
        assigned[role] = evidence

    return assigned
