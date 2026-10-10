"""Semantic port editing mutations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .editor_state import EditorState
from .semantic_model import Provenance, SemanticPort
from .semantic_projection import project_component_ports


def _find_visual_port(
    state: EditorState,
    port_id: str,
):
    """Find the visual port representing a semantic port."""
    for node in state.visual_model.nodes.values():
        visual_port = node.ports.get(
            port_id
        )

        if visual_port is not None:
            return visual_port

    return None


@dataclass(frozen=True)
class CreateSemanticPort:
    """Create a canonical component-owned port and project it visually."""

    port: SemanticPort

    def apply(
        self,
        state: EditorState,
    ) -> None:
        port = self.port

        if (
            port.component_id is None
            or port.controller_id is not None
        ):
            raise ValueError(
                "CreateSemanticPort requires exactly one "
                "MachineComponent owner."
            )

        component = (
            state.semantic_model.components.get(
                port.component_id
            )
        )

        if component is None:
            raise KeyError(
                "Unknown machine component: "
                f"{port.component_id}"
            )

        state.semantic_model.add_port(port)

        for visual_node in state.visual_model.nodes.values():
            if visual_node.semantic_reference == component.id:
                # Port authoring is incremental. Preserve unmatched
                # provisional palette ports so existing visual wires
                # do not lose their endpoints during projection.
                provisional_ports = tuple(
                    visual_node.ports.values()
                )

                project_component_ports(
                    component,
                    state.semantic_model,
                    visual_node,
                )

                projected_port_ids = set(
                    visual_node.ports
                )

                for provisional_port in provisional_ports:
                    if (
                        provisional_port.id
                        not in projected_port_ids
                        and provisional_port.semantic_reference
                        is None
                    ):
                        visual_node.ports[
                            provisional_port.id
                        ] = provisional_port

                break

@dataclass(frozen=True)
class UpdateSemanticPort:
    """Update editable fields of a canonical semantic port."""

    port_id: str
    purpose: str | None = None
    direction: str | None = None
    connector_id: str | None = None
    pin_id: str | None = None
    properties: dict[str, Any] | None = None
    provenance: Provenance | None = None

    def apply(
        self,
        state: EditorState,
    ) -> None:
        port = state.semantic_model.ports.get(
            self.port_id
        )

        if port is None:
            raise KeyError(
                "Unknown semantic port: "
                f"{self.port_id}"
            )

        if self.purpose is not None:
            if not self.purpose.strip():
                raise ValueError(
                    "Semantic port purpose "
                    "cannot be empty."
                )

            port.purpose = self.purpose

            visual_port = _find_visual_port(
                state,
                self.port_id,
            )

            if visual_port is not None:
                visual_port.label = (
                    self.purpose
                )

        if self.direction is not None:
            if not self.direction.strip():
                raise ValueError(
                    "Semantic port direction "
                    "cannot be empty."
                )

            port.direction = (
                self.direction
            )

            visual_port = _find_visual_port(
                state,
                self.port_id,
            )

            if visual_port is not None:
                visual_port.direction = (
                    self.direction
                )

        if self.connector_id is not None:
            port.connector_id = (
                self.connector_id
            )

        if self.pin_id is not None:
            port.pin_id = self.pin_id

        if self.properties is not None:
            port.properties = (
                self.properties.copy()
            )

        if self.provenance_entries is not None:
            port.provenance = list(
                self.provenance_entries
            )

        if self.provenance is not None:
            port.provenance.append(
                self.provenance
            )


@dataclass(frozen=True)
class SetSemanticPortProperty:
    """Set one property on a canonical semantic port."""

    port_id: str
    property_name: str
    value: Any

    def apply(
        self,
        state: EditorState,
    ) -> None:
        port = state.semantic_model.ports.get(
            self.port_id
        )

        if port is None:
            raise KeyError(
                "Unknown semantic port: "
                f"{self.port_id}"
            )

        if not self.property_name.strip():
            raise ValueError(
                "Semantic port property name "
                "cannot be empty."
            )

        port.properties[
            self.property_name
        ] = self.value