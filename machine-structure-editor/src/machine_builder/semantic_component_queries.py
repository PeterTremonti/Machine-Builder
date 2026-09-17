"""Queries for machine-component semantic authoring.

This module keeps component lookup and visual-to-semantic resolution out
of the visual editor itself.
"""

from __future__ import annotations

from .editor_state import EditorState
from .semantic_model import (
    MachineComponent,
    SemanticPort,
)


def get_component(
    state: EditorState,
    component_id: str,
) -> MachineComponent:
    """Return a canonical machine component."""
    component = (
        state.semantic_model.components.get(
            component_id
        )
    )

    if component is None:
        raise KeyError(
            "Unknown machine component: "
            f"{component_id}"
        )

    return component


def component_for_visual_node(
    state: EditorState,
    node_id: str,
) -> MachineComponent | None:
    """Resolve a visual node to its canonical component."""
    node = state.visual_model.nodes.get(
        node_id
    )

    if node is None:
        raise KeyError(
            "Unknown visual node: "
            f"{node_id}"
        )

    if node.semantic_reference is None:
        return None

    return get_component(
        state,
        node.semantic_reference,
    )


def visual_node_for_component(
    state: EditorState,
    component_id: str,
):
    """Resolve a canonical component to its visual representation."""
    get_component(
        state,
        component_id,
    )

    for node in state.visual_model.nodes.values():
        if (
            node.semantic_reference
            == component_id
        ):
            return node

    return None


def ports_for_component(
    state: EditorState,
    component_id: str,
) -> tuple[SemanticPort, ...]:
    """Return canonical ports belonging to a component."""
    component = get_component(
        state,
        component_id,
    )

    return tuple(
        state.semantic_model.ports[
            port_id
        ]
        for port_id in component.port_ids
        if port_id
        in state.semantic_model.ports
    )


def machine_id_for_component(
    state: EditorState,
    component_id: str,
) -> str:
    """Return the machine that owns a component."""
    get_component(
        state,
        component_id,
    )

    for (
        machine_id,
        machine,
    ) in state.semantic_model.machines.items():
        if component_id in machine.component_ids:
            return machine_id

    raise ValueError(
        "Component is not attached to a machine: "
        f"{component_id}"
    )


def component_id_for_visual_node(
    state: EditorState,
    node_id: str,
) -> str | None:
    """Return the semantic component ID for a visual node."""
    node = state.visual_model.nodes.get(
        node_id
    )

    if node is None:
        raise KeyError(
            "Unknown visual node: "
            f"{node_id}"
        )

    return node.semantic_reference