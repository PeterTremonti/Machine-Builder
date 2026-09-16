"""Application state store for the Machine Structure Editor.

The store owns both sides of the editor's model boundary:

    VisualModel
        presentation and editing state

    CanonicalMachineModel
        authoritative machine semantics

V0.2 uses complete EditorState snapshots for undo/redo so a meaningful
user action can update both models atomically.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Callable

from .editor_state import EditorState
from .mutations import Mutation
from .semantic_model import CanonicalMachineModel
from .visual_model import VisualModel


ModelListener = Callable[[VisualModel], None]


class ModelStore:
    """Own the editor state and its edit history."""

    def __init__(
        self,
        model: VisualModel | None = None,
        semantic_model: CanonicalMachineModel | None = None,
    ) -> None:
        self._state = EditorState(
            visual_model=(
                model
                if model is not None
                else VisualModel()
            ),
            semantic_model=(
                semantic_model
                if semantic_model is not None
                else CanonicalMachineModel()
            ),
        )

        self._undo_stack: list[
            EditorState
        ] = []

        self._redo_stack: list[
            EditorState
        ] = []

        self._listeners: list[
            ModelListener
        ] = []

    @property
    def model(self) -> VisualModel:
        """Return the current visual model.

        This property is retained for compatibility with the existing
        visual editor code.
        """
        return self._state.visual_model

    @property
    def semantic_model(
        self,
    ) -> CanonicalMachineModel:
        """Return the current canonical semantic model."""
        return self._state.semantic_model

    @property
    def state(self) -> EditorState:
        """Return the complete editor state."""
        return self._state

    @property
    def can_undo(self) -> bool:
        """Return whether an undo operation is available."""
        return bool(
            self._undo_stack
        )

    @property
    def can_redo(self) -> bool:
        """Return whether a redo operation is available."""
        return bool(
            self._redo_stack
        )

    def subscribe(
        self,
        listener: ModelListener,
    ) -> None:
        """Subscribe to visual-model changes."""
        if listener not in self._listeners:
            self._listeners.append(
                listener
            )

    def unsubscribe(
        self,
        listener: ModelListener,
    ) -> None:
        """Remove a previously registered listener."""
        if listener in self._listeners:
            self._listeners.remove(
                listener
            )

    def commit(
        self,
        mutation: Mutation,
    ) -> None:
        """Apply a mutation atomically.

        If the mutation fails, restore the complete pre-mutation state and
        leave undo/redo history unchanged.
        """
        before = deepcopy(
            self._state
        )

        try:
            mutation.apply(
                self._state
            )
        except Exception:
            self._state = before
            raise

        self._undo_stack.append(
            before
        )

        self._redo_stack.clear()

        self._notify()

    def undo(self) -> bool:
        """Undo the most recent committed mutation."""
        if not self._undo_stack:
            return False

        previous = self._undo_stack.pop()

        self._redo_stack.append(
            deepcopy(
                self._state
            )
        )

        self._state = previous

        self._notify()

        return True

    def redo(self) -> bool:
        """Redo the most recently undone mutation."""
        if not self._redo_stack:
            return False

        next_state = self._redo_stack.pop()

        self._undo_stack.append(
            deepcopy(
                self._state
            )
        )

        self._state = next_state

        self._notify()

        return True

    def replace_model(
        self,
        model: VisualModel,
    ) -> None:
        """Replace the visual model."""
        self._state = EditorState(
            visual_model=model,
            semantic_model=self._state.semantic_model,
        )

        self._undo_stack.clear()
        self._redo_stack.clear()

        self._notify()

    def replace_semantic_model(
        self,
        semantic_model: CanonicalMachineModel,
    ) -> None:
        """Replace the canonical semantic model."""
        self._state = EditorState(
            visual_model=self._state.visual_model,
            semantic_model=semantic_model,
        )

        self._undo_stack.clear()
        self._redo_stack.clear()

        self._notify()

    def clear_history(self) -> None:
        """Clear undo and redo history without changing the state."""
        self._undo_stack.clear()
        self._redo_stack.clear()

    def _notify(self) -> None:
        """Notify listeners that editor state changed."""
        for listener in tuple(
            self._listeners
        ):
            listener(
                self._state.visual_model
            )