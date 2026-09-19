"""Public routing interface for visual connections."""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF

from . import connection_routing_endpoint as endpoint_routing
from . import connection_routing_relevance as relevance
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
    """Coordinate relevance detection, endpoint preparation, and pathfinding."""

    ROUTING_MARGIN = 16.0
    STUB_LENGTH = 40.0
    ROUTING_RELEVANCE_RADIUS = (
        relevance.ROUTING_RELEVANCE_RADIUS
    )

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
        """Return the fixed outward endpoint stub."""
        return endpoint_routing.build_endpoint_stub(
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
        """Build a fixed outward stub or an obstacle escape."""
        return endpoint_routing.build_endpoint_escape(
            port_position=port_position,
            side=side,
            obstacles=obstacles,
            stub_length=cls.STUB_LENGTH,
            escape_clearance=cls.ESCAPE_CLEARANCE,
            ignored_obstacles=ignored_obstacles or [],
        )

    @classmethod
    def collect_relevant_obstacles(
        cls,
        *,
        direct_start: QPointF,
        direct_end: QPointF,
        prepared_start: QPointF,
        prepared_end: QPointF,
        obstacles: list[QRectF],
        ignored_obstacles: list[QRectF] | None = None,
    ) -> list[QRectF]:
        """Collect obstacles from the direct and orthogonal relevance passes."""
        ignored = ignored_obstacles or []

        direct_route = [
            direct_start,
            direct_end,
        ]

        orthogonal_probe_routes = (
            relevance.build_orthogonal_probe_routes(
                direct_start,
                direct_end,
            )
        )

        # The prepared endpoint route is also relevant. This catches
        # geometry introduced by the fixed endpoint stubs.
        orthogonal_probe_routes.append(
            [
                prepared_start,
                prepared_end,
            ]
        )

        relevant: list[QRectF] = []

        relevant.extend(
            relevance.collect_relevant_obstacles(
                direct_route,
                obstacles,
                cls.ROUTING_RELEVANCE_RADIUS,
                ignored,
            )
        )

        for probe_route in orthogonal_probe_routes:
            relevant.extend(
                relevance.collect_relevant_obstacles(
                    probe_route,
                    obstacles,
                    cls.ROUTING_RELEVANCE_RADIUS,
                    ignored,
                )
            )

        return relevance.dedupe_rectangles(
            relevant,
        )

    @classmethod
    def build_route(
        cls,
        start: QPointF,
        end: QPointF,
        start_direction: str,
        end_direction: str,
        obstacles: list[QRectF],
        direct_start: QPointF | None = None,
        direct_end: QPointF | None = None,
        ignored_obstacles: list[QRectF] | None = None,
    ) -> list[QPointF] | None:
        """Find an orthogonal route using only locally relevant obstacles."""
        if start == end:
            return [start]

        if direct_start is None:
            direct_start = start

        if direct_end is None:
            direct_end = end

        relevant_obstacles = (
            cls.collect_relevant_obstacles(
                direct_start=direct_start,
                direct_end=direct_end,
                prepared_start=start,
                prepared_end=end,
                obstacles=obstacles,
                ignored_obstacles=ignored_obstacles,
            )
        )

        return build_pathfinder_route(
            start=start,
            end=end,
            start_direction=start_direction,
            end_direction=end_direction,
            obstacles=relevant_obstacles,
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

    @staticmethod
    def _simplify_route(
        route: list[QPointF],
    ) -> list[QPointF]:
        return simplify_route(
            route,
        )

    @staticmethod
    def _has_immediate_uturn(
        route: list[QPointF],
    ) -> bool:
        return has_immediate_uturn(
            route,
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