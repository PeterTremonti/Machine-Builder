"""Queries for controller-to-visual semantic authoring."""

from __future__ import annotations

from .controller import Controller
from .editor_state import EditorState
from .visual_model import VisualNode


def get_controller(
    state: EditorState,
    controller_id: str,
) -> Controller:
    """Return a canonical controller."""
    controller = state.semantic_model.controllers.get(
        controller_id
    )

    if controller is None:
        raise KeyError(
            "Unknown controller: "
            f"{controller_id}"
        )

    return controller


def controller_for_visual_node(
    state: EditorState,
    node_id: str,
) -> Controller | None:
    """Resolve a visual node to its canonical controller."""
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

    return get_controller(
        state,
        node.semantic_reference,
    )


def visual_node_for_controller(
    state: EditorState,
    controller_id: str,
) -> VisualNode | None:
    """Resolve a canonical controller to its visual representation."""
    get_controller(
        state,
        controller_id,
    )

    for node in state.visual_model.nodes.values():
        if node.semantic_reference == controller_id:
            return node

    return None


def controller_id_for_visual_node(
    state: EditorState,
    node_id: str,
) -> str | None:
    """Return the canonical controller ID referenced by a visual node."""
    node = state.visual_model.nodes.get(
        node_id
    )

    if node is None:
        raise KeyError(
            "Unknown visual node: "
            f"{node_id}"
        )

    return node.semantic_reference