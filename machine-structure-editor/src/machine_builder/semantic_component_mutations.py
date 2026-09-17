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