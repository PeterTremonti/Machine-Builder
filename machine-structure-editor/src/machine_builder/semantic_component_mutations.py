"""Semantic machine-component editing mutations.

These mutations operate through EditorState so a user action can update
canonical semantic data and its visual representation atomically.

The canonical MachineComponent remains authoritative. VisualNode data is
updated only where the visual representation intentionally mirrors a
semantic field such as label.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .editor_state import EditorState
from .semantic_model import Provenance


def _find_visual_node_for_component(
    state: EditorState,
    component_id: str,
):
    """Find the visual node representing a canonical component."""
    for node in state.visual_model.nodes.values():
        if node.semantic_reference == component_id:
            return node

    return None


@dataclass(frozen=True)
class UpdateMachineComponent:
    """Update editable semantic fields of a machine component."""

    component_id: str
    role: str | None = None
    label: str | None = None
    properties: dict[str, Any] | None = None
    provenance: Provenance | None = None
    provenance_entries: list[Provenance] | None = None

    def apply(
        self,
        state: EditorState,
    ) -> None:
        component = (
            state.semantic_model.components.get(
                self.component_id
            )
        )

        if component is None:
            raise KeyError(
                "Unknown machine component: "
                f"{self.component_id}"
            )

        if self.role is not None:
            if not self.role.strip():
                raise ValueError(
                    "Machine component role "
                    "cannot be empty."
                )

            component.role = self.role

        if self.label is not None:
            component.label = self.label

            visual_node = (
                _find_visual_node_for_component(
                    state,
                    self.component_id,
                )
            )

            if visual_node is not None:
                visual_node.label = (
                    self.label
                )

        if self.properties is not None:
            component.properties = (
                self.properties.copy()
            )

        if self.provenance_entries is not None:
            component.provenance = list(
                self.provenance_entries
            )

        if self.provenance is not None:
            component.provenance.append(
                self.provenance
            )


@dataclass(frozen=True)
class SetMachineComponentProperty:
    """Set one property on a machine component."""

    component_id: str
    property_name: str
    value: Any

    def apply(
        self,
        state: EditorState,
    ) -> None:
        component = (
            state.semantic_model.components.get(
                self.component_id
            )
        )

        if component is None:
            raise KeyError(
                "Unknown machine component: "
                f"{self.component_id}"
            )

        if not self.property_name.strip():
            raise ValueError(
                "Machine component property name "
                "cannot be empty."
            )

        component.properties[
            self.property_name
        ] = self.value

class UpdateMachineComponentWithStepperTerminalProfile(UpdateMachineComponent):
    """Update component details and materialize explicitly requested stepper leads."""

    def apply(self, state: EditorState) -> None:
        from .semantic_model import Provenance, SemanticPort
        from .semantic_projection import project_component_ports

        component = state.semantic_model.components.get(self.component_id)
        if component is None:
            raise KeyError(f"Unknown machine component: {self.component_id}")

        requested_properties = (
            self.properties
            if self.properties is not None
            else component.properties
        )
        if requested_properties.get("motor_terminal_profile") != "stepper_four_lead":
            super().apply(state)
            return

        # Validate before mutation so direct calls fail atomically too.
        if requested_properties.get("visual_node_type") != "motor":
            raise ValueError(
                "motor_terminal_profile='stepper_four_lead' requires "
                "a component whose visual_node_type is 'motor'."
            )

        for index in range(1, 5):
            port_id = f"{component.id}-stepper-lead-{index}"
            existing = state.semantic_model.ports.get(port_id)
            if existing is None:
                continue
            if existing.component_id != component.id:
                raise ValueError(
                    f"Conflicting existing motor terminal port: {port_id}; "
                    "component owner does not match."
                )
            expected_metadata = {
                "interface_role": "motor_conductor_terminal",
                "interface_granularity": "physical_terminal",
                "motor_terminal_profile": "stepper_four_lead",
                "terminal_display_index": str(index),
            }
            for property_name, expected_value in expected_metadata.items():
                if existing.properties.get(property_name) != expected_value:
                    raise ValueError(
                        f"Conflicting existing motor terminal port: {port_id}; "
                        f"{property_name} must equal {expected_value!r}."
                    )

        super().apply(state)
        component = state.semantic_model.components.get(self.component_id)
        if component is None:
            raise KeyError(f"Unknown machine component: {self.component_id}")

        # These display indices distinguish four endpoints only. They do not
        # assert motor-coil pairing, wire-color mapping, or controller contacts.
        for index in range(1, 5):
            port_id = f"{component.id}-stepper-lead-{index}"
            existing = state.semantic_model.ports.get(port_id)

            if existing is not None:
                # Full terminal metadata was checked before any mutation.
                continue

            state.semantic_model.add_port(
                SemanticPort(
                    id=port_id,
                    component_id=component.id,
                    controller_id=None,
                    purpose=f"Unassigned motor lead endpoint {index}",
                    direction="unknown",
                    connector_id=None,
                    pin_id=None,
                    properties={
                        "interface_role": "motor_conductor_terminal",
                        "interface_granularity": "physical_terminal",
                        "motor_terminal_profile": "stepper_four_lead",
                        "terminal_display_index": str(index),
                        "terminal_identity_status": "unassigned",
                        "motor_coil_mapping_status": "not_established",
                        "controller_contact_mapping_status": "not_established",
                        "physical_wiring_status": "not_verified_as_built",
                        "visual_port_type": "motor",
                        "visual_side": "left",
                    },
                    provenance=[
                        Provenance(
                            source="Machine Builder stepper motor terminal profile",
                            evidence_type="authored",
                            method="explicit component profile",
                            context=(
                                "A distinct endpoint for a four-lead motor conductor. "
                                "The display index is not a physical pin number and "
                                "does not establish coil pairing or controller contact mapping."
                            ),
                            date="2026-10-19",
                            notes=(
                                "Wire color belongs to a physical SemanticConnection. "
                                "No conductor connection is created automatically."
                            ),
                        )
                    ],
                )
            )

        for visual_node in state.visual_model.nodes.values():
            if visual_node.semantic_reference != component.id:
                continue

            provisional_ports = tuple(visual_node.ports.values())
            project_component_ports(
                component,
                state.semantic_model,
                visual_node,
            )

            projected_ids = set(visual_node.ports)
            is_stepper_profile = (
                component.properties.get("motor_terminal_profile")
                == "stepper_four_lead"
            )
            connected_visual_port_ids = {
                endpoint_id
                for connection in state.visual_model.connections.values()
                for endpoint_id in (
                    connection.endpoint_a_id,
                    connection.endpoint_b_id,
                )
            }
            for provisional_port in provisional_ports:
                if (
                    provisional_port.id not in projected_ids
                    and provisional_port.semantic_reference is None
                ):
                    if (
                        is_stepper_profile
                        and provisional_port.id not in connected_visual_port_ids
                    ):
                        continue
                    visual_node.ports[provisional_port.id] = provisional_port
