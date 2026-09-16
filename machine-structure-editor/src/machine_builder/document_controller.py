"""Application-level document lifecycle for the Machine Structure Editor."""

from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Callable

from .store import ModelStore


DocumentListener = Callable[[], None]


class DocumentController:
    """Coordinate document lifecycle operations around a ModelStore.

    This layer deliberately contains no Qt code.  The GUI can use it for
    New/Open/Save/Save As operations without knowing how persistence is
    implemented.
    """

    def __init__(
        self,
        store: ModelStore | None = None,
    ) -> None:
        self.store = (
            store
            if store is not None
            else ModelStore()
        )

        self._listeners: list[
            DocumentListener
        ] = []

    @property
    def file_path(self) -> Path | None:
        """Return the current document path."""
        return self.store.file_path

    @property
    def is_modified(self) -> bool:
        """Return whether the current document has unsaved changes."""
        return self.store.is_modified

    @property
    def document_name(self) -> str:
        """Return a display name for the current document."""
        if self.file_path is None:
            return "Untitled"

        return self.file_path.name

    def subscribe(
        self,
        listener: DocumentListener,
    ) -> None:
        """Subscribe to document lifecycle changes."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unsubscribe(
        self,
        listener: DocumentListener,
    ) -> None:
        """Remove a document lifecycle listener."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def new_document(self) -> None:
        """Create a blank document."""
        self.store.new_document()
        self._notify()

    def open(
        self,
        path: str | PathLike[str] | Path,
    ) -> None:
        """Open a document from disk."""
        self.store.load(path)
        self._notify()

    def save(self) -> None:
        """Save the current document to its existing path."""
        self.store.save()
        self._notify()

    def save_as(
        self,
        path: str | PathLike[str] | Path,
    ) -> None:
        """Save the current document to a new path."""
        self.store.save(path)
        self._notify()

    def _notify(self) -> None:
        """Notify listeners that document state changed."""
        for listener in tuple(
            self._listeners
        ):
            listener()