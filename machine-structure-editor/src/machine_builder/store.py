"""Application state store for the Machine Structure Editor.

The store owns the current VisualModel and is the boundary through which
mutations are committed.

V0.1 uses model snapshots for undo/redo.  This is intentionally simple and
reliable.  A more sophisticated command history can replace this later if
the application's scale makes snapshots inefficient.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Callable

from .mutations import Mutation
from .visual_model import VisualModel


ModelListener = Callable[[VisualModel], None]


class ModelStore:
    """Own the current visual model and its edit history."""

    def __init__(self, model: VisualModel | None = None) -> None:
        self._model = model if model is not None else VisualModel()

        # Each history entry is a complete model snapshot taken immediately
        # before a committed mutation.
        self._undo_stack: list[VisualModel] = []

        # Redo snapshots represent the model state that was replaced by an
        # undo operation.
        self._redo_stack: list[VisualModel] = []

        self._listeners: list[ModelListener] = []

    @property
    def model(self) -> VisualModel:
        """Return the current visual model."""
        return self._model

    @property
    def can_undo(self) -> bool:
        """Return whether an undo operation is available."""
        return bool(self._undo_stack)

    @property
    def can_redo(self) -> bool:
        """Return whether a redo operation is available."""
        return bool(self._redo_stack)

    def subscribe(self, listener: ModelListener) -> None:
        """Subscribe to model changes.

        Listeners are called after the model changes.
        """
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unsubscribe(self, listener: ModelListener) -> None:
        """Remove a previously registered listener."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def commit(self, mutation: Mutation) -> None:
        """Apply a mutation and record it in the undo history."""
        before = deepcopy(self._model)

        mutation.apply(self._model)

        self._undo_stack.append(before)
        self._redo_stack.clear()

        self._notify()

    def undo(self) -> bool:
        """Undo the most recent committed mutation.

        Returns True when an undo occurred and False when there was nothing
        to undo.
        """
        if not self._undo_stack:
            return False

        previous = self._undo_stack.pop()

        self._redo_stack.append(deepcopy(self._model))
        self._model = previous

        self._notify()
        return True

    def redo(self) -> bool:
        """Redo the most recently undone mutation.

        Returns True when a redo occurred and False when there was nothing
        to redo.
        """
        if not self._redo_stack:
            return False

        next_model = self._redo_stack.pop()

        self._undo_stack.append(deepcopy(self._model))
        self._model = next_model

        self._notify()
        return True

    def replace_model(self, model: VisualModel) -> None:
        """Replace the current model.

        This is intended for future project loading and similar operations.

        Loading a project establishes a new editing starting point, so the
        existing edit history is cleared.
        """
        self._model = model
        self._undo_stack.clear()
        self._redo_stack.clear()

        self._notify()

    def clear_history(self) -> None:
        """Clear undo and redo history without changing the model."""
        self._undo_stack.clear()
        self._redo_stack.clear()

    def _notify(self) -> None:
        """Notify subscribers that the model has changed."""
        for listener in tuple(self._listeners):
            listener(self._model)