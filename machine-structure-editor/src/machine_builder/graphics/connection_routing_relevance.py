"""Local relevance detection for connection routing."""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF


ROUTING_RELEVANCE_RADIUS = 50.0


def build_orthogonal_probe_routes(
    start: QPointF,
    end: QPointF,
) -> list[list[QPointF]]:
    """Build the two simple orthogonal routes used for relevance detection."""
    horizontal_first = [
        start,
        QPointF(
            end.x(),
            start.y(),
        ),
        end,
    ]

    vertical_first = [
        start,
        QPointF(
            start.x(),
            end.y(),
        ),
        end,
    ]

    return [
        _remove_duplicate_points(
            horizontal_first,
        ),
        _remove_duplicate_points(
            vertical_first,
        ),
    ]


def collect_relevant_obstacles(
    route: list[QPointF],
    obstacles: list[QRectF],
    radius: float,
    ignored_obstacles: list[QRectF] | None = None,
) -> list[QRectF]:
    """Collect obstacles whose relevance zone touches a route."""
    ignored = ignored_obstacles or []

    relevant: list[QRectF] = []

    for obstacle in obstacles:
        if any(
            obstacle == ignored_obstacle
            for ignored_obstacle in ignored
        ):
            continue

        if polyline_intersects_relevance_zone(
            route,
            obstacle,
            radius,
        ):
            relevant.append(
                obstacle,
            )

    return relevant


def expand_relevant_obstacles(
    relevant_obstacles: list[QRectF],
    obstacles: list[QRectF],
    radius: float,
    ignored_obstacles: list[QRectF] | None = None,
) -> list[QRectF]:
    """Expand relevance through nearby chains of obstacles."""
    ignored = ignored_obstacles or []
    relevant = list(relevant_obstacles)

    changed = True

    while changed:
        changed = False

        for obstacle in obstacles:
            if any(
                obstacle == ignored_obstacle
                for ignored_obstacle in ignored
            ):
                continue

            if any(
                obstacle == existing
                for existing in relevant
            ):
                continue

            for existing in relevant:
                expanded = existing.adjusted(
                    -radius,
                    -radius,
                    radius,
                    radius,
                )

                if expanded.intersects(obstacle):
                    relevant.append(obstacle)
                    changed = True
                    break

    return relevant


def polyline_intersects_relevance_zone(
    route: list[QPointF],
    obstacle: QRectF,
    radius: float,
) -> bool:
    """Return whether a route passes within radius of an obstacle."""
    if not route:
        return False

    expanded = obstacle.adjusted(
        -radius,
        -radius,
        radius,
        radius,
    )

    if len(route) == 1:
        return expanded.contains(
            route[0],
        )

    return any(
        _segment_intersects_rect(
            route[index],
            route[index + 1],
            expanded,
        )
        for index in range(
            len(route) - 1,
        )
    )


def collect_relevant_wires(
    route: list[QPointF],
    wire_routes: list[list[QPointF]],
    radius: float,
) -> list[list[QPointF]]:
    """Collect existing wire routes near a relevance probe.

    This is intentionally separated from hard-obstacle collection. Wires
    are not obstacles simply because they are nearby; they are future route
    organization/alignment information.
    """
    return [
        wire
        for wire in wire_routes
        if _polylines_are_near(
            route,
            wire,
            radius,
        )
    ]


def dedupe_rectangles(
    rectangles: list[QRectF],
) -> list[QRectF]:
    """Return rectangles without duplicate geometry."""
    result: list[QRectF] = []

    for rectangle in rectangles:
        if not any(
            rectangle == existing
            for existing in result
        ):
            result.append(
                rectangle,
            )

    return result


def _polylines_are_near(
    first: list[QPointF],
    second: list[QPointF],
    radius: float,
) -> bool:
    if not first or not second:
        return False

    for index_a in range(
        len(first) - 1,
    ):
        first_start = first[index_a]
        first_end = first[index_a + 1]

        for index_b in range(
            len(second) - 1,
        ):
            second_start = second[index_b]
            second_end = second[index_b + 1]

            if _segments_are_near(
                first_start,
                first_end,
                second_start,
                second_end,
                radius,
            ):
                return True

    return False


def _segments_are_near(
    first_start: QPointF,
    first_end: QPointF,
    second_start: QPointF,
    second_end: QPointF,
    radius: float,
) -> bool:
    """Approximate segment proximity using endpoint-to-segment distance."""
    if (
        _point_to_segment_distance(
            first_start,
            second_start,
            second_end,
        )
        <= radius
    ):
        return True

    if (
        _point_to_segment_distance(
            first_end,
            second_start,
            second_end,
        )
        <= radius
    ):
        return True

    if (
        _point_to_segment_distance(
            second_start,
            first_start,
            first_end,
        )
        <= radius
    ):
        return True

    if (
        _point_to_segment_distance(
            second_end,
            first_start,
            first_end,
        )
        <= radius
    ):
        return True

    return False


def _point_to_segment_distance(
    point: QPointF,
    start: QPointF,
    end: QPointF,
) -> float:
    dx = end.x() - start.x()
    dy = end.y() - start.y()

    length_squared = (
        dx * dx
        + dy * dy
    )

    if length_squared <= 0.000001:
        return (
            (
                point.x()
                - start.x()
            )
            ** 2
            + (
                point.y()
                - start.y()
            )
            ** 2
        ) ** 0.5

    t = (
        (
            point.x()
            - start.x()
        )
        * dx
        + (
            point.y()
            - start.y()
        )
        * dy
    ) / length_squared

    t = max(
        0.0,
        min(
            1.0,
            t,
        ),
    )

    projection_x = (
        start.x()
        + t * dx
    )

    projection_y = (
        start.y()
        + t * dy
    )

    return (
        (
            point.x()
            - projection_x
        )
        ** 2
        + (
            point.y()
            - projection_y
        )
        ** 2
    ) ** 0.5


def _segment_intersects_rect(
    start: QPointF,
    end: QPointF,
    rect: QRectF,
) -> bool:
    """Use Liang-Barsky clipping to test segment/rectangle intersection."""
    if rect.contains(
        start
    ) or rect.contains(
        end
    ):
        return True

    dx = end.x() - start.x()
    dy = end.y() - start.y()

    if (
        abs(dx) < 0.000001
        and abs(dy) < 0.000001
    ):
        return rect.contains(
            start,
        )

    p = [
        -dx,
        dx,
        -dy,
        dy,
    ]

    q = [
        start.x()
        - rect.left(),
        rect.right()
        - start.x(),
        start.y()
        - rect.top(),
        rect.bottom()
        - start.y(),
    ]

    u1 = 0.0
    u2 = 1.0

    for pi, qi in zip(
        p,
        q,
    ):
        if abs(pi) < 0.000001:
            if qi < 0.0:
                return False

            continue

        value = qi / pi

        if pi < 0.0:
            if value > u2:
                return False

            u1 = max(
                u1,
                value,
            )
        else:
            if value < u1:
                return False

            u2 = min(
                u2,
                value,
            )

    return (
        u1
        <= u2 + 0.000001
    )


def _remove_duplicate_points(
    route: list[QPointF],
) -> list[QPointF]:
    result = [
        route[0],
    ]

    for point in route[1:]:
        if point != result[-1]:
            result.append(
                point,
            )

    return result