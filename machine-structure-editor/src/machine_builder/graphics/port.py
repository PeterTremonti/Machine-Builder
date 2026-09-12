"""Port graphics for the Machine Structure Editor.

This module contains the Qt presentation and interaction class for a visual
machine port. The underlying port data remains in visual_model.py.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush, QPen
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsSimpleTextItem

from ..visual_model import VisualPort


class PortGraphicsItem(QGraphicsEllipseItem):
    """Rendered representation of one VisualPort."""

    DIAMETER = 16.0

    NORMAL_FILL = QColor("#d7dde8")
    NORMAL_BORDER = QColor("#667085")

    HOVER_FILL = QColor("#58a6ff")
    HOVER_BORDER = QColor("#d7ecff")

    SOURCE_FILL = QColor("#f2c94c")
    SOURCE_BORDER = QColor("#fff3b0")

    VALID_FILL = QColor("#4caf50")
    VALID_BORDER = QColor("#d8ffd8")

    UNKNOWN_FILL = QColor("#9b8cff")
    UNKNOWN_BORDER = QColor("#ebe7ff")

    INVALID_FILL = QColor("#d9534f")
    INVALID_BORDER = QColor("#ffd7d5")

    def __init__(
        self,
        port: VisualPort,
        connection_drag_started: Any,
        connection_drag_moved: Any,
        connection_drag_finished: Any,
    ) -> None:
        radius = self.DIAMETER / 2.0

        super().__init__(
            -radius,
            -radius,
            self.DIAMETER,
            self.DIAMETER,
        )

        self.port_id = port.id
        self._side = port.side.lower().strip()

        self._connection_drag_started = connection_drag_started
        self._connection_drag_moved = connection_drag_moved
        self._connection_drag_finished = connection_drag_finished

        self._hovered = False
        self._connection_state: str = "normal"

        self.setBrush(
            QBrush(self.NORMAL_FILL)
        )
        self.setPen(
            QPen(
                self.NORMAL_BORDER,
                1.2,
            )
        )

        self.setZValue(20.0)

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
            False,
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            False,
        )

        self.setAcceptHoverEvents(True)

        self.setAcceptedMouseButtons(
            Qt.MouseButton.LeftButton
        )

        self.setToolTip(
            self._build_tooltip(port)
        )

    @staticmethod
    def _build_tooltip(
        port: VisualPort,
    ) -> str:
        """Build a concise tooltip describing the port."""
        lines = [
            port.label or "Interface",
            f"Type: {port.port_type}",
            f"Direction: {port.direction}",
        ]

        return "\n".join(lines)

    def set_connection_state(
        self,
        state: str,
    ) -> None:
        """Set the temporary connection feedback state."""
        self._connection_state = state
        self._apply_visual_state()

    def _apply_visual_state(self) -> None:
        """Apply the current visual state."""
        if self._connection_state == "source":
            fill = self.SOURCE_FILL
            border = self.SOURCE_BORDER

        elif self._connection_state == "valid":
            fill = self.VALID_FILL
            border = self.VALID_BORDER

        elif self._connection_state == "unknown":
            fill = self.UNKNOWN_FILL
            border = self.UNKNOWN_BORDER

        elif self._connection_state == "invalid":
            fill = self.INVALID_FILL
            border = self.INVALID_BORDER

        elif self._hovered:
            fill = self.HOVER_FILL
            border = self.HOVER_BORDER

        else:
            fill = self.NORMAL_FILL
            border = self.NORMAL_BORDER

        self.setBrush(
            QBrush(fill)
        )

        self.setPen(
            QPen(
                border,
                1.5
                if self._connection_state != "normal"
                else 1.2,
            )
        )

    def hoverEnterEvent(
        self,
        event: Any,
    ) -> None:
        """Highlight a port under the pointer."""
        self._hovered = True
        self._apply_visual_state()

        super().hoverEnterEvent(
            event
        )

    def hoverLeaveEvent(
        self,
        event: Any,
    ) -> None:
        """Restore the port appearance after hover."""
        self._hovered = False
        self._apply_visual_state()

        super().hoverLeaveEvent(
            event
        )

    def mousePressEvent(
        self,
        event: Any,
    ) -> None:
        """Start a connection directly from this port."""
        if (
            event.button()
            != Qt.MouseButton.LeftButton
        ):
            event.ignore()
            return

        event.accept()

        scene_position = event.scenePos()

        self._connection_drag_started(
            self.port_id,
            scene_position,
        )

    def mouseMoveEvent(
        self,
        event: Any,
    ) -> None:
        """Continue the connection preview."""
        if (
            event.buttons()
            & Qt.MouseButton.LeftButton
        ):
            event.accept()

            self._connection_drag_moved(
                self.port_id,
                event.scenePos(),
            )

            return

        super().mouseMoveEvent(
            event
        )

    def mouseReleaseEvent(
        self,
        event: Any,
    ) -> None:
        """Finish or cancel the connection attempt."""
        if (
            event.button()
            != Qt.MouseButton.LeftButton
        ):
            event.ignore()
            return

        event.accept()

        self._connection_drag_finished(
            self.port_id,
            event.scenePos(),
        )