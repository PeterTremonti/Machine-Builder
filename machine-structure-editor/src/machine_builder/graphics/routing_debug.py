"""Temporary visual routing diagnostics."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QGraphicsItem


class RoutingDebugOverlay(QGraphicsItem):
    """Visual-only routing diagnostics."""

    PHYSICAL_FILL = QColor(
        235,
        55,
        55,
        34,
    )
    ROUTING_BOUNDARY = QColor(
        "#f2c94c"
    )

    STUB_COLOR = QColor(
        "#168a52"
    )
    ESCAPE_COLOR = QColor(
        "#00b894"
    )
    MAIN_ROUTE_COLOR = QColor(
        "#66ff33"
    )
    UNROUTABLE_COLOR = QColor(
        "#ff3030"
    )

    ROUTING_MARGIN = 16.0

    def __init__(
        self,
        canvas: Any,
    ) -> None:
        super().__init__()

        self._canvas = canvas

        # Keep diagnostics above the normal canvas graphics so the
        # routing geometry is easy to see.
        self.setZValue(
            50.0
        )

        self.setAcceptedMouseButtons(
            Qt.MouseButton.NoButton
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            False,
        )

        self.setVisible(
            False
        )

    def boundingRect(self) -> QRectF:
        return QRectF(
            -100000.0,
            -100000.0,
            200000.0,
            200000.0,
        )

    def shape(self) -> QPainterPath:
        """Make the diagnostic overlay completely transparent to hit testing."""
        return QPainterPath()

    def refresh(self) -> None:
        self.update()

    def paint(
        self,
        painter: QPainter,
        option: Any,
        widget: Any = None,
    ) -> None:
        del option, widget

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing,
            True,
        )

        self._draw_components(
            painter
        )
        self._draw_connections(
            painter
        )

    def _draw_components(
        self,
        painter: QPainter,
    ) -> None:
        painter.setPen(
            Qt.PenStyle.NoPen
        )
        painter.setBrush(
            QBrush(
                self.PHYSICAL_FILL
            )
        )

        for item in (
            self._canvas._node_items.values()
        ):
            physical = item.sceneBoundingRect()

            if physical.isEmpty():
                continue

            # Physical component bounds:
            # transparent red, no hard border.
            painter.drawRect(
                physical
            )

            # Expanded routing boundary:
            # visible amber dashed rectangle.
            routing = physical.adjusted(
                -self.ROUTING_MARGIN,
                -self.ROUTING_MARGIN,
                self.ROUTING_MARGIN,
                self.ROUTING_MARGIN,
            )

            painter.setBrush(
                Qt.BrushStyle.NoBrush
            )
            painter.setPen(
                QPen(
                    self.ROUTING_BOUNDARY,
                    1.5,
                    Qt.PenStyle.DashLine,
                )
            )
            painter.drawRect(
                routing
            )

            painter.setPen(
                Qt.PenStyle.NoPen
            )
            painter.setBrush(
                QBrush(
                    self.PHYSICAL_FILL
                )
            )

    def _draw_connections(
        self,
        painter: QPainter,
    ) -> None:
        for connection in (
            self._canvas._connection_items.values()
        ):
            start_escape, route, end_escape = (
                connection.debug_geometry()
            )

            # Fixed endpoint stub.
            self._draw_segments(
                painter,
                start_escape[:2],
                self.STUB_COLOR,
                4.0,
            )

            # Endpoint escape.
            self._draw_segments(
                painter,
                start_escape[1:],
                self.ESCAPE_COLOR,
                3.5,
            )

            # Main pathfinder route.
            if route is not None:
                self._draw_segments(
                    painter,
                    route,
                    self.MAIN_ROUTE_COLOR,
                    3.5,
                )

            # Fixed endpoint stub.
            self._draw_segments(
                painter,
                end_escape[:2],
                self.STUB_COLOR,
                4.0,
            )

            # Endpoint escape.
            self._draw_segments(
                painter,
                end_escape[1:],
                self.ESCAPE_COLOR,
                3.5,
            )

            # No legal middle route.
            if route is None:
                self._draw_unroutable_marker(
                    painter,
                    start_escape[-1],
                )
                self._draw_unroutable_marker(
                    painter,
                    end_escape[-1],
                )

    @staticmethod
    def _draw_segments(
        painter: QPainter,
        points,
        color: QColor,
        width: float,
    ) -> None:
        if len(points) < 2:
            return

        painter.setPen(
            QPen(
                color,
                width,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            )
        )

        for start, end in zip(
            points,
            points[1:],
        ):
            painter.drawLine(
                start,
                end,
            )

    @staticmethod
    def _draw_unroutable_marker(
        painter: QPainter,
        position,
    ) -> None:
        painter.setPen(
            QPen(
                QColor("#ff3030"),
                3.0,
            )
        )
        painter.setBrush(
            QBrush(
                QColor("#ff3030")
            )
        )
        painter.drawEllipse(
            position,
            6.0,
            6.0,
        )
