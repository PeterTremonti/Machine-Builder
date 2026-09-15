"""Port graphics for the Machine Structure Editor.

This module contains the Qt presentation and interaction class for a visual
machine port. The underlying port data remains in visual_model.py.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsSimpleTextItem,
)

from ..visual_model import VisualPort


class PortGraphicsItem(QGraphicsEllipseItem):
    """Presentation object for one VisualPort."""

    DIAMETER = 18.0

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

    LABEL_COLOR = QColor("#f0f0f0")
    ICON_COLOR = QColor("#20242b")
    STATUS_COLOR = QColor("#20242b")

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

        self._connection_drag_started = (
            connection_drag_started
        )
        self._connection_drag_moved = (
            connection_drag_moved
        )
        self._connection_drag_finished = (
            connection_drag_finished
        )

        self._hovered = False
        self._connection_state: str = "normal"

        self.setBrush(
            QBrush(
                self.NORMAL_FILL
            )
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

        # Persistent purpose icon.
        self._icon_item = QGraphicsSimpleTextItem(
            self._purpose_icon(port),
            self,
        )

        self._icon_item.setBrush(
            QBrush(
                self.ICON_COLOR
            )
        )

        self._icon_item.setAcceptedMouseButtons(
            Qt.MouseButton.NoButton
        )

        self._icon_item.setZValue(1.0)

        # Persistent port identity.
        self._label_item = QGraphicsSimpleTextItem(
            port.label or "Interface",
            self,
        )

        self._label_item.setBrush(
            QBrush(
                self.LABEL_COLOR
            )
        )

        self._label_item.setAcceptedMouseButtons(
            Qt.MouseButton.NoButton
        )

        # Non-color status indicator.
        self._status_item = QGraphicsSimpleTextItem(
            "",
            self,
        )

        self._status_item.setBrush(
            QBrush(
                self.STATUS_COLOR
            )
        )

        self._status_item.setAcceptedMouseButtons(
            Qt.MouseButton.NoButton
        )

        self._status_item.setZValue(2.0)

        self._position_icon()
        self._position_label()
        self._position_status()

    @staticmethod
    def _purpose_icon(
        port: VisualPort,
    ) -> str:
        """Return a simple purpose-based visual icon for the port."""

        port_type = (
            port.port_type or ""
        ).lower().strip()

        label = (
            port.label or ""
        ).lower().strip()

        searchable = (
            f"{port_type} {label}"
        )

        if any(
            word in searchable
            for word in (
                "fan",
                "blower",
            )
        ):
            return "🌀"

        if any(
            word in searchable
            for word in (
                "heater",
                "heating",
                "heat",
            )
        ):
            return "🔥"

        if any(
            word in searchable
            for word in (
                "temperature",
                "thermistor",
                "thermocouple",
                "temp",
            )
        ):
            return "🌡"

        if any(
            word in searchable
            for word in (
                "motor",
                "stepper",
                "stepper motor",
            )
        ):
            return "↻"

        if any(
            word in searchable
            for word in (
                "power",
                "voltage",
                "24v",
                "12v",
                "5v",
                "ac",
                "dc",
            )
        ):
            return "⚡"

        if any(
            word in searchable
            for word in (
                "endstop",
                "end stop",
                "limit",
                "switch",
            )
        ):
            return "□"

        return "•"

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

    def _position_icon(self) -> None:
        """Center the purpose icon over the port."""
        icon_rect = (
            self._icon_item.boundingRect()
        )

        self._icon_item.setPos(
            -icon_rect.width() / 2.0,
            -icon_rect.height() / 2.0 - 1.0,
        )

    def _position_label(self) -> None:
        """Place the persistent port label outside the node."""
        label_rect = (
            self._label_item.boundingRect()
        )

        gap = 8.0

        if self._side == "left":
            self._label_item.setPos(
                -label_rect.width() - gap,
                -label_rect.height() / 2.0,
            )

        elif self._side == "right":
            self._label_item.setPos(
                gap,
                -label_rect.height() / 2.0,
            )

        elif self._side == "top":
            self._label_item.setPos(
                -label_rect.width() / 2.0,
                -label_rect.height() - gap,
            )

        elif self._side == "bottom":
            self._label_item.setPos(
                -label_rect.width() / 2.0,
                gap,
            )

        else:
            self._label_item.setPos(
                gap,
                -label_rect.height() / 2.0,
            )

    def _position_status(self) -> None:
        """Center the connection-status symbol over the port."""
        status_rect = (
            self._status_item.boundingRect()
        )

        self._status_item.setPos(
            -status_rect.width() / 2.0,
            -status_rect.height() / 2.0 - 1.0,
        )

    def set_connection_state(
        self,
        state: str,
    ) -> None:
        """Set temporary connection feedback state."""
        self._connection_state = state
        self._apply_visual_state()

    def _apply_visual_state(self) -> None:
        """Apply color and non-color connection feedback."""

        if self._connection_state == "source":
            fill = self.SOURCE_FILL
            border = self.SOURCE_BORDER
            symbol = ""

        elif self._connection_state == "valid":
            fill = self.VALID_FILL
            border = self.VALID_BORDER
            symbol = "✓"

        elif self._connection_state == "unknown":
            fill = self.UNKNOWN_FILL
            border = self.UNKNOWN_BORDER
            symbol = "?"

        elif self._connection_state == "invalid":
            fill = self.INVALID_FILL
            border = self.INVALID_BORDER
            symbol = "×"

        elif self._hovered:
            fill = self.HOVER_FILL
            border = self.HOVER_BORDER
            symbol = ""

        else:
            fill = self.NORMAL_FILL
            border = self.NORMAL_BORDER
            symbol = ""

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

        self._status_item.setText(
            symbol
        )

        # Hide the purpose icon while compatibility feedback is shown.
        self._icon_item.setVisible(
            symbol == ""
        )

        self._status_item.setVisible(
            symbol != ""
        )

        self._position_status()

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

        self._connection_drag_started(
            self.port_id,
            event.scenePos(),
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