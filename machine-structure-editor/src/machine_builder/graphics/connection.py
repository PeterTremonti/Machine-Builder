"""Connection graphics for the Machine Structure Editor.

This module contains the Qt presentation class for visual connections.
The underlying connection data remains in visual_model.py.

Committed connections are rendered as orthogonal (horizontal/vertical)
paths that route around visual node rectangles. Each endpoint gets a
short visual stub that extends outward from its node before the main
routing path begins.

Endpoint nodes are excluded from the general obstacle list so the
connection can terminate at their ports. The outward stubs and routing
buffer help keep the path visually clear of the connected components.
"""

from __future__ import annotations

import heapq
from typing import Any

from PySide6.QtCore import QPointF, Qt, QRectF
from PySide6.QtGui import QColor, QPainterPath, QPen
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsPathItem,
    QGraphicsRectItem,
)


class ConnectionGraphicsItem(QGraphicsPathItem):
    """Rendered representation of one committed visual connection."""

    NORMAL_COLOR = QColor("#aab4c4")
    SELECTED_COLOR = QColor("#58a6ff")

    ROUTING_MARGIN = 16.0
    STUB_LENGTH = 40.0
    BEND_PENALTY = 80.0

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

    # ------------------------------------------------------------------
    # Public geometry API
    # ------------------------------------------------------------------

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

        route = self._build_orthogonal_path(
            start_stub,
            end_stub,
            start_direction,
            end_direction,
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

    # ------------------------------------------------------------------
    # Endpoint stubs
    # ------------------------------------------------------------------

    def _build_endpoint_stub(
        self,
        port_id: str,
        port_position: QPointF,
    ) -> tuple[QPointF, str]:
        """Return an outward stub endpoint and its direction."""
        port_item = self._find_port_item(
            port_id
        )

        if port_item is None:
            return (
                port_position,
                "none",
            )

        side = str(
            getattr(
                port_item,
                "_side",
                "",
            )
        ).lower().strip()

        if side == "left":
            return (
                QPointF(
                    port_position.x()
                    - self.STUB_LENGTH,
                    port_position.y(),
                ),
                "horizontal",
            )

        if side == "right":
            return (
                QPointF(
                    port_position.x()
                    + self.STUB_LENGTH,
                    port_position.y(),
                ),
                "horizontal",
            )

        if side == "top":
            return (
                QPointF(
                    port_position.x(),
                    port_position.y()
                    - self.STUB_LENGTH,
                ),
                "vertical",
            )

        if side == "bottom":
            return (
                QPointF(
                    port_position.x(),
                    port_position.y()
                    + self.STUB_LENGTH,
                ),
                "vertical",
            )

        return (
            port_position,
            "none",
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

        parent = port_item.parentItem()

        if parent is None:
            return None

        return parent

    # ------------------------------------------------------------------
    # Routing
    # ------------------------------------------------------------------

    def _build_orthogonal_path(
        self,
        start: QPointF,
        end: QPointF,
        start_direction: str,
        end_direction: str,
    ) -> list[QPointF]:
        """Build an obstacle-aware orthogonal route."""
        obstacles = self._collect_obstacles(
            start,
            end,
        )

        route = self._find_grid_route(
            start,
            end,
            obstacles,
            start_direction,
            end_direction,
        )

        if route is None:
            route = self._fallback_route(
                start,
                end,
                obstacles,
                start_direction,
                end_direction,
            )

        return self._simplify_route(
            route
        )

    def _collect_obstacles(
        self,
        start: QPointF,
        end: QPointF,
    ) -> list[QRectF]:
        """Collect expanded node rectangles that should be avoided."""
        scene = self.scene()

        if scene is None:
            return []

        obstacles: list[QRectF] = []

        start_node = self._find_endpoint_node(
            self.endpoint_a_id
        )

        end_node = self._find_endpoint_node(
            self.endpoint_b_id
        )

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

            # The nodes containing the connection endpoints are deliberately
            # excluded. The route begins/ends at their ports.
            if (
                item is start_node
                or item is end_node
            ):
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

    def _find_grid_route(
        self,
        start: QPointF,
        end: QPointF,
        obstacles: list[QRectF],
        start_direction: str,
        end_direction: str,
    ) -> list[QPointF] | None:
        """Find an orthogonal route through a visibility grid."""
        x_values = {
            start.x(),
            end.x(),
        }

        y_values = {
            start.y(),
            end.y(),
        }

        for rect in obstacles:
            x_values.add(
                rect.left()
            )
            x_values.add(
                rect.right()
            )

            y_values.add(
                rect.top()
            )
            y_values.add(
                rect.bottom()
            )

        xs = sorted(
            x_values
        )

        ys = sorted(
            y_values
        )

        points: dict[
            tuple[float, float],
            QPointF,
        ] = {}

        for x in xs:
            for y in ys:
                point = QPointF(
                    x,
                    y,
                )

                if self._point_blocked(
                    point,
                    obstacles,
                ):
                    continue

                key = (
                    round(x, 4),
                    round(y, 4),
                )

                points[key] = point

        start_key = (
            round(start.x(), 4),
            round(start.y(), 4),
        )

        end_key = (
            round(end.x(), 4),
            round(end.y(), 4),
        )

        points[start_key] = start
        points[end_key] = end

        horizontal_groups: dict[
            float,
            list[tuple[float, tuple[float, float]]],
        ] = {}

        vertical_groups: dict[
            float,
            list[tuple[float, tuple[float, float]]],
        ] = {}

        for key in points:
            x, y = key

            horizontal_groups.setdefault(
                y,
                [],
            ).append(
                (
                    x,
                    key,
                )
            )

            vertical_groups.setdefault(
                x,
                [],
            ).append(
                (
                    y,
                    key,
                )
            )

        adjacency: dict[
            tuple[float, float],
            list[
                tuple[
                    tuple[float, float],
                    float,
                    str,
                ]
            ],
        ] = {
            key: []
            for key in points
        }

        for group in horizontal_groups.values():
            group.sort()

            for index in range(
                len(group) - 1
            ):
                _, key_a = group[index]
                _, key_b = group[index + 1]

                point_a = points[key_a]
                point_b = points[key_b]

                if self._segment_blocked(
                    point_a,
                    point_b,
                    obstacles,
                ):
                    continue

                distance = abs(
                    point_b.x()
                    - point_a.x()
                )

                adjacency[key_a].append(
                    (
                        key_b,
                        distance,
                        "horizontal",
                    )
                )

                adjacency[key_b].append(
                    (
                        key_a,
                        distance,
                        "horizontal",
                    )
                )

        for group in vertical_groups.values():
            group.sort()

            for index in range(
                len(group) - 1
            ):
                _, key_a = group[index]
                _, key_b = group[index + 1]

                point_a = points[key_a]
                point_b = points[key_b]

                if self._segment_blocked(
                    point_a,
                    point_b,
                    obstacles,
                ):
                    continue

                distance = abs(
                    point_b.y()
                    - point_a.y()
                )

                adjacency[key_a].append(
                    (
                        key_b,
                        distance,
                        "vertical",
                    )
                )

                adjacency[key_b].append(
                    (
                        key_a,
                        distance,
                        "vertical",
                    )
                )

        start_state = (
            start_key,
            "none",
        )

        queue: list[
            tuple[
                float,
                tuple[float, float],
                str,
            ]
        ] = [
            (
                0.0,
                start_key,
                "none",
            )
        ]

        distances: dict[
            tuple[
                tuple[float, float],
                str,
            ],
            float,
        ] = {
            start_state: 0.0
        }

        previous: dict[
            tuple[
                tuple[float, float],
                str,
            ],
            tuple[
                tuple[float, float],
                str,
            ]
            | None,
        ] = {
            start_state: None
        }

        final_state: (
            tuple[
                tuple[float, float],
                str,
            ]
            | None
        ) = None

        while queue:
            (
                current_cost,
                current_key,
                current_direction,
            ) = heapq.heappop(
                queue
            )

            current_state = (
                current_key,
                current_direction,
            )

            best_known = distances.get(
                current_state
            )

            if (
                best_known is None
                or current_cost > best_known + 0.001
            ):
                continue

            if current_key == end_key:
                final_state = current_state
                break

            for (
                neighbor_key,
                distance,
                direction,
            ) in adjacency.get(
                current_key,
                [],
            ):
                bend_cost = 0.0

                if (
                    current_direction != "none"
                    and current_direction != direction
                ):
                    bend_cost = self.BEND_PENALTY

                if (
                    current_key == start_key
                    and start_direction != "none"
                    and direction != start_direction
                ):
                    bend_cost += self.BEND_PENALTY * 2.0

                if (
                    neighbor_key == end_key
                    and end_direction != "none"
                    and direction != end_direction
                ):
                    bend_cost += self.BEND_PENALTY * 2.0

                new_cost = (
                    current_cost
                    + distance
                    + bend_cost
                )

                neighbor_state = (
                    neighbor_key,
                    direction,
                )

                if (
                    new_cost
                    < distances.get(
                        neighbor_state,
                        float("inf"),
                    )
                ):
                    distances[
                        neighbor_state
                    ] = new_cost

                    previous[
                        neighbor_state
                    ] = current_state

                    heapq.heappush(
                        queue,
                        (
                            new_cost,
                            neighbor_key,
                            direction,
                        ),
                    )

        if final_state is None:
            return None

        keys: list[
            tuple[float, float]
        ] = []

        state = final_state

        while state is not None:
            keys.append(
                state[0]
            )

            state = previous.get(
                state
            )

        keys.reverse()

        return [
            points[key]
            for key in keys
        ]

    @staticmethod
    def _fallback_route(
        start: QPointF,
        end: QPointF,
        obstacles: list[QRectF],
        start_direction: str,
        end_direction: str,
    ) -> list[QPointF]:
        """Return a simple orthogonal route if grid routing fails."""
        candidates: list[
            list[QPointF]
        ] = [
            [
                start,
                QPointF(
                    end.x(),
                    start.y(),
                ),
                end,
            ],
            [
                start,
                QPointF(
                    start.x(),
                    end.y(),
                ),
                end,
            ],
        ]

        if obstacles:
            top = min(
                rect.top()
                for rect in obstacles
            )

            left = min(
                rect.left()
                for rect in obstacles
            )

            candidates.extend(
                [
                    [
                        start,
                        QPointF(
                            start.x(),
                            top,
                        ),
                        QPointF(
                            end.x(),
                            top,
                        ),
                        end,
                    ],
                    [
                        start,
                        QPointF(
                            left,
                            start.y(),
                        ),
                        QPointF(
                            left,
                            end.y(),
                        ),
                        end,
                    ],
                ]
            )

        for candidate in candidates:
            if all(
                not ConnectionGraphicsItem._segment_blocked(
                    candidate[index],
                    candidate[index + 1],
                    obstacles,
                )
                for index in range(
                    len(candidate) - 1
                )
            ):
                return ConnectionGraphicsItem._simplify_route(
                    candidate
                )

        return ConnectionGraphicsItem._simplify_route(
            candidates[0]
        )

    @staticmethod
    def _point_blocked(
        point: QPointF,
        obstacles: list[QRectF],
    ) -> bool:
        """Return True if a routing point is inside an obstacle."""
        return any(
            rect.contains(point)
            for rect in obstacles
        )

    @staticmethod
    def _segment_blocked(
        start: QPointF,
        end: QPointF,
        obstacles: list[QRectF],
    ) -> bool:
        """Return True if an orthogonal segment crosses an obstacle."""
        if (
            abs(start.x() - end.x()) < 0.001
            and abs(start.y() - end.y()) < 0.001
        ):
            return False

        if (
            abs(start.y() - end.y()) < 0.001
        ):
            y = start.y()

            segment_left = min(
                start.x(),
                end.x(),
            )

            segment_right = max(
                start.x(),
                end.x(),
            )

            for rect in obstacles:
                if (
                    rect.top()
                    < y
                    < rect.bottom()
                    and segment_right > rect.left()
                    and segment_left < rect.right()
                ):
                    return True

            return False

        if (
            abs(start.x() - end.x()) < 0.001
        ):
            x = start.x()

            segment_top = min(
                start.y(),
                end.y(),
            )

            segment_bottom = max(
                start.y(),
                end.y(),
            )

            for rect in obstacles:
                if (
                    rect.left()
                    < x
                    < rect.right()
                    and segment_bottom > rect.top()
                    and segment_top < rect.bottom()
                ):
                    return True

            return False

        return True

    @staticmethod
    def _simplify_route(
        route: list[QPointF],
    ) -> list[QPointF]:
        """Remove redundant collinear intermediate points."""
        if len(route) <= 2:
            return route

        simplified = [
            route[0]
        ]

        for index in range(
            1,
            len(route) - 1,
        ):
            previous = simplified[-1]
            current = route[index]
            following = route[index + 1]

            same_x = (
                abs(
                    previous.x()
                    - current.x()
                )
                < 0.001
                and abs(
                    current.x()
                    - following.x()
                )
                < 0.001
            )

            same_y = (
                abs(
                    previous.y()
                    - current.y()
                )
                < 0.001
                and abs(
                    current.y()
                    - following.y()
                )
                < 0.001
            )

            if same_x or same_y:
                continue

            simplified.append(
                current
            )

        simplified.append(
            route[-1]
        )

        return simplified

    # ------------------------------------------------------------------
    # Selection
    # ------------------------------------------------------------------

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