"""Application entry point for the Machine Structure Editor."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from .canvas import MachineCanvas
from .palette_extensions import (
    add_chamber_heater_template,
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

    add_chamber_heater_template(
        window
    )

    window.setWindowTitle(
        "Machine Builder — Machine Structure Editor"
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