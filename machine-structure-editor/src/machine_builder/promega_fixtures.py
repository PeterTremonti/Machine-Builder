"""Promega manufacturer-reference wiring fixture.

Connections describe documented reference mappings, not inspected wiring
on an individual installed machine.
"""

from __future__ import annotations

import re
from typing import Any

from .mutations import CreateConnection
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
        and _contact_position(port) == position
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
