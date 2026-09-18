"""Public routing interface for visual connections."""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF

from .connection_routing_endpoint import (
    build_endpoint_escape,
    build_endpoint_stub,
)
from .connection_routing_pathfinder import (
    build_route as build_pathfinder_route,
)
from .connection_routing_pathfinder import (
    has_immediate_uturn,
    route_is_clear,
    segment_blocked,
    simplify_route,
)


class ConnectionRoutingEngine:
    """Coordinate endpoint escape and orthogonal pathfinding."""

    ROUTING_MARGIN = 16.0
    STUB_LENGTH = 40.0
    BEND_PENALTY = 80.0
    ENDPOINT_DIRECTION_PENALTY = 160.0
    U_TURN_MIN_SEPARATION = 32.0
    ESCAPE_CLEARANCE = 1.0

    @classmethod
    def build_endpoint_stub(
        cls,
        port_position: QPointF,
        side: str,
    ) -> tuple[QPointF, str]:
        """Return the traditional outward endpoint stub."""
        return build_endpoint_stub(
            port_position,
            side,
            cls.STUB_LENGTH,
        )

    @classmethod
    def build_endpoint_escape(
        cls,
        port_position: QPointF,
        side: str,
        obstacles: list[QRectF],
        ignored_obstacles: list[QRectF] | None = None,
    ) -> tuple[list[QPointF], str]:
        """Build an obstacle-aware route out of an endpoint port."""
        return build_endpoint_escape(
            port_position=port_position,
            side=side,
            obstacles=obstacles,
            stub_length=cls.STUB_LENGTH,
            escape_clearance=cls.ESCAPE_CLEARANCE,
            ignored_obstacles=ignored_obstacles or [],
        )

    @classmethod
    def build_route(
        cls,
        start: QPointF,
        end: QPointF,
        start_direction: str,
        end_direction: str,
        obstacles: list[QRectF],
    ) -> list[QPointF]:
        """Build the preferred route, then fall back to pathfinding."""
        if start == end:
            return [start]

        preferred = cls._build_preferred_route(
            start,
            end,
            start_direction,
            end_direction,
        )

        if (
            cls.route_is_clear(
                preferred,
                obstacles,
            )
            and not cls._has_immediate_uturn(
                preferred,
            )
        ):
            return cls._simplify_route(
                preferred,
            )

        return build_pathfinder_route(
            start=start,
            end=end,
            start_direction=start_direction,
            end_direction=end_direction,
            obstacles=obstacles,
            bend_penalty=cls.BEND_PENALTY,
            endpoint_direction_penalty=(
                cls.ENDPOINT_DIRECTION_PENALTY
            ),
            u_turn_min_separation=(
                cls.U_TURN_MIN_SEPARATION
            ),
        )

    @staticmethod
    def route_is_clear(
        route: list[QPointF],
        obstacles: list[QRectF],
    ) -> bool:
        return route_is_clear(
            route,
            obstacles,
        )

    @classmethod
    def _build_preferred_route(
        cls,
        start: QPointF,
        end: QPointF,
        start_direction: str,
        end_direction: str,
    ) -> list[QPointF]:
        """Choose between the two simple orthogonal L-shaped routes."""
        candidates = [
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

        candidates = [
            cls._remove_duplicate_points(
                route,
            )
            for route in candidates
        ]

        def score(
            route: list[QPointF],
        ) -> float:
            directions = [
                cls._segment_direction(
                    route[index],
                    route[index + 1],
                )
                for index in range(
                    len(route) - 1,
                )
            ]

            bends = sum(
                directions[index]
                != directions[index - 1]
                for index in range(
                    1,
                    len(directions),
                )
            )

            result = cls._route_length(
                route,
            )

            result += bends * cls.BEND_PENALTY

            if directions:
                if not cls._direction_matches(
                    directions[0],
                    start_direction,
                ):
                    result += (
                        cls.ENDPOINT_DIRECTION_PENALTY
                    )

                if not cls._direction_matches(
                    directions[-1],
                    end_direction,
                ):
                    result += (
                        cls.ENDPOINT_DIRECTION_PENALTY
                    )

            if cls._has_immediate_uturn(
                route,
            ):
                result += 10_000.0

            return result

        return min(
            candidates,
            key=score,
        )

    @staticmethod
    def _remove_duplicate_points(
        route: list[QPointF],
    ) -> list[QPointF]:
        result = [
            route[0],
        ]

        for point in route[1:]:
            if point != result[-1]:
                result.append(point)

        return result

    @staticmethod
    def _route_length(
        route: list[QPointF],
    ) -> float:
        return sum(
            abs(
                route[index + 1].x()
                - route[index].x()
            )
            + abs(
                route[index + 1].y()
                - route[index].y()
            )
            for index in range(
                len(route) - 1,
            )
        )

    @staticmethod
    def _segment_direction(
        start: QPointF,
        end: QPointF,
    ) -> str:
        delta_x = end.x() - start.x()
        delta_y = end.y() - start.y()

        if abs(delta_x) >= 0.001:
            return (
                "right"
                if delta_x > 0
                else "left"
            )

        if abs(delta_y) >= 0.001:
            return (
                "down"
                if delta_y > 0
                else "up"
            )

        return "none"

    @staticmethod
    def _direction_matches(
        actual: str,
        preferred: str,
    ) -> bool:
        preferred = preferred.lower().strip()

        if preferred in {
            "",
            "none",
        }:
            return True

        if preferred == "horizontal":
            return actual in {
                "left",
                "right",
            }

        if preferred == "vertical":
            return actual in {
                "up",
                "down",
            }

        return actual == preferred

    @classmethod
    def _simplify_route(
        cls,
        route: list[QPointF],
    ) -> list[QPointF]:
        return simplify_route(
            route,
        )

    @classmethod
    def _has_immediate_uturn(
        cls,
        route: list[QPointF],
    ) -> bool:
        return has_immediate_uturn(
            route,
        )

    @staticmethod
    def _opposite_direction(
        direction: str,
    ) -> str:
        return {
            "left": "right",
            "right": "left",
            "up": "down",
            "down": "up",
        }.get(
            direction,
            "none",
        )

    @staticmethod
    def _normalize_side(
        side: str,
    ) -> str:
        normalized = side.lower().strip()

        if normalized in {
            "left",
            "right",
            "top",
            "bottom",
        }:
            return normalized

        return "none"

    @staticmethod
    def _distance(
        start: QPointF,
        end: QPointF,
    ) -> float:
        return (
            abs(start.x() - end.x())
            + abs(start.y() - end.y())
        )

    @staticmethod
    def _point_blocked(
        point: QPointF,
        obstacles: list[QRectF],
    ) -> bool:
        return any(
            rect.left() < point.x() < rect.right()
            and rect.top() < point.y() < rect.bottom()
            for rect in obstacles
        )

    @staticmethod
    def _segment_blocked(
        start: QPointF,
        end: QPointF,
        obstacles: list[QRectF],
    ) -> bool:
        return segment_blocked(
            start,
            end,
            obstacles,
        )