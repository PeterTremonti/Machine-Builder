"""Mutations for authoring canonical controller resources."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .editor_state import EditorState
from .semantic_model import Provenance


@dataclass
class UpdateControllerResource:
    """Update the authored fields of a controller resource."""

    resource_id: str
    name: str
    resource_type: str
    controller_id: str | None = None
    properties: dict[str, Any] = field(default_factory=dict)
    provenance: list[Provenance] = field(default_factory=list)

    def apply(self, state: EditorState) -> None:
        """Apply the resource update to the canonical model."""
        resource = state.semantic_model.get_controller_resource(
            self.resource_id
        )

        if not self.name.strip():
            raise ValueError(
                "Controller resource name cannot be empty."
            )

        if not self.resource_type.strip():
            raise ValueError(
                "Controller resource type cannot be empty."
            )

        if self.controller_id is not None:
            if self.controller_id not in state.semantic_model.controllers:
                raise ValueError(
                    "Unknown controller: "
                    f"{self.controller_id}"
                )

            resource_machine_id = (
                state.semantic_model._machine_for_canonical_object(
                    self.resource_id
                )
            )
            controller_machine_id = (
                state.semantic_model._machine_for_canonical_object(
                    self.controller_id
                )
            )

            if (
                resource_machine_id is not None
                and controller_machine_id is not None
                and resource_machine_id != controller_machine_id
            ):
                raise ValueError(
                    "Controller belongs to a different machine: "
                    f"{self.controller_id}"
                )

        resource.name = self.name
        resource.resource_type = self.resource_type
        resource.controller_id = self.controller_id
        resource.properties = dict(self.properties)
        resource.provenance = list(self.provenance)


@dataclass
class SetControllerResourceProperty:
    """Set one property on a controller resource."""

    resource_id: str
    name: str
    value: Any

    def apply(self, state: EditorState) -> None:
        """Set the requested property."""
        resource = state.semantic_model.get_controller_resource(
            self.resource_id
        )

        property_name = self.name.strip()

        if not property_name:
            raise ValueError(
                "Controller resource property name cannot be empty."
            )

        resource.properties[property_name] = self.value