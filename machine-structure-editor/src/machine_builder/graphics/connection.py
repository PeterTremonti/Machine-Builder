"""Connection graphics for the Machine Structure Editor.

This module contains the Qt presentation class for visual connections.
The underlying connection data remains in visual_model.py.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QGraphicsLineItem

from ..visual_model import VisualConnection


class ConnectionGraphicsItem(QGraphicsLineItem):
    """Rendered representation of one committed VisualConnection."""

    def __init__(
        self,
        connection: VisualConnection,
    ) -> None:
        super().__init__()

        self.connection_id = connection.id
        self.source_port_id = connection.source_port_id
        self.target_port_id = connection.target_port_id

        self.setPen(
            QPen(
                QColor("#aab4c4"),
                2.0,
            )
        )

        # Keep connections visually behind components and ports.
        self.setZValue(-10.0)

        # Connections do not intercept mouse interaction yet.
        # Connection selection/deletion will be added after the refactor.
        self.setAcceptedMouseButtons(
            Qt.MouseButton.NoButton
        )