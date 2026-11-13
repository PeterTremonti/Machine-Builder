"""Pure geometry helpers for shared conductor-harness routing."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence

from PySide6.QtCore import QPointF


def centered_lane_offsets(
    member_count: int,
    lane_spacing: float,
) -> tuple[float, ...]:
    """Return evenly spaced offsets centered around a bundle's route spine."""
    if isinstance(member_count, bool) or not isinstance(member_count, int):
        raise ValueError("member_count must be a positive integer")
    if member_count < 1:
        raise ValueError("member_count must be a positive integer")
    if not math.isfinite(lane_spacing) or lane_spacing <= 0.0:
        raise ValueError("lane_spacing must be finite and positive")

    midpoint = (member_count - 1) / 2.0
    return tuple(
        (index - midpoint) * lane_spacing
        for index in range(member_count)
    )


def bundle_envelope_half_width(
    member_count: int,
    lane_spacing: float,
    conductor_radius: float = 1.0,
    extra_clearance: float = 0.0,
) -> float:
    """Return the clearance radius needed around the shared route spine."""
    if not math.isfinite(conductor_radius) or conductor_radius < 0.0:
        raise ValueError("conductor_radius must be finite and nonnegative")
    if not math.isfinite(extra_clearance) or extra_clearance < 0.0:
        raise ValueError("extra_clearance must be finite and nonnegative")

    offsets = centered_lane_offsets(member_count, lane_spacing)
    return max(abs(offset) for offset in offsets) + conductor_radius + extra_clearance


def offset_orthogonal_route(
    route: Sequence[QPointF],
    offset: float,
    *,
    epsilon: float = 1e-6,
) -> list[QPointF] | None:
    """Create a parallel offset of an orthogonal route with mitered corners.

    Positive offsets use the normal (-dy, dx) in scene coordinates.
    Invalid, diagonal, reversing, or degenerate geometry is rejected.
    """
    if not math.isfinite(offset):
        raise ValueError("offset must be finite")
    if not math.isfinite(epsilon) or epsilon <= 0.0:
        raise ValueError("epsilon must be finite and positive")

    points: list[QPointF] = []
    for source in route:
        point = QPointF(float(source.x()), float(source.y()))
        if not math.isfinite(point.x()) or not math.isfinite(point.y()):
            return None

        if points:
            previous = points[-1]
            if (
                abs(point.x() - previous.x()) <= epsilon
                and abs(point.y() - previous.y()) <= epsilon
            ):
                continue

        if len(points) >= 2:
            first = points[-2]
            middle = points[-1]
            first_dx = middle.x() - first.x()
            first_dy = middle.y() - first.y()
            next_dx = point.x() - middle.x()
            next_dy = point.y() - middle.y()

            same_horizontal_direction = (
                abs(first_dy) <= epsilon
                and abs(next_dy) <= epsilon
                and first_dx * next_dx > 0.0
            )
            same_vertical_direction = (
                abs(first_dx) <= epsilon
                and abs(next_dx) <= epsilon
                and first_dy * next_dy > 0.0
            )
            if same_horizontal_direction or same_vertical_direction:
                points[-1] = point
                continue

        points.append(point)

    if len(points) < 2:
        return None

    directions: list[tuple[float, float]] = []
    normals: list[tuple[float, float]] = []

    for first, second in zip(points, points[1:]):
        dx = second.x() - first.x()
        dy = second.y() - first.y()

        if abs(dx) <= epsilon and abs(dy) > epsilon:
            direction = (0.0, 1.0 if dy > 0.0 else -1.0)
        elif abs(dy) <= epsilon and abs(dx) > epsilon:
            direction = (1.0 if dx > 0.0 else -1.0, 0.0)
        else:
            return None

        directions.append(direction)
        normals.append((-direction[1], direction[0]))

    result = [
        QPointF(
            points[0].x() + normals[0][0] * offset,
            points[0].y() + normals[0][1] * offset,
        )
    ]

    for index, point in enumerate(points[1:-1], start=1):
        previous_direction = directions[index - 1]
        next_direction = directions[index]
        dot = (
            previous_direction[0] * next_direction[0]
            + previous_direction[1] * next_direction[1]
        )

        if dot < -epsilon:
            return None

        if abs(dot) <= epsilon:
            previous_normal = normals[index - 1]
            next_normal = normals[index]
            result.append(
                QPointF(
                    point.x()
                    + offset * (previous_normal[0] + next_normal[0]),
                    point.y()
                    + offset * (previous_normal[1] + next_normal[1]),
                )
            )
        else:
            normal = normals[index - 1]
            result.append(
                QPointF(
                    point.x() + offset * normal[0],
                    point.y() + offset * normal[1],
                )
            )

    last_normal = normals[-1]
    result.append(
        QPointF(
            points[-1].x() + last_normal[0] * offset,
            points[-1].y() + last_normal[1] * offset,
        )
    )

    # Reject offsets that consume a segment or reverse its direction at a bend.
    for index, direction in enumerate(directions):
        dx = result[index + 1].x() - result[index].x()
        dy = result[index + 1].y() - result[index].y()
        if (
            abs(dx * direction[1] - dy * direction[0]) > epsilon
            or dx * direction[0] + dy * direction[1] <= epsilon
        ):
            return None

    return result


def lane_order_is_compatible(
    start_offsets: Mapping[str, float],
    end_offsets: Mapping[str, float],
    *,
    epsilon: float = 1e-6,
) -> bool:
    """Return whether the same members keep their relative lane order.

    Each mapping associates a connection ID with its signed endpoint
    fan-out offset. Missing, non-finite, or indistinguishable lanes are
    ambiguous and therefore ineligible for shared-envelope routing.
    """
    if not math.isfinite(epsilon) or epsilon <= 0.0:
        raise ValueError("epsilon must be finite and positive")

    if len(start_offsets) < 2 or set(start_offsets) != set(end_offsets):
        return False

    if any(
        not isinstance(member_id, str) or not member_id.strip()
        for member_id in start_offsets
    ):
        return False

    def validated_offsets(
        offsets: Mapping[str, float],
    ) -> dict[str, float] | None:
        normalized: dict[str, float] = {}
        for member_id, raw_offset in offsets.items():
            if isinstance(raw_offset, bool):
                return None
            try:
                value = float(raw_offset)
            except (TypeError, ValueError):
                return None
            if not math.isfinite(value):
                return None
            normalized[member_id] = value

        ordered_values = sorted(normalized.values())
        if any(
            later - earlier <= epsilon
            for earlier, later in zip(
                ordered_values, ordered_values[1:]
            )
        ):
            return None
        return normalized

    start = validated_offsets(start_offsets)
    end = validated_offsets(end_offsets)
    if start is None or end is None:
        return False

    start_order = sorted(start, key=start.__getitem__)
    end_order = sorted(end, key=end.__getitem__)
    return start_order == end_order
