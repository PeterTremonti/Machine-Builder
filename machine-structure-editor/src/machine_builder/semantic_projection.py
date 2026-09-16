"""Projection helpers between canonical semantics and visual presentation.

The canonical semantic model is authoritative. This module projects
canonical information into visual objects without making visual presentation
part of the canonical model.
"""

from __future__ import annotations

from copy import deepcopy

from .semantic_model import (
    CanonicalMachineModel,
    MachineComponent,
    SemanticPort,
)
from .visual_model import (
    VisualNode,
    VisualPort,
)


def project_component_ports(
    component: MachineComponent,
    semantic_model: CanonicalMachineModel,
    visual_node: VisualNode,
) -> None:
    """Project canonical component ports onto a visual node.

    Existing visual port placement information is preserved when a visual
    port can be matched by semantic reference or purpose. The canonical
    port remains authoritative for identity, purpose, direction, and other
    semantic information.

    This function changes only the visual node.
    """
    existing_ports = tuple(
        visual_node.ports.values()
    )

    projected_ports: dict[
        str,
        VisualPort,
    ] = {}

    for port_id in component.port_ids:
        canonical_port = semantic_model.get_port(
            port_id
        )

        existing_visual = (
            _find_matching_visual_port(
                existing_ports,
                canonical_port,
            )
        )

        if existing_visual is not None:
            visual_port = VisualPort(
                id=existing_visual.id,
                node_id=visual_node.id,
                label=canonical_port.purpose,
                port_type=(
                    existing_visual.port_type
                ),
                direction=canonical_port.direction,
                semantic_reference=canonical_port.id,
                side=existing_visual.side,
                order=existing_visual.order,
            )
        else:
            visual_port = VisualPort(
                id=_visual_port_id(
                    visual_node.id,
                    canonical_port,
                ),
                node_id=visual_node.id,
                label=canonical_port.purpose,
                port_type=_default_visual_port_type(
                    canonical_port
                ),
                direction=canonical_port.direction,
                semantic_reference=canonical_port.id,
                side="left",
                order=len(
                    projected_ports
                ),
            )

        projected_ports[
            visual_port.id
        ] = visual_port

    visual_node.ports = projected_ports


def _find_matching_visual_port(
    existing_ports: tuple[VisualPort, ...],
    canonical_port: SemanticPort,
) -> VisualPort | None:
    """Find an existing visual port corresponding to a canonical port."""
    for visual_port in existing_ports:
        if (
            visual_port.semantic_reference
            == canonical_port.id
        ):
            return visual_port

    purpose = canonical_port.purpose.lower().strip()

    for visual_port in existing_ports:
        label = (
            visual_port.label
            or ""
        ).lower().strip()

        if label == purpose:
            return visual_port

    return None


def _visual_port_id(
    node_id: str,
    canonical_port: SemanticPort,
) -> str:
    """Build a stable visual ID for a projected canonical port."""
    normalized = (
        canonical_port.purpose
        .lower()
        .replace(" ", "-")
    )

    return (
        f"{node_id}-{normalized}"
    )


def _default_visual_port_type(
    canonical_port: SemanticPort,
) -> str:
    """Choose a presentation type without changing canonical meaning."""
    purpose = (
        canonical_port.purpose
        .lower()
        .strip()
    )

    if purpose == "power":
        return "power"

    if purpose in {
        "ground",
        "signal",
        "sensor",
        "temperature",
    }:
        return "electrical"

    if purpose in {
        "motor",
        "fan",
        "heater",
    }:
        return purpose

    return "unknown"