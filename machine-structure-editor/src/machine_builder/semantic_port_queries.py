"""Queries for semantic port authoring and inspection."""

from __future__ import annotations

from .editor_state import EditorState
from .semantic_model import MachineComponent, SemanticPort


def get_port(
    state: EditorState,
    port_id: str,
) -> SemanticPort:
    """Return a canonical semantic port."""
    port = state.semantic_model.ports.get(
        port_id
    )

    if port is None:
        raise KeyError(
            "Unknown semantic port: "
            f"{port_id}"
        )

    return port


def component_for_port(
    state: EditorState,
    port_id: str,
) -> MachineComponent:
    """Return the canonical component owning a port."""
    port = get_port(
        state,
        port_id,
    )

    component = (
        state.semantic_model.components.get(
            port.component_id
        )
    )

    if component is None:
        raise ValueError(
            "Semantic port refers to an "
            "unknown component: "
            f"{port.component_id}"
        )

    return component


def visual_port_for_semantic_port(
    state: EditorState,
    port_id: str,
):
    """Return the visual port representing a semantic port."""
    get_port(
        state,
        port_id,
    )

    for node in state.visual_model.nodes.values():
        for visual_port in node.ports.values():
            if (
                visual_port.semantic_reference
                == port_id
            ):
                return visual_port

    return None


def visual_node_for_semantic_port(
    state: EditorState,
    port_id: str,
):
    """Return the visual node containing a semantic port."""
    get_port(
        state,
        port_id,
    )

    for node in state.visual_model.nodes.values():
        for visual_port in node.ports.values():
            if (
                visual_port.semantic_reference
                == port_id
            ):
                return node

    return None


def machine_id_for_port(
    state: EditorState,
    port_id: str,
) -> str:
    """Return the machine owning the component that owns a port."""
    component = component_for_port(
        state,
        port_id,
    )

    for (
        machine_id,
        machine,
    ) in state.semantic_model.machines.items():
        if component.id in machine.component_ids:
            return machine_id

    raise ValueError(
        "Component owning semantic port is not "
        "attached to a machine: "
        f"{component.id}"
    )


def port_id_for_visual_port(
    state: EditorState,
    visual_node_id: str,
    visual_port_id: str,
) -> str | None:
    """Return a semantic port ID from a visual port."""
    node = state.visual_model.nodes.get(
        visual_node_id
    )

    if node is None:
        raise KeyError(
            "Unknown visual node: "
            f"{visual_node_id}"
        )

    visual_port = node.ports.get(
        visual_port_id
    )

    if visual_port is None:
        raise KeyError(
            "Unknown visual port: "
            f"{visual_port_id}"
        )

    return visual_port.semantic_reference


def semantic_ports_for_component(
    state: EditorState,
    component_id: str,
) -> tuple[SemanticPort, ...]:
    """Return all canonical ports belonging to a component."""
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

    return tuple(
        state.semantic_model.ports[
            port_id
        ]
        for port_id in component.port_ids
        if port_id
        in state.semantic_model.ports
    )