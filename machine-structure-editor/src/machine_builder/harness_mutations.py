"""Mutations for authoring canonical physical harness groupings."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from .editor_state import EditorState
from .semantic_harness import Harness
from .semantic_model import Provenance


@dataclass(frozen=True)
class CreateHarness:
    """Create one canonical harness."""

    harness: Harness

    def apply(self, state: EditorState) -> None:
        state.semantic_model.add_harness(
            deepcopy(self.harness)
        )


@dataclass(frozen=True)
class UpdateHarness:
    """Update harness metadata without changing its memberships."""

    harness_id: str
    name: str | None = None
    properties: dict[str, Any] | None = None
    provenance: list[Provenance] | None = None

    def apply(self, state: EditorState) -> None:
        harness = state.semantic_model.harnesses.get(self.harness_id)
        if harness is None:
            raise KeyError(f"Unknown harness: {self.harness_id}")

        if self.name is not None:
            if not isinstance(self.name, str) or not self.name.strip():
                raise ValueError("Harness name must be a non-empty string.")
            harness.name = self.name

        if self.properties is not None:
            harness.properties = deepcopy(self.properties)

        if self.provenance is not None:
            harness.provenance = deepcopy(self.provenance)


@dataclass(frozen=True)
class DeleteHarness:
    """Delete an empty, unreferenced harness."""

    harness_id: str

    def apply(self, state: EditorState) -> None:
        model = state.semantic_model
        harness = model.harnesses.get(self.harness_id)
        if harness is None:
            raise KeyError(f"Unknown harness: {self.harness_id}")

        if harness.member_connection_ids:
            raise ValueError(
                f"Cannot delete harness {self.harness_id}: "
                "it still has direct connection members."
            )
        if harness.child_harness_ids:
            raise ValueError(
                f"Cannot delete harness {self.harness_id}: "
                "it still has child harnesses."
            )
        if any(
            self.harness_id in candidate.child_harness_ids
            for candidate in model.harnesses.values()
            if candidate.id != self.harness_id
        ):
            raise ValueError(
                f"Cannot delete harness {self.harness_id}: "
                "it is still attached to a parent."
            )

        del model.harnesses[self.harness_id]


@dataclass(frozen=True)
class AddConnectionToHarness:
    """Add an existing canonical connection as a direct harness member."""

    harness_id: str
    connection_id: str

    def apply(self, state: EditorState) -> None:
        state.semantic_model.add_harness_connection(
            self.harness_id,
            self.connection_id,
        )


@dataclass(frozen=True)
class RemoveConnectionFromHarness:
    """Remove direct membership without deleting the physical connection."""

    harness_id: str
    connection_id: str

    def apply(self, state: EditorState) -> None:
        state.semantic_model.remove_harness_connection(
            self.harness_id,
            self.connection_id,
        )


@dataclass(frozen=True)
class AttachChildHarness:
    """Attach an existing harness as a child."""

    harness_id: str
    child_harness_id: str

    def apply(self, state: EditorState) -> None:
        state.semantic_model.add_child_harness(
            self.harness_id,
            self.child_harness_id,
        )


@dataclass(frozen=True)
class DetachChildHarness:
    """Detach a child while preserving both harnesses."""

    harness_id: str
    child_harness_id: str

    def apply(self, state: EditorState) -> None:
        state.semantic_model.remove_child_harness(
            self.harness_id,
            self.child_harness_id,
        )
