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

        # Temporary overlap-routing state. This is presentation/runtime
        # state only; it is not part of the canonical machine model.
        self._overlap_escape_state: dict[
            str,
            dict[str, Any],
        ] = {}

        self._routing_debug_mode = False
        self._stable_route: tuple[QPointF, ...] | None = None
        self._debug_start_escape: tuple[QPointF, ...] = ()
        self._debug_route: tuple[QPointF, ...] | None = None
        self._debug_end_escape: tuple[QPointF, ...] = ()

        self.OVERLAP_ESCAPE_RESELECT_DISTANCE = 24.0
        self.OVERLAP_ESCAPE_IMPROVEMENT_RATIO = 0.20
        self.OVERLAP_ESCAPE_MIN_IMPROVEMENT = 24.0
        self.ROUTE_STABILITY_COST_TOLERANCE = 16.0

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

    def set_routing_debug_mode(
        self,
        enabled: bool,
    ) -> None:
        """Enable or disable temporary routing diagnostics."""
        self._routing_debug_mode = bool(enabled)

        # Diagnostics deliberately ignore history-based escape selection.
        self._overlap_escape_state.clear()

    def debug_geometry(
        self,
    ) -> tuple[
        tuple[QPointF, ...],
        tuple[QPointF, ...] | None,
        tuple[QPointF, ...],
    ]:
        """Return the last computed routing stages for diagnostics."""
        return (
            self._debug_start_escape,
            self._debug_route,
            self._debug_end_escape,
        )

    @staticmethod
    def _route_direction(
        start: QPointF,
        end: QPointF,
    ) -> str:
        delta_x = end.x() - start.x()
        delta_y = end.y() - start.y()

        if abs(delta_x) >= 0.001:
            return "right" if delta_x > 0 else "left"

        if abs(delta_y) >= 0.001:
            return "down" if delta_y > 0 else "up"

        return "none"

    @classmethod
    def _route_cost(
        cls,
        route: tuple[QPointF, ...] | list[QPointF],
        start_direction: str,
        end_direction: str,
    ) -> float:
        if len(route) < 2:
            return 0.0

        distance = 0.0

        for index in range(len(route) - 1):
            distance += (
                abs(
                    route[index + 1].x()
                    - route[index].x()
                )
                + abs(
                    route[index + 1].y()
                    - route[index].y()
                )
            )

        cost = (
            distance
            + max(0, len(route) - 2)
            * ConnectionRoutingEngine.BEND_PENALTY
        )

        first_direction = cls._route_direction(
            route[0],
            route[1],
        )
        last_direction = cls._route_direction(
            route[-2],
            route[-1],
        )

        if (
            start_direction != "none"
            and first_direction != start_direction
        ):
            cost += (
                ConnectionRoutingEngine.ENDPOINT_DIRECTION_PENALTY
            )

        if (
            end_direction != "none"
            and last_direction != end_direction
        ):
            cost += (
                ConnectionRoutingEngine.ENDPOINT_DIRECTION_PENALTY
            )

        return cost

    def _select_stable_route(
        self,
        candidate_route: list[QPointF] | None,
        start: QPointF,
        end: QPointF,
        start_direction: str,
        end_direction: str,
        obstacles: list[Any],
    ) -> list[QPointF] | None:
        if candidate_route is None:
            self._stable_route = None
            return None

        candidate = tuple(
            QPointF(point)
            for point in candidate_route
        )

        previous = self._stable_route

        if (
            self._routing_debug_mode
            or previous is None
            or len(previous) < 2
            or previous[0] != start
            or previous[-1] != end
            or not ConnectionRoutingEngine.route_is_clear(
                list(previous),
                obstacles,
            )
        ):
            self._stable_route = candidate
            return list(candidate)

        candidate_cost = self._route_cost(
            candidate,
            start_direction,
            end_direction,
        )
        previous_cost = self._route_cost(
            previous,
            start_direction,
            end_direction,
        )

        if (
            previous_cost
            <= candidate_cost
            + self.ROUTE_STABILITY_COST_TOLERANCE
        ):
            return list(previous)

        self._stable_route = candidate
        return list(candidate)

    def setLine(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
    ) -> None:
        """Build the complete relevance-scoped visual connection."""
        start = QPointF(
            x1,
            y1,
        )

        end = QPointF(
            x2,
            y2,
        )

        obstacles = self._collect_obstacles()
        physical_obstacles = self._collect_physical_obstacles()

        start_escape, start_direction = (
            self._build_endpoint_escape(
                self.endpoint_a_id,
                start,
                obstacles,
                physical_obstacles,
            )
        )

        end_escape, end_direction = (
            self._build_endpoint_escape(
                self.endpoint_b_id,
                end,
                obstacles,
                physical_obstacles,
            )
        )

        candidate_route = ConnectionRoutingEngine.build_route(
            start=start_escape[-1],
            end=end_escape[-1],
            start_direction=start_direction,
            end_direction=end_direction,
            obstacles=obstacles,
            direct_start=start,
            direct_end=end,
        )

        route = self._select_stable_route(
            candidate_route=candidate_route,
            start=start_escape[-1],
            end=end_escape[-1],
            start_direction=start_direction,
            end_direction=end_direction,
            obstacles=obstacles,
        )

        self._debug_start_escape = tuple(
            QPointF(point)
            for point in start_escape
        )
        self._debug_route = (
            tuple(
                QPointF(point)
                for point in route
            )
            if route is not None
            else None
        )
        self._debug_end_escape = tuple(
            QPointF(point)
            for point in end_escape
        )

        path = QPainterPath(
            start,
        )

        for point in start_escape[1:]:
            path.lineTo(
                point,
            )

        if route is not None:
            for point in route[1:]:
                path.lineTo(
                    point,
                )

            for point in reversed(
                end_escape[:-1]
            ):
                path.lineTo(
                    point,
                )

            path.lineTo(
                end,
            )
        else:
            # No legal route exists between the fixed endpoint escapes.
            # Preserve the endpoint geometry without drawing a wire through
            # an obstructing component. Placement validation can flag the
            # offending geometry separately in the future.
            path.moveTo(
                end_escape[-1],
            )

            for point in reversed(
                end_escape[:-1]
            ):
                path.lineTo(
                    point,
                )

            path.lineTo(
                end,
            )

        self.setPath(
            path,
        )

    def _build_endpoint_escape(
        self,
        port_id: str,
        port_position: QPointF,
        obstacles: list[Any],
        physical_obstacles: list[Any] | None = None,
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
                endpoint_node.sceneBoundingRect()
            )

        endpoint_collision_obstacles = (
            physical_obstacles
            if physical_obstacles is not None
            else obstacles
        )

        state = self._overlap_escape_state.get(
            port_id,
        )

        if self._routing_debug_mode:
            state = None

        preferred_direction = (
            state.get("direction")
            if state is not None
            else None
        )

        previous_position = (
            state.get("position")
            if state is not None
            else None
        )

        if previous_position is None:
            allow_reselection = True
        else:
            movement = (
                (
                    port_position.x()
                    - previous_position.x()
                ) ** 2
                + (
                    port_position.y()
                    - previous_position.y()
                ) ** 2
            ) ** 0.5

            allow_reselection = (
                movement
                >= self.OVERLAP_ESCAPE_RESELECT_DISTANCE
            )

        escape = (
            ConnectionRoutingEngine.build_endpoint_escape(
                port_position=port_position,
                side=side,
                obstacles=endpoint_collision_obstacles,
                ignored_obstacles=ignored_obstacles,
                preferred_escape_direction=(
                    preferred_direction
                ),
                allow_escape_reselection=(
                    allow_reselection
                ),
                escape_hysteresis_ratio=(
                    self.OVERLAP_ESCAPE_IMPROVEMENT_RATIO
                ),
                escape_hysteresis_distance=(
                    self.OVERLAP_ESCAPE_MIN_IMPROVEMENT
                ),
            )
        )

        points = escape[0]

        if (
            self._routing_debug_mode
            or len(points) < 3
        ):
            self._overlap_escape_state.pop(
                port_id,
                None,
            )
        else:
            previous = points[-2]
            final = points[-1]

            if abs(
                final.x()
                - previous.x()
            ) >= 0.001:
                escape_direction = (
                    "right"
                    if final.x() > previous.x()
                    else "left"
                )
            elif abs(
                final.y()
                - previous.y()
            ) >= 0.001:
                escape_direction = (
                    "down"
                    if final.y() > previous.y()
                    else "up"
                )
            else:
                escape_direction = "none"

            self._overlap_escape_state[
                port_id
            ] = {
                "direction": escape_direction,
                "position": QPointF(
                    port_position,
                ),
            }

        return escape

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

    def _collect_endpoint_obstacles(self) -> list[Any]:
        """Return expanded rectangles for both endpoint nodes."""
        obstacles: list[Any] = []

        for port_id in (
            self.endpoint_a_id,
            self.endpoint_b_id,
        ):
            node = self._find_endpoint_node(
                port_id,
            )

            if node is None:
                continue

            rect = node.sceneBoundingRect().adjusted(
                -self.ROUTING_MARGIN,
                -self.ROUTING_MARGIN,
                self.ROUTING_MARGIN,
                self.ROUTING_MARGIN,
            )

            if rect.isEmpty():
                continue

            if not any(
                rect == existing
                for existing in obstacles
            ):
                obstacles.append(
                    rect,
                )

        return obstacles

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

    def _collect_physical_obstacles(self) -> list[Any]:
        """Return actual component bounds for endpoint-stub collision checks."""
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
                rect,
            )

        return obstacles

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