"""Semantic/model boundary between canonical and visual machine data.

The canonical Machine Builder model is the authoritative semantic
representation. The visual model represents how that information is shown
and edited in the visual editor.

This module provides the first explicit boundary between those two models.
"""

from __future__ import annotations

from .semantic_model import (
    CanonicalMachineModel,
    MachineComponent,
)
from .visual_model import (
    VisualModel,
    VisualNode,
)


class SemanticModelBoundary:
    """Resolve and validate relationships between semantic and visual data."""

    def __init__(
        self,
        canonical_model: CanonicalMachineModel | None = None,
        visual_model: VisualModel | None = None,
    ) -> None:
        self.canonical_model = (
            canonical_model
            if canonical_model is not None
            else CanonicalMachineModel()
        )

        self.visual_model = (
            visual_model
            if visual_model is not None
            else VisualModel()
        )

    def create_component(
        self,
        machine_id: str,
        component: MachineComponent,
    ) -> MachineComponent:
        """Create a canonical machine component."""
        self.canonical_model.add_component(
            machine_id,
            component,
        )

        return component

    def bind_node(
        self,
        node: VisualNode,
        component_id: str,
    ) -> None:
        """Bind a visual node to a canonical machine component."""
        if node.id not in self.visual_model.nodes:
            raise ValueError(
                f"Visual node is not in the visual model: "
                f"{node.id}"
            )

        if component_id not in self.canonical_model.components:
            raise ValueError(
                f"Canonical component does not exist: "
                f"{component_id}"
            )

        existing_reference = (
            node.semantic_reference
        )

        if (
            existing_reference is not None
            and existing_reference != component_id
        ):
            raise ValueError(
                f"Visual node {node.id} is already bound to "
                f"canonical component {existing_reference}."
            )

        node.semantic_reference = component_id

    def get_component_for_node(
        self,
        node_id: str,
    ) -> MachineComponent | None:
        """Return the canonical component represented by a visual node."""
        node = self.visual_model.nodes.get(
            node_id
        )

        if node is None:
            raise KeyError(
                f"Unknown visual node: {node_id}"
            )

        if node.semantic_reference is None:
            return None

        return self.canonical_model.components.get(
            node.semantic_reference
        )

    def get_node_for_component(
        self,
        component_id: str,
    ) -> VisualNode | None:
        """Return the visual node representing a canonical component."""
        if component_id not in self.canonical_model.components:
            raise KeyError(
                f"Unknown canonical component: {component_id}"
            )

        for node in self.visual_model.nodes.values():
            if (
                node.semantic_reference
                == component_id
            ):
                return node

        return None

    def is_bound(
        self,
        node_id: str,
    ) -> bool:
        """Return whether a visual node is bound to canonical semantics."""
        node = self.visual_model.nodes.get(
            node_id
        )

        if node is None:
            raise KeyError(
                f"Unknown visual node: {node_id}"
            )

        return node.semantic_reference is not None