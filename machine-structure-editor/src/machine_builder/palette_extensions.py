"""Optional palette entries for the Machine Structure Editor."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem


def add_chamber_heater_template(
    window: object,
) -> None:
    """Add the real chamber-heater entry to the editor palette."""
    item = QListWidgetItem(
        "Chamber Heater"
    )

    item.setData(
        Qt.ItemDataRole.UserRole,
        "chamber_heater",
    )

    window.palette.addItem(
        item
    )