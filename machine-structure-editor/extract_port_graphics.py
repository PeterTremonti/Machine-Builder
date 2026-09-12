from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent

CANVAS_PATH = (
    PROJECT_ROOT
    / "src"
    / "machine_builder"
    / "canvas.py"
)

PORT_PATH = (
    PROJECT_ROOT
    / "src"
    / "machine_builder"
    / "graphics"
    / "port.py"
)


PORT_SECTION_START = (
    "# ---------------------------------------------------------------------------\n"
    "# Port graphics\n"
    "# ---------------------------------------------------------------------------\n"
)

CONNECTION_SECTION_START = (
    "# ---------------------------------------------------------------------------\n"
    "# Connection graphics\n"
    "# ---------------------------------------------------------------------------\n"
)

CANVAS_IMPORT_MARKER = (
    "from .compatibility import (\n"
)


PORT_IMPORTS = """\
from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem

from ..visual_model import VisualPort


"""


def main() -> None:
    """Move PortGraphicsItem from canvas.py into graphics/port.py."""
    canvas_text = CANVAS_PATH.read_text(
        encoding="utf-8"
    )

    start = canvas_text.find(
        PORT_SECTION_START
    )

    if start == -1:
        raise RuntimeError(
            "Could not find the Port graphics section."
        )

    end = canvas_text.find(
        CONNECTION_SECTION_START,
        start,
    )

    if end == -1:
        raise RuntimeError(
            "Could not find the Connection graphics section."
        )

    port_section = canvas_text[
        start:end
    ]

    class_start = port_section.find(
        "class PortGraphicsItem("
    )

    if class_start == -1:
        raise RuntimeError(
            "Could not find PortGraphicsItem."
        )

    class_text = port_section[
        class_start:
    ].rstrip()

    PORT_PATH.write_text(
        PORT_IMPORTS
        + class_text
        + "\n",
        encoding="utf-8",
    )

    new_canvas_text = (
        canvas_text[:start]
        + CONNECTION_SECTION_START
        + canvas_text[
            end + len(CONNECTION_SECTION_START):
        ]
    )

    import_statement = (
        "from .graphics.port import PortGraphicsItem\n"
    )

    if import_statement not in new_canvas_text:
        new_canvas_text = new_canvas_text.replace(
            CANVAS_IMPORT_MARKER,
            import_statement
            + CANVAS_IMPORT_MARKER,
            1,
        )

    # PortGraphicsItem was the only reason canvas.py needed
    # QGraphicsEllipseItem, so remove that import.
    new_canvas_text = new_canvas_text.replace(
        "    QGraphicsEllipseItem,\n",
        "",
        1,
    )

    CANVAS_PATH.write_text(
        new_canvas_text,
        encoding="utf-8",
    )

    print("PortGraphicsItem extracted successfully.")
    print(f"Created: {PORT_PATH}")
    print(f"Updated: {CANVAS_PATH}")


if __name__ == "__main__":
    main()