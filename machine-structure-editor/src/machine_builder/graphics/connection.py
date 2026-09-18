"""Connection graphics for the Machine Structure Editor."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainterPath, QPen
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsPathItem,
    QGraphicsRectItem,
)

from .connection_routing import ConnectionRoutingEngine


class ConnectionGraphicsItem(QGraphicsPathItem):
    """Rendered representation of one committed visual connection."""

    NORMAL_COLOR = QColor(
        "#aab4c4"
    )

    SELECTED_COLOR = QColor(
        "#58a6ff"
    )

    ROUTING_MARGIN = (
        ConnectionRoutingEngine.ROUTING_MARGIN
    )

    STUB_LENGTH = (
        ConnectionRoutingEngine.STUB_LENGTH
    )

    BEND_PENALTY = (
        ConnectionRoutingEngine.BEND_PENALTY
    )

    def __init__(
        self,
        connection: Any,
        selection_callback: Any,
    ) -> None:
        super().__init__()

        self.connection_id = connection.id
        self.endpoint_a_id = connection.endpoint_a_id
        self.endpoint_b_id = connection.endpoint_b_id
        self._selection_callback = (
            selection_callback
        )

        self.setPen(
            QPen(
                self.NORMAL_COLOR,
                2.0,
            )
        )

        self.setZValue(
            -10.0
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            True,
        )

        self.setAcceptedMouseButtons(
            Qt.MouseButton.LeftButton
        )

    def setLine(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
    ) -> None:
        """Build an orthogonal route with visual endpoint stubs."""
        start = QPointF(
            x1,
            y1,
        )

        end = QPointF(
            x2,
            y2,
        )

        (
            start_stub,
            start_direction,
        ) = self._build_endpoint_stub(
            self.endpoint_a_id,
            start,
        )

        (
            end_stub,
            end_direction,
        ) = self._build_endpoint_stub(
            self.endpoint_b_id,
            end,
        )

        obstacles = self._collect_obstacles()

        route = ConnectionRoutingEngine.build_route(
            start_stub,
            end_stub,
            start_direction,
            end_direction,
            obstacles,
        )

        path = QPainterPath(
            start
        )

        if start_stub != start:
            path.lineTo(
                start_stub
            )

        for point in route:
            path.lineTo(
                point
            )

        if end_stub != end:
            path.lineTo(
                end_stub
            )

        path.lineTo(
            end
        )

        self.setPath(
            path
        )

    def _build_endpoint_stub(
        self,
        port_id: str,
        port_position: QPointF,
    ) -> tuple[QPointF, str]:
        """Return an outward endpoint stub and its direction."""
        port_item = self._find_port_item(
            port_id
        )

        if port_item is None:
            return (
                port_position,
                "none",
            )

        return (
            ConnectionRoutingEngine.build_endpoint_stub(
                port_position,
                str(
                    getattr(
                        port_item,
                        "_side",
                        "",
                    )
                ),
            )
        )

    def _find_port_item(
        self,
        port_id: str,
    ) -> QGraphicsItem | None:
        """Find the visual port item belonging to an endpoint."""
        scene = self.scene()

        if scene is None:
            return None

        for item in scene.items():
            if getattr(
                item,
                "port_id",
                None,
            ) == port_id:
                return item

        return None

    def _find_endpoint_node(
        self,
        port_id: str,
    ) -> QGraphicsItem | None:
        """Find the node graphics item containing an endpoint port."""
        port_item = self._find_port_item(
            port_id
        )

        if port_item is None:
            return None

        return port_item.parentItem()

    def _collect_obstacles(
        self,
    ) -> list[QRectF]:
        """Collect all expanded visual node rectangles as obstacles."""
        scene = self.scene()

        if scene is None:
            return []

        obstacles: list[QRectF] = []

        for item in scene.items():
            if not isinstance(
                item,
                QGraphicsRectItem,
            ):
                continue

            if item is self:
                continue

            rect = item.sceneBoundingRect()

            if rect.isEmpty():
                continue

            obstacles.append(
                rect.adjusted(
                    -self.ROUTING_MARGIN,
                    -self.ROUTING_MARGIN,
                    self.ROUTING_MARGIN,
                    self.ROUTING_MARGIN,
                )
            )

        return obstacles

    def itemChange(
        self,
        change: QGraphicsItem.GraphicsItemChange,
        value: Any,
    ) -> Any:
        """Update visual state when the connection is selected."""
        if (
            change
            == QGraphicsItem.GraphicsItemChange.ItemSelectedChange
        ):
            selected = bool(
                value
            )

            self.setPen(
                QPen(
                    self.SELECTED_COLOR
                    if selected
                    else self.NORMAL_COLOR,
                    3.0
                    if selected
                    else 2.0,
                )
            )

            self._selection_callback(
                self.connection_id,
                selected,
            )

        return super().itemChange(
            change,
            value,
        )