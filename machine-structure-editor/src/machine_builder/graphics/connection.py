"""Connection graphics for the Machine Structure Editor."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainterPath, QPen
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsPathItem,
    QGraphicsRectItem,
)

from .connection_routing import ConnectionRoutingEngine


class ConnectionGraphicsItem(QGraphicsPathItem):
    """Rendered representation of one committed visual connection."""

    NORMAL_COLOR = QColor("#aab4c4")
    SELECTED_COLOR = QColor("#58a6ff")

    ROUTING_MARGIN = ConnectionRoutingEngine.ROUTING_MARGIN
    STUB_LENGTH = ConnectionRoutingEngine.STUB_LENGTH

    def __init__(
        self,
        connection: Any,
        selection_callback: Any,
    ) -> None:
        super().__init__()

        self.connection_id = connection.id
        self.endpoint_a_id = connection.endpoint_a_id
        self.endpoint_b_id = connection.endpoint_b_id
        self._selection_callback = selection_callback

        self.setPen(
            QPen(
                self.NORMAL_COLOR,
                2.0,
            )
        )

        self.setZValue(-10.0)

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
        """Build the complete obstacle-aware visual connection."""
        start = QPointF(
            x1,
            y1,
        )

        end = QPointF(
            x2,
            y2,
        )

        obstacles = self._collect_obstacles()

        start_escape, start_direction = (
            self._build_endpoint_escape(
                self.endpoint_a_id,
                start,
                obstacles,
            )
        )

        end_escape, end_direction = (
            self._build_endpoint_escape(
                self.endpoint_b_id,
                end,
                obstacles,
            )
        )

        route = ConnectionRoutingEngine.build_route(
            start=start_escape[-1],
            end=end_escape[-1],
            start_direction=start_direction,
            end_direction=end_direction,
            obstacles=obstacles,
        )

        path = QPainterPath(
            start,
        )

        for point in start_escape[1:]:
            path.lineTo(point)

        for point in route[1:]:
            path.lineTo(point)

        for point in reversed(
            end_escape[:-1]
        ):
            path.lineTo(point)

        path.lineTo(end)

        self.setPath(
            path,
        )

    def _build_endpoint_escape(
        self,
        port_id: str,
        port_position: QPointF,
        obstacles: list[Any],
    ) -> tuple[list[QPointF], str]:
        port_item = self._find_port_item(
            port_id,
        )

        if port_item is None:
            return (
                [port_position],
                "none",
            )

        side = str(
            getattr(
                port_item,
                "_side",
                "",
            )
        )

        ignored_obstacles: list[Any] = []

        endpoint_node = self._find_endpoint_node(
            port_id,
        )

        if endpoint_node is not None:
            ignored_obstacles.append(
                endpoint_node.sceneBoundingRect().adjusted(
                    -self.ROUTING_MARGIN,
                    -self.ROUTING_MARGIN,
                    self.ROUTING_MARGIN,
                    self.ROUTING_MARGIN,
                )
            )

        return ConnectionRoutingEngine.build_endpoint_escape(
            port_position=port_position,
            side=side,
            obstacles=obstacles,
            ignored_obstacles=ignored_obstacles,
        )

    def _build_endpoint_stub(
        self,
        port_id: str,
        port_position: QPointF,
    ) -> tuple[QPointF, str]:
        """Compatibility helper retained for diagnostics/tests."""
        port_item = self._find_port_item(
            port_id,
        )

        if port_item is None:
            return (
                port_position,
                "none",
            )

        return ConnectionRoutingEngine.build_endpoint_stub(
            port_position,
            str(
                getattr(
                    port_item,
                    "_side",
                    "",
                )
            ),
        )

    def _find_port_item(
        self,
        port_id: str,
    ) -> QGraphicsItem | None:
        scene = self.scene()

        if scene is None:
            return None

        for item in scene.items():
            if (
                getattr(
                    item,
                    "port_id",
                    None,
                )
                == port_id
            ):
                return item

        return None

    def _find_endpoint_node(
        self,
        port_id: str,
    ) -> QGraphicsItem | None:
        port_item = self._find_port_item(
            port_id,
        )

        if port_item is None:
            return None

        return port_item.parentItem()

    def _collect_obstacles(self) -> list[Any]:
        scene = self.scene()

        if scene is None:
            return []

        obstacles = []

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
        if (
            change
            == QGraphicsItem.GraphicsItemChange.ItemSelectedChange
        ):
            selected = bool(value)

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