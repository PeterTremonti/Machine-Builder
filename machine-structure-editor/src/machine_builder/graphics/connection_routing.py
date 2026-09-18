"""Pure geometry and pathfinding for visual connection routing."""

from __future__ import annotations

import heapq

from PySide6.QtCore import QPointF, QRectF


class ConnectionRoutingEngine:
    """Build orthogonal connection routes around rectangular obstacles."""

    ROUTING_MARGIN = 16.0
    STUB_LENGTH = 40.0
    BEND_PENALTY = 80.0

    @classmethod
    def build_endpoint_stub(
        cls,
        port_position: QPointF,
        side: str,
    ) -> tuple[QPointF, str]:
        """Return the outward endpoint-stub point and route direction."""
        normalized_side = side.lower().strip()

        if normalized_side == "left":
            return (
                QPointF(
                    port_position.x()
                    - cls.STUB_LENGTH,
                    port_position.y(),
                ),
                "horizontal",
            )

        if normalized_side == "right":
            return (
                QPointF(
                    port_position.x()
                    + cls.STUB_LENGTH,
                    port_position.y(),
                ),
                "horizontal",
            )

        if normalized_side == "top":
            return (
                QPointF(
                    port_position.x(),
                    port_position.y()
                    - cls.STUB_LENGTH,
                ),
                "vertical",
            )

        if normalized_side == "bottom":
            return (
                QPointF(
                    port_position.x(),
                    port_position.y()
                    + cls.STUB_LENGTH,
                ),
                "vertical",
            )

        return (
            port_position,
            "none",
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
        """Build a preferred route, rerouting when obstacles block it."""
        preferred = cls._build_preferred_route(
            start,
            end,
            start_direction,
            end_direction,
        )

        if (
            preferred is not None
            and cls.route_is_clear(
                preferred,
                obstacles,
            )
        ):
            return cls._simplify_route(
                preferred
            )

        route = cls._find_grid_route(
            start,
            end,
            obstacles,
            start_direction,
            end_direction,
        )

        if route is not None:
            return cls._simplify_route(
                route
            )

        fallback = cls._fallback_route(
            start,
            end,
            obstacles,
        )

        return cls._simplify_route(
            fallback
        )

    @staticmethod
    def route_is_clear(
        route: list[QPointF],
        obstacles: list[QRectF],
    ) -> bool:
        """Return whether every route segment avoids every obstacle."""
        return all(
            not ConnectionRoutingEngine._segment_blocked(
                route[index],
                route[index + 1],
                obstacles,
            )
            for index in range(
                len(route) - 1
            )
        )

    @classmethod
    def _build_preferred_route(
        cls,
        start: QPointF,
        end: QPointF,
        start_direction: str,
        end_direction: str,
    ) -> list[QPointF] | None:
        """Return the simplest orthogonal candidate geometry."""
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

        valid_candidates = [
            candidate
            for candidate in candidates
            if cls._route_points_valid(
                candidate
            )
        ]

        if not valid_candidates:
            return None

        def score(
            candidate: list[QPointF],
        ) -> float:
            distance = cls._route_length(
                candidate
            )

            bends = max(
                len(candidate) - 2,
                0,
            )

            result = (
                distance
                + bends * cls.BEND_PENALTY
            )

            first_direction = (
                cls._segment_direction(
                    candidate[0],
                    candidate[1],
                )
            )

            last_direction = (
                cls._segment_direction(
                    candidate[-2],
                    candidate[-1],
                )
            )

            if (
                start_direction != "none"
                and first_direction
                != start_direction
            ):
                result += (
                    cls.BEND_PENALTY * 2.0
                )

            if (
                end_direction != "none"
                and last_direction
                != end_direction
            ):
                result += (
                    cls.BEND_PENALTY * 2.0
                )

            return result

        return min(
            valid_candidates,
            key=score,
        )

    @staticmethod
    def _route_points_valid(
        route: list[QPointF],
    ) -> bool:
        for index in range(
            len(route) - 1
        ):
            start = route[index]
            end = route[index + 1]

            if (
                abs(
                    start.x()
                    - end.x()
                )
                >= 0.001
                and abs(
                    start.y()
                    - end.y()
                )
                >= 0.001
            ):
                return False

        return True

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
                len(route) - 1
            )
        )

    @staticmethod
    def _segment_direction(
        start: QPointF,
        end: QPointF,
    ) -> str:
        if (
            abs(
                start.x()
                - end.x()
            )
            >= 0.001
        ):
            return "horizontal"

        if (
            abs(
                start.y()
                - end.y()
            )
            >= 0.001
        ):
            return "vertical"

        return "none"

    @classmethod
    def _find_grid_route(
        cls,
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

                if cls._point_blocked(
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
            round(
                start.x(),
                4,
            ),
            round(
                start.y(),
                4,
            ),
        )

        end_key = (
            round(
                end.x(),
                4,
            ),
            round(
                end.y(),
                4,
            ),
        )

        points[start_key] = start
        points[end_key] = end

        horizontal_groups: dict[
            float,
            list[
                tuple[
                    float,
                    tuple[float, float],
                ]
            ],
        ] = {}

        vertical_groups: dict[
            float,
            list[
                tuple[
                    float,
                    tuple[float, float],
                ]
            ],
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

                if cls._segment_blocked(
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

                if cls._segment_blocked(
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
                or current_cost
                > best_known + 0.001
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
                    and current_direction
                    != direction
                ):
                    bend_cost = (
                        cls.BEND_PENALTY
                    )

                if (
                    current_key == start_key
                    and start_direction != "none"
                    and direction
                    != start_direction
                ):
                    bend_cost += (
                        cls.BEND_PENALTY
                        * 2.0
                    )

                if (
                    neighbor_key == end_key
                    and end_direction != "none"
                    and direction
                    != end_direction
                ):
                    bend_cost += (
                        cls.BEND_PENALTY
                        * 2.0
                    )

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

    @classmethod
    def _fallback_route(
        cls,
        start: QPointF,
        end: QPointF,
        obstacles: list[QRectF],
    ) -> list[QPointF]:
        """Return a simple orthogonal route if grid search fails."""
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
            if cls.route_is_clear(
                candidate,
                obstacles,
            ):
                return candidate

        return candidates[0]

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
            abs(
                start.x()
                - end.x()
            )
            < 0.001
            and abs(
                start.y()
                - end.y()
            )
            < 0.001
        ):
            return False

        if (
            abs(
                start.y()
                - end.y()
            )
            < 0.001
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
                    and segment_right
                    > rect.left()
                    and segment_left
                    < rect.right()
                ):
                    return True

            return False

        if (
            abs(
                start.x()
                - end.x()
            )
            < 0.001
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
                    and segment_bottom
                    > rect.top()
                    and segment_top
                    < rect.bottom()
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