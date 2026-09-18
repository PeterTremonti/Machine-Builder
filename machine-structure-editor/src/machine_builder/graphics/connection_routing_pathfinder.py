"""Orthogonal obstacle-aware pathfinding."""

from __future__ import annotations

import heapq
from itertools import count

from PySide6.QtCore import QPointF, QRectF


def build_route(
    *,
    start: QPointF,
    end: QPointF,
    start_direction: str,
    end_direction: str,
    obstacles: list[QRectF],
    bend_penalty: float,
    endpoint_direction_penalty: float,
    u_turn_min_separation: float,
) -> list[QPointF]:
    """Find an orthogonal route through the obstacle visibility grid."""

    route = _find_grid_route(
        start=start,
        end=end,
        obstacles=obstacles,
        start_direction=start_direction,
        end_direction=end_direction,
        bend_penalty=bend_penalty,
        endpoint_direction_penalty=(
            endpoint_direction_penalty
        ),
        u_turn_min_separation=(
            u_turn_min_separation
        ),
    )

    if route is not None:
        return simplify_route(
            route,
        )

    fallback = _build_fallback_route(
        start,
        end,
        obstacles,
        u_turn_min_separation,
    )

    return simplify_route(
        fallback,
    )


def route_is_clear(
    route: list[QPointF],
    obstacles: list[QRectF],
) -> bool:
    """Return whether all route segments avoid all obstacles."""
    return all(
        not segment_blocked(
            route[index],
            route[index + 1],
            obstacles,
        )
        for index in range(
            len(route) - 1,
        )
    )


def segment_blocked(
    start: QPointF,
    end: QPointF,
    obstacles: list[QRectF],
) -> bool:
    """Return True if an orthogonal segment enters an obstacle."""
    if (
        abs(start.x() - end.x()) < 0.001
        and abs(start.y() - end.y()) < 0.001
    ):
        return False

    if abs(start.y() - end.y()) < 0.001:
        y = start.y()
        left = min(
            start.x(),
            end.x(),
        )
        right = max(
            start.x(),
            end.x(),
        )

        return any(
            rect.top() < y < rect.bottom()
            and right > rect.left()
            and left < rect.right()
            for rect in obstacles
        )

    if abs(start.x() - end.x()) < 0.001:
        x = start.x()
        top = min(
            start.y(),
            end.y(),
        )
        bottom = max(
            start.y(),
            end.y(),
        )

        return any(
            rect.left() < x < rect.right()
            and bottom > rect.top()
            and top < rect.bottom()
            for rect in obstacles
        )

    # Routing geometry must remain orthogonal.
    return True


def simplify_route(
    route: list[QPointF],
) -> list[QPointF]:
    """Remove redundant collinear points without hiding U-turns."""
    if len(route) <= 2:
        return route

    result = [
        route[0],
    ]

    for index in range(
        1,
        len(route) - 1,
    ):
        previous = result[-1]
        current = route[index]
        following = route[index + 1]

        direction_a = _segment_direction(
            previous,
            current,
        )
        direction_b = _segment_direction(
            current,
            following,
        )

        if (
            direction_a != "none"
            and direction_a == direction_b
        ):
            continue

        result.append(
            current,
        )

    result.append(
        route[-1],
    )

    return result


def has_immediate_uturn(
    route: list[QPointF],
) -> bool:
    directions = [
        _segment_direction(
            route[index],
            route[index + 1],
        )
        for index in range(
            len(route) - 1,
        )
    ]

    return any(
        directions[index] != "none"
        and directions[index + 1]
        == _opposite_direction(
            directions[index],
        )
        for index in range(
            len(directions) - 1,
        )
    )


def _find_grid_route(
    *,
    start: QPointF,
    end: QPointF,
    obstacles: list[QRectF],
    start_direction: str,
    end_direction: str,
    bend_penalty: float,
    endpoint_direction_penalty: float,
    u_turn_min_separation: float,
) -> list[QPointF] | None:
    coordinates_x = {
        start.x(),
        end.x(),
    }

    coordinates_y = {
        start.y(),
        end.y(),
    }

    for rect in obstacles:
        coordinates_x.update(
            {
                rect.left(),
                rect.right(),
                rect.left()
                - u_turn_min_separation,
                rect.right()
                + u_turn_min_separation,
            }
        )

        coordinates_y.update(
            {
                rect.top(),
                rect.bottom(),
                rect.top()
                - u_turn_min_separation,
                rect.bottom()
                + u_turn_min_separation,
            }
        )

    points: dict[
        tuple[float, float],
        QPointF,
    ] = {}

    for x in coordinates_x:
        for y in coordinates_y:
            point = QPointF(
                x,
                y,
            )

            if _point_blocked(
                point,
                obstacles,
            ):
                continue

            points[
                _key(point)
            ] = point

    start_key = _key(start)
    end_key = _key(end)

    points[start_key] = start
    points[end_key] = end

    adjacency = {
        key: []
        for key in points
    }

    _connect_horizontal(
        points,
        adjacency,
        obstacles,
    )

    _connect_vertical(
        points,
        adjacency,
        obstacles,
    )

    initial_state = (
        start_key,
        "none",
        "none",
        None,
    )

    queue: list[
        tuple[
            float,
            int,
            tuple,
        ]
    ] = []

    sequence = count()

    heapq.heappush(
        queue,
        (
            0.0,
            next(sequence),
            initial_state,
        ),
    )

    distances = {
        initial_state: 0.0,
    }

    previous: dict[
        tuple,
        tuple | None,
    ] = {
        initial_state: None,
    }

    final_state = None

    while queue:
        (
            cost,
            _sequence,
            state,
        ) = heapq.heappop(
            queue,
        )

        if (
            cost
            > distances.get(
                state,
                float("inf"),
            )
            + 0.001
        ):
            continue

        (
            current_key,
            current_direction,
            previous_direction,
            previous_key,
        ) = state

        if current_key == end_key:
            final_state = state
            break

        for (
            neighbor_key,
            distance,
            direction,
        ) in adjacency.get(
            current_key,
            [],
        ):
            if (
                current_direction != "none"
                and direction
                == _opposite_direction(
                    current_direction,
                )
            ):
                continue

            move_cost = distance

            if (
                current_direction != "none"
                and direction != current_direction
            ):
                move_cost += bend_penalty

            if (
                current_key == start_key
                and not _direction_matches(
                    direction,
                    start_direction,
                )
            ):
                move_cost += (
                    endpoint_direction_penalty
                )

            if (
                neighbor_key == end_key
                and not _direction_matches(
                    direction,
                    end_direction,
                )
            ):
                move_cost += (
                    endpoint_direction_penalty
                )

            if (
                previous_key is not None
                and previous_direction != "none"
                and direction
                == _opposite_direction(
                    previous_direction,
                )
                and current_direction != "none"
                and current_direction
                != previous_direction
            ):
                separation = _distance(
                    points[previous_key],
                    points[current_key],
                )

                if (
                    separation
                    < u_turn_min_separation
                ):
                    continue

            next_state = (
                neighbor_key,
                direction,
                current_direction,
                current_key,
            )

            new_cost = cost + move_cost

            if (
                new_cost
                < distances.get(
                    next_state,
                    float("inf"),
                )
            ):
                distances[
                    next_state
                ] = new_cost

                previous[
                    next_state
                ] = state

                heapq.heappush(
                    queue,
                    (
                        new_cost,
                        next(sequence),
                        next_state,
                    ),
                )

    if final_state is None:
        return None

    keys = []
    state = final_state

    while state is not None:
        keys.append(
            state[0],
        )
        state = previous.get(
            state,
        )

    keys.reverse()

    return [
        points[key]
        for key in keys
    ]


def _connect_horizontal(
    points: dict[
        tuple[float, float],
        QPointF,
    ],
    adjacency: dict,
    obstacles: list[QRectF],
) -> None:
    groups: dict[
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
        groups.setdefault(
            y,
            [],
        ).append(
            (
                x,
                key,
            )
        )

    for group in groups.values():
        group.sort()

        for index in range(
            len(group) - 1,
        ):
            key_a = group[index][1]
            key_b = group[index + 1][1]

            point_a = points[key_a]
            point_b = points[key_b]

            if segment_blocked(
                point_a,
                point_b,
                obstacles,
            ):
                continue

            direction = _segment_direction(
                point_a,
                point_b,
            )

            distance = abs(
                point_b.x()
                - point_a.x()
            )

            adjacency[key_a].append(
                (
                    key_b,
                    distance,
                    direction,
                )
            )

            adjacency[key_b].append(
                (
                    key_a,
                    distance,
                    _opposite_direction(
                        direction,
                    ),
                )
            )


def _connect_vertical(
    points: dict[
        tuple[float, float],
        QPointF,
    ],
    adjacency: dict,
    obstacles: list[QRectF],
) -> None:
    groups: dict[
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
        groups.setdefault(
            x,
            [],
        ).append(
            (
                y,
                key,
            )
        )

    for group in groups.values():
        group.sort()

        for index in range(
            len(group) - 1,
        ):
            key_a = group[index][1]
            key_b = group[index + 1][1]

            point_a = points[key_a]
            point_b = points[key_b]

            if segment_blocked(
                point_a,
                point_b,
                obstacles,
            ):
                continue

            direction = _segment_direction(
                point_a,
                point_b,
            )

            distance = abs(
                point_b.y()
                - point_a.y()
            )

            adjacency[key_a].append(
                (
                    key_b,
                    distance,
                    direction,
                )
            )

            adjacency[key_b].append(
                (
                    key_a,
                    distance,
                    _opposite_direction(
                        direction,
                    ),
                )
            )


def _build_fallback_route(
    start: QPointF,
    end: QPointF,
    obstacles: list[QRectF],
    separation: float,
) -> list[QPointF]:
    if not obstacles:
        return [
            start,
            QPointF(
                end.x(),
                start.y(),
            ),
            end,
        ]

    top = min(
        rect.top()
        for rect in obstacles
    ) - separation

    bottom = max(
        rect.bottom()
        for rect in obstacles
    ) + separation

    left = min(
        rect.left()
        for rect in obstacles
    ) - separation

    right = max(
        rect.right()
        for rect in obstacles
    ) + separation

    candidates = [
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
                start.x(),
                bottom,
            ),
            QPointF(
                end.x(),
                bottom,
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
        [
            start,
            QPointF(
                right,
                start.y(),
            ),
            QPointF(
                right,
                end.y(),
            ),
            end,
        ],
    ]

    valid = [
        candidate
        for candidate in candidates
        if route_is_clear(
            candidate,
            obstacles,
        )
    ]

    if valid:
        return min(
            valid,
            key=_route_length,
        )

    return candidates[0]


def _route_length(
    route: list[QPointF],
) -> float:
    return sum(
        _distance(
            route[index],
            route[index + 1],
        )
        for index in range(
            len(route) - 1,
        )
    )


def _point_blocked(
    point: QPointF,
    obstacles: list[QRectF],
) -> bool:
    return any(
        rect.left() < point.x() < rect.right()
        and rect.top() < point.y() < rect.bottom()
        for rect in obstacles
    )


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


def _distance(
    start: QPointF,
    end: QPointF,
) -> float:
    return (
        abs(start.x() - end.x())
        + abs(start.y() - end.y())
    )


def _key(
    point: QPointF,
) -> tuple[float, float]:
    return (
        round(point.x(), 4),
        round(point.y(), 4),
    )