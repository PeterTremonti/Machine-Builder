"""Application state store for the Machine Structure Editor.

The store owns both sides of the editor's model boundary:

    VisualModel
        presentation and editing state

    CanonicalMachineModel
        authoritative machine semantics

V0.2 uses complete EditorState snapshots for undo/redo so a meaningful
user action can update both models atomically.

Persistence is deliberately kept outside the model classes. The store
provides the application-level save/load boundary for complete editor
state and tracks the document's file path and modified state.
"""

from __future__ import annotations

from copy import deepcopy
from os import PathLike
from pathlib import Path
from typing import Callable

from .editor_state import EditorState
from .mutations import Mutation
from .persistence import load_editor_state, save_editor_state
from .semantic_model import CanonicalMachineModel
from .visual_model import VisualModel


ModelListener = Callable[[VisualModel], None]


class ModelStore:
    """Own the editor state, document state, and edit history."""

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

        self._undo_stack: list[EditorState] = []
        self._redo_stack: list[EditorState] = []
        self._listeners: list[ModelListener] = []

        self._file_path: Path | None = None
        self._modified = False

    @property
    def model(self) -> VisualModel:
        """Return the current visual model.

        This property is retained for compatibility with existing
        visual-editor code.
        """
        return self._state.visual_model

    @property
    def semantic_model(self) -> CanonicalMachineModel:
        """Return the current canonical semantic model."""
        return self._state.semantic_model

    @property
    def state(self) -> EditorState:
        """Return the complete editor state."""
        return self._state

    @property
    def can_undo(self) -> bool:
        """Return whether an undo operation is available."""
        return bool(self._undo_stack)

    @property
    def can_redo(self) -> bool:
        """Return whether a redo operation is available."""
        return bool(self._redo_stack)

    @property
    def file_path(self) -> Path | None:
        """Return the current document path, if one is associated."""
        return self._file_path

    @property
    def is_modified(self) -> bool:
        """Return whether the document has unsaved changes."""
        return self._modified

    def subscribe(
        self,
        listener: ModelListener,
    ) -> None:
        """Subscribe to visual-model changes."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unsubscribe(
        self,
        listener: ModelListener,
    ) -> None:
        """Remove a previously registered listener."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def commit(
        self,
        mutation: Mutation,
    ) -> None:
        """Apply a mutation atomically."""
        before = deepcopy(self._state)

        try:
            mutation.apply(self._state)
        except Exception:
            self._state = before
            raise

        self._undo_stack.append(before)
        self._redo_stack.clear()
        self._modified = True

        self._notify()

    def undo(self) -> bool:
        """Undo the most recent committed mutation."""
        if not self._undo_stack:
            return False

        previous = self._undo_stack.pop()

        self._redo_stack.append(
            deepcopy(self._state)
        )

        self._state = previous
        self._modified = True

        self._notify()

        return True

    def redo(self) -> bool:
        """Redo the most recently undone mutation."""
        if not self._redo_stack:
            return False

        next_state = self._redo_stack.pop()

        self._undo_stack.append(
            deepcopy(self._state)
        )

        self._state = next_state
        self._modified = True

        self._notify()

        return True

    def new_document(self) -> None:
        """Replace the current document with a blank editor state.

        A new document has no associated file path, no edit history, and
        no unsaved changes. It is therefore a clean editing baseline.
        """
        self._state = EditorState(
            visual_model=VisualModel(),
            semantic_model=CanonicalMachineModel(),
        )

        self._undo_stack.clear()
        self._redo_stack.clear()

        self._file_path = None
        self._modified = False

        self._notify()

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
        self._modified = True

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
        self._modified = True

        self._notify()

    def save(
        self,
        path: str | PathLike[str] | Path | None = None,
    ) -> None:
        """Save the complete editor state.

        When ``path`` is omitted, the previously associated document
        path is used. Saving establishes that path as the current
        document path and clears the modified flag.
        """
        target = (
            Path(path)
            if path is not None
            else self._file_path
        )

        if target is None:
            raise ValueError(
                "No document path specified."
            )

        save_editor_state(
            self._state,
            target,
        )

        self._file_path = target
        self._modified = False

    def load(
        self,
        path: str | PathLike[str] | Path,
    ) -> None:
        """Load a complete editor state from disk.

        Loading replaces the current state and establishes the loaded
        file as the current document. Undo/redo history is cleared and
        the resulting state is considered clean.
        """
        target = Path(path)

        state = load_editor_state(
            target,
        )

        self._state = state

        self._undo_stack.clear()
        self._redo_stack.clear()

        self._file_path = target
        self._modified = False

        self._notify()

    def clear_history(self) -> None:
        """Clear undo and redo history without changing document state."""
        self._undo_stack.clear()
        self._redo_stack.clear()

    def _notify(self) -> None:
        """Notify listeners that editor state changed."""
        for listener in tuple(self._listeners):
            listener(self._state.visual_model)