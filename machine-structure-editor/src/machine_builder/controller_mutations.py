"""Canonical controller editing mutations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .editor_state import EditorState
from .semantic_model import Provenance


def _find_visual_node_for_controller(
    state: EditorState,
    controller_id: str,
):
    """Find the visual node representing a canonical controller."""
    for node in state.visual_model.nodes.values():
        if node.semantic_reference == controller_id:
            return node

    return None


@dataclass(frozen=True)
class UpdateController:
    """Update editable fields of a canonical controller."""

    controller_id: str
    name: str | None = None
    controller_type: str | None = None
    version: str | None = None
    properties: dict[str, Any] | None = None
    provenance: Provenance | None = None

    def apply(
        self,
        state: EditorState,
    ) -> None:
        controller = (
            state.semantic_model.controllers.get(
                self.controller_id
            )
        )
        if controller is None:
            raise KeyError(
                "Unknown controller: "
                f"{self.controller_id}"
            )

        if self.name is not None:
            if not self.name.strip():
                raise ValueError(
                    "Controller name cannot be empty."
                )

            controller.name = self.name

            visual_node = (
                _find_visual_node_for_controller(
                    state,
                    self.controller_id,
                )
            )

            if visual_node is not None:
                visual_node.label = self.name

        if self.controller_type is not None:
            if not self.controller_type.strip():
                raise ValueError(
                    "Controller type cannot be empty."
                )

            controller.controller_type = (
                self.controller_type
            )

        if self.version is not None:
            controller.version = (
                self.version.strip()
                or None
            )

        if self.properties is not None:
            controller.properties = (
                self.properties.copy()
            )

        if self.provenance is not None:
            controller.provenance.append(
                self.provenance
            )


@dataclass(frozen=True)
class SetControllerProperty:
    """Set one property on a canonical controller."""

    controller_id: str
    property_name: str
    value: Any

    def apply(
        self,
        state: EditorState,
    ) -> None:
        controller = (
            state.semantic_model.controllers.get(
                self.controller_id
            )
        )

        if controller is None:
            raise KeyError(
                "Unknown controller: "
                f"{self.controller_id}"
            )

        if not self.property_name.strip():
            raise ValueError(
                "Controller property name cannot be empty."
            )

        controller.properties[
            self.property_name
        ] = self.value