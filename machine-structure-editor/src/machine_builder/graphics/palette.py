"""Palette graphics for the Machine Structure Editor.

This module contains the Qt palette widget used to select and drag
prototype component templates into the editor canvas.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QMimeData, Qt
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QListWidget


class PaletteList(QListWidget):
    """Palette supporting selection and drag-and-drop."""

    def startDrag(
        self,
        supported_actions: Any,
    ) -> None:
        """Start a drag containing the selected template ID."""
        item = self.currentItem()

        if item is None:
            return

        node_type = item.data(
            Qt.ItemDataRole.UserRole
        )

        if not isinstance(
            node_type,
            str,
        ):
            return

        mime_data = QMimeData()

        mime_data.setText(
            node_type
        )

        drag = QDrag(
            self
        )

        drag.setMimeData(
            mime_data
        )

        drag.exec(
            Qt.DropAction.CopyAction
        )
