from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent

CANVAS_PATH = (
    PROJECT_ROOT
    / "src"
    / "machine_builder"
    / "canvas.py"
)

CONNECTION_PATH = (
    PROJECT_ROOT
    / "src"
    / "machine_builder"
    / "graphics"
    / "connection.py"
)


CONNECTION_SECTION_START = (
    "# ---------------------------------------------------------------------------\n"
    "# Connection graphics\n"
    "# ---------------------------------------------------------------------------\n"
)

NODE_SECTION_START = (
    "# ---------------------------------------------------------------------------\n"
    "# Node graphics\n"
    "# ---------------------------------------------------------------------------\n"
)

CANVAS_IMPORT_MARKER = (
    "from .compatibility import (\n"
)

IMPORT_STATEMENT = (
    "from .graphics.connection import ConnectionGraphicsItem\n"
)


CONNECTION_HEADER = '''"""Connection graphics for the Machine Structure Editor.

This module contains the Qt presentation class for visual connections.
The underlying connection data remains in visual_model.py.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QGraphicsLineItem


'''


def main() -> None:
    """Move ConnectionGraphicsItem from canvas.py into graphics/connection.py."""
    canvas_text = CANVAS_PATH.read_text(
        encoding="utf-8"
    )

    start = canvas_text.find(
        CONNECTION_SECTION_START
    )

    if start == -1:
        raise RuntimeError(
            "Could not find the Connection graphics section."
        )

    end = canvas_text.find(
        NODE_SECTION_START,
        start,
    )

    if end == -1:
        raise RuntimeError(
            "Could not find the Node graphics section."
        )

    connection_section = canvas_text[
        start:end
    ]

    class_start = connection_section.find(
        "class ConnectionGraphicsItem("
    )

    if class_start == -1:
        raise RuntimeError(
            "Could not find ConnectionGraphicsItem."
        )

    class_text = connection_section[
        class_start:
    ].rstrip()

    CONNECTION_PATH.write_text(
        CONNECTION_HEADER
        + class_text
        + "\n",
        encoding="utf-8",
    )

    new_canvas_text = (
        canvas_text[:start]
        + NODE_SECTION_START
        + canvas_text[
            end + len(NODE_SECTION_START):
        ]
    )

    if IMPORT_STATEMENT not in new_canvas_text:
        new_canvas_text = new_canvas_text.replace(
            CANVAS_IMPORT_MARKER,
            IMPORT_STATEMENT
            + CANVAS_IMPORT_MARKER,
            1,
        )

    CANVAS_PATH.write_text(
        new_canvas_text,
        encoding="utf-8",
    )

    print(
        "ConnectionGraphicsItem extracted successfully."
    )
    print(
        f"Created: {CONNECTION_PATH}"
    )
    print(
        f"Updated: {CANVAS_PATH}"
    )


if __name__ == "__main__":
    main()