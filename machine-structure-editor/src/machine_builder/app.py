"""Application entry point for the Machine Structure Editor."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMessageBox,
)

from .canvas import MachineCanvas
from .document_controller import DocumentController
from .palette_extensions import (
    add_chamber_heater_template,
)


WINDOW_TITLE = (
    "Machine Builder — Machine Structure Editor"
)


def _update_window_title(
    window: MachineCanvas,
    controller: DocumentController,
) -> None:
    """Update the main-window title from document state."""
    title = WINDOW_TITLE

    if controller.file_path is not None:
        title = (
            f"{WINDOW_TITLE} — "
            f"{controller.document_name}"
        )

    if controller.is_modified:
        title += " *"

    window.setWindowTitle(
        title
    )


def _confirm_discard_changes(
    window: MachineCanvas,
    controller: DocumentController,
) -> bool:
    """Ask whether unsaved changes should be discarded."""
    if not controller.is_modified:
        return True

    result = QMessageBox.question(
        window,
        "Unsaved Changes",
        (
            f'"{controller.document_name}" has unsaved '
            "changes.\n\n"
            "Discard those changes?"
        ),
        QMessageBox.StandardButton.Discard
        | QMessageBox.StandardButton.Cancel,
        QMessageBox.StandardButton.Cancel,
    )

    return (
        result
        == QMessageBox.StandardButton.Discard
    )


def _save_document(
    window: MachineCanvas,
    controller: DocumentController,
) -> bool:
    """Save the current document."""
    if controller.file_path is None:
        return _save_document_as(
            window,
            controller,
        )

    try:
        controller.save()
    except OSError as exc:
        QMessageBox.critical(
            window,
            "Save Failed",
            f"Could not save the document:\n\n{exc}",
        )
        return False

    return True


def _save_document_as(
    window: MachineCanvas,
    controller: DocumentController,
) -> bool:
    """Save the current document using a selected path."""
    suggested_name = (
        controller.document_name
        if controller.file_path is not None
        else "untitled.machine.json"
    )

    path, _ = QFileDialog.getSaveFileName(
        window,
        "Save Machine Builder Document",
        suggested_name,
        (
            "Machine Builder documents "
            "(*.machine.json);;"
            "JSON files (*.json);;"
            "All files (*)"
        ),
    )

    if not path:
        return False

    try:
        controller.save_as(
            Path(path)
        )
    except OSError as exc:
        QMessageBox.critical(
            window,
            "Save Failed",
            f"Could not save the document:\n\n{exc}",
        )
        return False

    return True


def _new_document(
    window: MachineCanvas,
    controller: DocumentController,
) -> None:
    """Create a new blank document."""
    if not _confirm_discard_changes(
        window,
        controller,
    ):
        return

    controller.new_document()


def _open_document(
    window: MachineCanvas,
    controller: DocumentController,
) -> None:
    """Open a document selected by the user."""
    if not _confirm_discard_changes(
        window,
        controller,
    ):
        return

    path, _ = QFileDialog.getOpenFileName(
        window,
        "Open Machine Builder Document",
        "",
        (
            "Machine Builder documents "
            "(*.machine.json);;"
            "JSON files (*.json);;"
            "All files (*)"
        ),
    )

    if not path:
        return

    try:
        controller.open(
            Path(path)
        )
    except (
        OSError,
        ValueError,
    ) as exc:
        QMessageBox.critical(
            window,
            "Open Failed",
            f"Could not open the document:\n\n{exc}",
        )


def _create_document_actions(
    window: MachineCanvas,
    controller: DocumentController,
) -> None:
    """Create the document menu and actions."""
    menu = window.menuBar().addMenu(
        "File"
    )

    new_action = menu.addAction(
        "New"
    )

    new_action.setShortcut(
        "Ctrl+N"
    )

    new_action.triggered.connect(
        lambda: _new_document(
            window,
            controller,
        )
    )

    open_action = menu.addAction(
        "Open..."
    )

    open_action.setShortcut(
        "Ctrl+O"
    )

    open_action.triggered.connect(
        lambda: _open_document(
            window,
            controller,
        )
    )

    menu.addSeparator()

    save_action = menu.addAction(
        "Save"
    )

    save_action.setShortcut(
        "Ctrl+S"
    )

    save_action.triggered.connect(
        lambda: _save_document(
            window,
            controller,
        )
    )

    save_as_action = menu.addAction(
        "Save As..."
    )

    save_as_action.setShortcut(
        "Ctrl+Shift+S"
    )

    save_as_action.triggered.connect(
        lambda: _save_document_as(
            window,
            controller,
        )
    )


def main() -> int:
    """Create and run the Machine Structure Editor application."""
    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "Machine Structure Editor"
    )

    app.setApplicationVersion(
        "0.1.0"
    )

    window = MachineCanvas()

    document_controller = DocumentController(
        window.store
    )

    window.document_controller = (
        document_controller
    )

    document_controller.subscribe(
        lambda: _update_window_title(
            window,
            document_controller,
        )
    )

    _create_document_actions(
        window,
        document_controller,
    )

    add_chamber_heater_template(
        window
    )

    _update_window_title(
        window,
        document_controller,
    )

    window.resize(
        1400,
        900,
    )

    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(
        main()
    )