"""Mutations for authoring canonical semantic relationships."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .editor_state import EditorState
from .semantic_relationship import SemanticRelationship


@dataclass(frozen=True)
class CreateSemanticRelationship:
    """Create one canonical semantic relationship."""

    relationship: SemanticRelationship

    def apply(
        self,
        state: EditorState,
    ) -> None:
        state.semantic_model.add_relationship(
            self.relationship
        )


@dataclass(frozen=True)
class DeleteSemanticRelationship:
    """Delete one canonical semantic relationship."""

    relationship_id: str

    def apply(
        self,
        state: EditorState,
    ) -> None:
        state.semantic_model.remove_relationship(
            self.relationship_id
        )