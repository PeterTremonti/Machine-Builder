"""Shared composition path for the Promega reference specimen.

The specimen records approved semantic roles and manufacturer-reference paths.
It does not assert unverified as-built hardware identity or wiring.
"""

from __future__ import annotations


from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication

from .canvas import MachineCanvas
from .editor_state import EditorState

from .promega_fixtures import (
    add_promega_firmware_configuration_evidence,
    add_promega_ir_probe_reference_connections,
    add_promega_operational_fan_assignments,
    add_promega_xy_motor_reference_connections,
    add_promega_z_motor_resource_assignment,
)
from .semantic_component_mutations import UpdateMachineComponent
from .semantic_model import Provenance


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

_ROLE_EVIDENCE_SOURCE = "Planning milestone: First Promega Reference Specimen"
_ROLE_EVIDENCE_METHOD = "manual transcription"
_ROLE_EVIDENCE_NOTES = (
    "Exact installed identity, physical variant, and wiring remain "
    "unverified; no part number or endpoint is inferred."
)

def build_promega_reference_specimen() -> EditorState:
    """Build a fresh, detached EditorState for the Promega reference specimen.

    Construction uses a private MachineCanvas and its existing template and
    canonical-mutation paths. The caller receives the complete EditorState;
    no active application document is passed in or mutated.

    The fourteen PROMEGA_ROLES entries are role-only components. The two
    additional X/Y cable-reference components represent documented reference
    paths, not verified as-built cables or conductor mappings.
    """
    if QApplication.instance() is None:
        raise RuntimeError(
            "A QApplication must exist before building the Promega specimen."
        )

    canvas = MachineCanvas()
    if len(PROMEGA_ROLES) != 14 or len({role for role, _ in PROMEGA_ROLES}) != 14:
        raise RuntimeError("PROMEGA_ROLES must contain fourteen unique roles.")

    model = canvas.store.semantic_model
    visual_model = canvas.store.model
    if (
        visual_model.nodes
        or model.controllers
        or model.components
        or model.connections
        or model.ports
        or model.controller_resource_assignments
    ):
        raise ValueError(
            "Promega specimen composition requires a blank MachineCanvas; "
            "refusing to append to or duplicate content in an existing document."
        )

    canvas.create_node_from_template(
        "duet_2_maestro_v1_0",
        QPointF(100.0, 100.0),
    )
    if len(model.controllers) != 1:
        raise RuntimeError("Maestro template did not create exactly one controller.")
    controller = next(iter(model.controllers.values()))

    component_ids: dict[str, str] = {}
    role_evidence: dict[str, Provenance] = {}

    def add_role(role: str, node_type: str, x: float, y: float) -> str:
        previous_node_ids = set(canvas.store.model.nodes)
        canvas.create_node_from_template(node_type, QPointF(x, y))
        added_nodes = [
            node
            for node in canvas.store.model.nodes.values()
            if node.id not in previous_node_ids
        ]
        if len(added_nodes) != 1 or added_nodes[0].node_type != node_type:
            raise RuntimeError(
                f"Template creation did not produce exactly one {node_type!r} "
                f"node for specimen role {role!r}."
            )

        component_id = added_nodes[0].semantic_reference
        if component_id is None or component_id not in model.components:
            raise RuntimeError(
                f"Template node for specimen role {role!r} has no canonical component."
            )
        if role in component_ids:
            raise RuntimeError(f"Duplicate Promega specimen role: {role!r}.")

        component = model.components[component_id]
        evidence = Provenance(
            source=_ROLE_EVIDENCE_SOURCE,
            evidence_type="authored",
            method=_ROLE_EVIDENCE_METHOD,
            context=f"Planning-defined role only: {role}.",
            date="2026-10-24",
            notes=_ROLE_EVIDENCE_NOTES,
        )
        properties = dict(component.properties)
        properties.update(
            {
                "specimen_scope": "promega_compound_reference",
                "verification_status": "role_only_identity_unverified",
                "physical_presence_status": "not_verified_as_built",
                "physical_wiring_status": "not_verified_as_built",
                "inventory_crosswalk_status": "not_established",
                "firmware_assignment_status": "not_established",
                "inventory_crosswalk_notes": (
                    "No product identity or inventory identifier inferred."
                ),
            }
        )
        canvas.store.commit(
            UpdateMachineComponent(
                component_id=component_id,
                role=role,
                label=role,
                properties=properties,
                provenance_entries=[evidence],
            )
        )
        component_ids[role] = component_id
        role_evidence[role] = evidence
        return component_id

    for index, (role, node_type) in enumerate(PROMEGA_ROLES, start=1):
        add_role(
            role,
            node_type,
            100.0 + index * 65.0,
            130.0 + index * 28.0,
        )

    x_cable_id = add_role("X motor cable reference", "component", 280.0, 110.0)
    y_cable_id = add_role("Y motor cable reference", "component", 280.0, 260.0)

    x_motor_id = component_ids["X motion motor"]
    y_motor_id = component_ids["Y motion motor"]
    z_motor_id = component_ids["Z motion motor"]
    probe_id = component_ids["IR Z probe"]
    fan_ids = {
        role: component_ids[role]
        for role in (
            "Hotend heatsink/cold-section fan",
            "Part-cooling/nozzle fan",
        )
    }

    _xy_ports, xy_expected = add_promega_xy_motor_reference_connections(
        canvas,
        x_cable_id,
        y_cable_id,
        controller.id,
    )
    _probe_ports, probe_expected = add_promega_ir_probe_reference_connections(
        canvas,
        probe_id,
        controller.id,
    )
    fan_evidence = add_promega_operational_fan_assignments(
        canvas,
        fan_ids,
        controller.id,
    )
    configuration_evidence = add_promega_firmware_configuration_evidence(
        canvas,
        controller.id,
    )
    z_assignment = add_promega_z_motor_resource_assignment(
        canvas,
        z_motor_id,
        controller.id,
    )

    expected_roles = {role for role, _kind in PROMEGA_ROLES} | {
        "X motor cable reference",
        "Y motor cable reference",
    }
    actual_roles = {component.role for component in model.components.values()}
    if (
        len(model.controllers) != 1
        or len(model.components) != 16
        or actual_roles != expected_roles
        or len(xy_expected) != 8
        or len(probe_expected) != 3
        or len(model.connections) != 11
        or len(model.controller_resource_assignments) != 3
    ):
        raise RuntimeError(
            "Composed Promega specimen failed its structural checks: "
            f"controllers={len(model.controllers)}, "
            f"components={len(model.components)}, "
            f"connections={len(model.connections)}, "
            f"assignments={len(model.controller_resource_assignments)}."
        )

    return canvas.store.state
