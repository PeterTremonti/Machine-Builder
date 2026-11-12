"""Build a bounded, runtime-only four-connection presentation route graph.

This module derives visual merge/trunk/split topology over four existing
connections. It does not create electrical junctions, physical cables,
Harness membership, or canonical machine entities.

The caller supplies individual endpoint geometry, explicit two-member
presentation groups, obstacles, and a route callback. The callback is
expected to use the application's obstacle-aware routing engine.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
import math

from .presentation_route_graph import (
    Point2D,
    PresentationConnectionRoute,
    PresentationRouteGraph,
    PresentationRouteNode,
    PresentationRouteSegment,
)


_EPSILON = 1e-6
RouteSegment = tuple[Point2D, Point2D]
ProtectedSegments = tuple[RouteSegment, ...]
RouteFunction = Callable[
    [
        Point2D,
        Point2D,
        str,
        str,
        Sequence[object],
        ProtectedSegments,
    ],
    Sequence[Point2D] | None,
]


def _identifier(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonblank string")
    return value


def _point(value: object, field_name: str) -> Point2D:
    if isinstance(value, (str, bytes)):
        raise ValueError(f"{field_name} must be a two-coordinate point")

    try:
        coordinates = tuple(value)
    except TypeError as exc:
        raise ValueError(
            f"{field_name} must be a two-coordinate point"
        ) from exc

    if len(coordinates) != 2:
        raise ValueError(f"{field_name} must contain exactly two coordinates")

    result: list[float] = []
    for coordinate in coordinates:
        if isinstance(coordinate, bool):
            raise ValueError(f"{field_name} coordinates must be finite")
        try:
            number = float(coordinate)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(
                f"{field_name} coordinates must be finite"
            ) from exc
        if not math.isfinite(number):
            raise ValueError(f"{field_name} coordinates must be finite")
        result.append(number)

    return (result[0], result[1])


def _points(
    values: object,
    field_name: str,
    *,
    minimum: int = 1,
) -> tuple[Point2D, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{field_name} must be a collection of points")
    try:
        raw = tuple(values)
    except TypeError as exc:
        raise ValueError(
            f"{field_name} must be a collection of points"
        ) from exc

    if len(raw) < minimum:
        raise ValueError(
            f"{field_name} must contain at least {minimum} point(s)"
        )

    return tuple(
        _point(value, f"{field_name}[{index}]")
        for index, value in enumerate(raw)
    )


def _same(first: Point2D, second: Point2D) -> bool:
    return (
        abs(first[0] - second[0]) <= _EPSILON
        and abs(first[1] - second[1]) <= _EPSILON
    )


def _clean_path(values: Sequence[Point2D]) -> tuple[Point2D, ...]:
    result: list[Point2D] = []
    for value in values:
        if not result or not _same(result[-1], value):
            result.append(value)
    return tuple(result)


def _centroid(points: Sequence[Point2D]) -> Point2D:
    if not points:
        raise ValueError("cannot calculate the centroid of no points")
    count = float(len(points))
    return (
        sum(point[0] for point in points) / count,
        sum(point[1] for point in points) / count,
    )


def _perpendicular_departure_direction(
    direction: Point2D,
    origin: Point2D,
    target: Point2D,
) -> str | None:
    """Choose the perpendicular departure side toward a target."""
    normal = (-direction[1], direction[0])
    dx = target[0] - origin[0]
    dy = target[1] - origin[1]
    projection = dx * normal[0] + dy * normal[1]

    if abs(projection) <= _EPSILON:
        return None

    if abs(normal[0]) >= abs(normal[1]):
        return "right" if projection * normal[0] > 0.0 else "left"

    return "down" if projection * normal[1] > 0.0 else "up"

def _is_orthogonal(path: Sequence[Point2D]) -> bool:
    return all(
        abs(first[0] - second[0]) <= _EPSILON
        or abs(first[1] - second[1]) <= _EPSILON
        for first, second in zip(path, path[1:])
    )


@dataclass(frozen=True, slots=True)
class PresentationEndpointGeometry:
    """Prepared endpoint data from one existing ConnectionGraphicsItem.

    Escape point sequences start at their respective route positions and
    proceed outward from the original visual endpoint. Canonical and visual
    endpoint IDs remain separate and unchanged.
    """

    connection_id: str
    canonical_endpoint_a_id: str
    canonical_endpoint_b_id: str
    visual_endpoint_a_id: str
    visual_endpoint_b_id: str
    start_position: Point2D
    start_route_position: Point2D
    start_escape_points: tuple[Point2D, ...]
    start_direction: str
    end_position: Point2D
    end_route_position: Point2D
    end_escape_points: tuple[Point2D, ...]
    end_direction: str

    def __post_init__(self) -> None:
        for field_name in (
            "connection_id",
            "canonical_endpoint_a_id",
            "canonical_endpoint_b_id",
            "visual_endpoint_a_id",
            "visual_endpoint_b_id",
            "start_direction",
            "end_direction",
        ):
            object.__setattr__(
                self,
                field_name,
                _identifier(getattr(self, field_name), field_name),
            )

        for field_name in (
            "start_position",
            "start_route_position",
            "end_position",
            "end_route_position",
        ):
            object.__setattr__(
                self,
                field_name,
                _point(getattr(self, field_name), field_name),
            )

        for field_name in ("start_escape_points", "end_escape_points"):
            object.__setattr__(
                self,
                field_name,
                _points(getattr(self, field_name), field_name),
            )

        if not _same(
            self.start_escape_points[0],
            self.start_route_position,
        ):
            raise ValueError(
                "start escape geometry must begin at start_route_position"
            )

        if not _same(
            self.end_escape_points[0],
            self.end_route_position,
        ):
            raise ValueError(
                "end escape geometry must begin at end_route_position"
            )


def _trim_polyline_for_junction(
    points: Sequence[Point2D],
    start_distance: float,
    end_distance: float,
) -> tuple[Point2D, ...] | None:
    """Trim a small zone from intentional junction endpoints."""
    lengths = tuple(
        math.hypot(second[0] - first[0], second[1] - first[1])
        for first, second in zip(points, points[1:])
    )
    total = sum(lengths)

    if total <= start_distance + end_distance + _EPSILON:
        return None

    def point_at(distance: float) -> Point2D:
        walked = 0.0
        for first, second, length in zip(points, points[1:], lengths):
            if length <= _EPSILON:
                continue
            if walked + length >= distance - _EPSILON:
                ratio = max(0.0, min(1.0, (distance - walked) / length))
                return (
                    first[0] + (second[0] - first[0]) * ratio,
                    first[1] + (second[1] - first[1]) * ratio,
                )
            walked += length
        return points[-1]

    lower = start_distance
    upper = total - end_distance
    result = [point_at(lower)]
    walked = 0.0

    for point, length in zip(points[1:-1], lengths):
        walked += length
        if lower + _EPSILON < walked < upper - _EPSILON:
            result.append(point)

    result.append(point_at(upper))
    cleaned = _clean_path(result)
    return cleaned if len(cleaned) >= 2 else None

def _protected_segments(
    existing: Sequence[PresentationRouteSegment],
    start_node_id: str,
    end_node_id: str,
) -> ProtectedSegments:
    """Protect existing routes while leaving a short intentional junction zone."""
    junction_clearance = 9.0
    protected: list[RouteSegment] = []

    for segment in existing:
        trim_start = (
            junction_clearance
            if segment.start_node_id in {start_node_id, end_node_id}
            else 0.0
        )
        trim_end = (
            junction_clearance
            if segment.end_node_id in {start_node_id, end_node_id}
            else 0.0
        )
        points = _trim_polyline_for_junction(
            segment.points,
            trim_start,
            trim_end,
        )
        if points is None:
            continue

        protected.extend(
            (first, second)
            for first, second in zip(points, points[1:])
            if not _same(first, second)
        )

    return tuple(protected)


def _request_route(
    *,
    start: Point2D,
    end: Point2D,
    start_direction: str,
    end_direction: str,
    obstacles: Sequence[object],
    existing_segments: Sequence[PresentationRouteSegment],
    start_node_id: str,
    end_node_id: str,
    route_between: RouteFunction,
    allow_same_point: bool,
) -> tuple[Point2D, ...] | None:
    if _same(start, end):
        return (start,) if allow_same_point else None

    protected = _protected_segments(
        existing_segments,
        start_node_id,
        end_node_id,
    )

    raw = route_between(
        start,
        end,
        start_direction,
        end_direction,
        obstacles,
        protected,
    )
    if raw is None:
        return None

    normalized = _points(raw, "routed path", minimum=2)
    cleaned = _clean_path(normalized)

    if len(cleaned) < 2:
        return None
    if not _same(cleaned[0], start) or not _same(cleaned[-1], end):
        return None
    if not _is_orthogonal(cleaned):
        return None

    return cleaned


def _intersect_edges(
    first_start: Point2D,
    first_end: Point2D,
    second_start: Point2D,
    second_end: Point2D,
) -> tuple[str, Point2D | None]:
    """Return ('none', None), ('point', point), or ('overlap', None)."""
    first_horizontal = abs(first_start[1] - first_end[1]) <= _EPSILON
    second_horizontal = abs(second_start[1] - second_end[1]) <= _EPSILON
    first_vertical = abs(first_start[0] - first_end[0]) <= _EPSILON
    second_vertical = abs(second_start[0] - second_end[0]) <= _EPSILON

    if first_horizontal and second_horizontal:
        if abs(first_start[1] - second_start[1]) > _EPSILON:
            return ("none", None)
        low = max(
            min(first_start[0], first_end[0]),
            min(second_start[0], second_end[0]),
        )
        high = min(
            max(first_start[0], first_end[0]),
            max(second_start[0], second_end[0]),
        )
        if high < low - _EPSILON:
            return ("none", None)
        if high - low > _EPSILON:
            return ("overlap", None)
        return (
            "point",
            ((low + high) / 2.0, (first_start[1] + second_start[1]) / 2.0),
        )

    if first_vertical and second_vertical:
        if abs(first_start[0] - second_start[0]) > _EPSILON:
            return ("none", None)
        low = max(
            min(first_start[1], first_end[1]),
            min(second_start[1], second_end[1]),
        )
        high = min(
            max(first_start[1], first_end[1]),
            max(second_start[1], second_end[1]),
        )
        if high < low - _EPSILON:
            return ("none", None)
        if high - low > _EPSILON:
            return ("overlap", None)
        return (
            "point",
            ((first_start[0] + second_start[0]) / 2.0, (low + high) / 2.0),
        )

    if first_horizontal and second_vertical:
        point = (second_start[0], first_start[1])
        horizontal_low = min(first_start[0], first_end[0])
        horizontal_high = max(first_start[0], first_end[0])
        vertical_low = min(second_start[1], second_end[1])
        vertical_high = max(second_start[1], second_end[1])
    elif first_vertical and second_horizontal:
        point = (first_start[0], second_start[1])
        horizontal_low = min(second_start[0], second_end[0])
        horizontal_high = max(second_start[0], second_end[0])
        vertical_low = min(first_start[1], first_end[1])
        vertical_high = max(first_start[1], first_end[1])
    else:
        return ("none", None)

    if (
        horizontal_low - _EPSILON <= point[0] <= horizontal_high + _EPSILON
        and vertical_low - _EPSILON <= point[1] <= vertical_high + _EPSILON
    ):
        return ("point", point)

    return ("none", None)


def _segments_have_only_declared_joins(
    segments: Sequence[PresentationRouteSegment],
    node_positions: Mapping[str, Point2D],
) -> bool:
    for index, first in enumerate(segments):
        if not _is_orthogonal(first.points):
            return False

        for second in segments[index + 1:]:
            if not _is_orthogonal(second.points):
                return False

            shared_node_ids = (
                {first.start_node_id, first.end_node_id}
                & {second.start_node_id, second.end_node_id}
            )
            allowed_points = tuple(
                node_positions[node_id]
                for node_id in shared_node_ids
            )

            for first_start, first_end in zip(
                first.points, first.points[1:]
            ):
                for second_start, second_end in zip(
                    second.points, second.points[1:]
                ):
                    kind, intersection = _intersect_edges(
                        first_start,
                        first_end,
                        second_start,
                        second_end,
                    )
                    if kind == "overlap":
                        return False
                    if kind == "point" and not any(
                        _same(intersection, allowed)
                        for allowed in allowed_points
                    ):
                        return False

    return True


def build_four_connection_presentation_route_graph(
    *,
    connections: Sequence[PresentationEndpointGeometry],
    expected_connection_ids: Sequence[str],
    branch_members: Mapping[str, Sequence[str]],
    obstacles: Sequence[object],
    route_between: RouteFunction,
    trunk_entry_fraction: float = 0.25,
    trunk_split_fraction: float = 0.62,
    pair_branch_offset: float = 24.0,
) -> PresentationRouteGraph | None:
    """Build a validated four-member merge/trunk/two-branch presentation.

    The two explicit member pairs merge at separate visual branch points,
    feed a four-member shared trunk, and split into those same two pairs.
    Every original connection keeps its own endpoint fan-in and fan-out.

    ``route_between`` must return an obstacle-clear orthogonal route, or
    ``None`` when no suitable route exists. It receives prior protected
    route segments that do not share an intentional graph node with the
    requested route.

    Returns ``None`` when routing fails or the resulting paths cross or
    overlap outside explicitly shared graph nodes. Invalid input raises
    ``ValueError``.
    """
    expected_ids = tuple(
        _identifier(value, "expected connection id")
        for value in expected_connection_ids
    )
    if len(expected_ids) != 4 or len(set(expected_ids)) != 4:
        raise ValueError("the bounded presentation prototype requires four unique connections")

    records = tuple(connections)
    by_id = {record.connection_id: record for record in records}
    if len(by_id) != len(records):
        raise ValueError("connection geometry IDs must be unique")
    if set(by_id) != set(expected_ids):
        raise ValueError(
            "connection geometry coverage must exactly match expected_connection_ids"
        )
    if len(records) != 4:
        raise ValueError("the bounded presentation prototype requires four geometries")

    if not isinstance(branch_members, Mapping) or len(branch_members) != 2:
        raise ValueError("branch_members must define exactly two explicit groups")

    normalized_branches: list[tuple[str, tuple[str, ...]]] = []
    flattened_members: list[str] = []

    for branch_id, raw_members in branch_members.items():
        branch_id = _identifier(branch_id, "branch id")
        members = tuple(
            _identifier(value, f"branch {branch_id} member id")
            for value in raw_members
        )
        if len(members) != 2 or len(set(members)) != 2:
            raise ValueError("each presentation branch must have two unique members")
        normalized_branches.append((branch_id, members))
        flattened_members.extend(members)

    if (
        len(flattened_members) != 4
        or len(set(flattened_members)) != 4
        or set(flattened_members) != set(expected_ids)
    ):
        raise ValueError(
            "the two explicit branch groups must partition all four connections"
        )

    if (
        not math.isfinite(trunk_entry_fraction)
        or not math.isfinite(trunk_split_fraction)
        or not (0.0 < trunk_entry_fraction < trunk_split_fraction < 1.0)
    ):
        raise ValueError(
            "trunk fractions must satisfy 0 < entry < split < 1"
        )
    if not math.isfinite(pair_branch_offset) or pair_branch_offset <= 0.0:
        raise ValueError("pair_branch_offset must be finite and positive")

    ordered_records = tuple(by_id[connection_id] for connection_id in expected_ids)
    visual_endpoint_ids = [
        endpoint_id
        for record in ordered_records
        for endpoint_id in (
            record.visual_endpoint_a_id,
            record.visual_endpoint_b_id,
        )
    ]
    if len(set(visual_endpoint_ids)) != len(visual_endpoint_ids):
        raise ValueError("visual endpoint IDs must be unique in this four-wire prototype")

    start_escape_ends = {
        record.connection_id: record.start_escape_points[-1]
        for record in ordered_records
    }
    end_escape_ends = {
        record.connection_id: record.end_escape_points[-1]
        for record in ordered_records
    }

    source_center = _centroid(tuple(start_escape_ends.values()))
    terminal_center = _centroid(tuple(end_escape_ends.values()))
    route_dx = terminal_center[0] - source_center[0]
    route_dy = terminal_center[1] - source_center[1]
    route_length = math.hypot(route_dx, route_dy)

    if route_length <= _EPSILON:
        return None

    direction = (route_dx / route_length, route_dy / route_length)

    if abs(direction[0]) >= abs(direction[1]):
        source_route_direction = "right" if direction[0] > 0.0 else "left"
    else:
        source_route_direction = "down" if direction[1] > 0.0 else "up"

    if pair_branch_offset >= min(
        route_length * trunk_entry_fraction,
        route_length * (1.0 - trunk_split_fraction),
    ):
        return None

    shared_entry = (
        source_center[0] + direction[0] * route_length * trunk_entry_fraction,
        source_center[1] + direction[1] * route_length * trunk_entry_fraction,
    )
    nominal_split = (
        source_center[0] + direction[0] * route_length * trunk_split_fraction,
        source_center[1] + direction[1] * route_length * trunk_split_fraction,
    )

    if _same(shared_entry, nominal_split):
        return None

    source_pair_positions: dict[str, Point2D] = {}
    terminal_pair_positions: dict[str, Point2D] = {}

    for branch_id, members in normalized_branches:
        source_pair_center = _centroid(
            tuple(start_escape_ends[member] for member in members)
        )
        terminal_pair_center = _centroid(
            tuple(end_escape_ends[member] for member in members)
        )
        source_pair_positions[branch_id] = (
            source_pair_center[0] + direction[0] * pair_branch_offset,
            source_pair_center[1] + direction[1] * pair_branch_offset,
        )
        terminal_pair_positions[branch_id] = (
            terminal_pair_center[0] - direction[0] * pair_branch_offset,
            terminal_pair_center[1] - direction[1] * pair_branch_offset,
        )

    nodes: list[PresentationRouteNode] = []
    node_positions: dict[str, Point2D] = {}

    def add_node(node_id: str, position: Point2D, kind: str) -> None:
        if node_id in node_positions:
            raise ValueError(f"duplicate presentation node ID: {node_id}")
        node_positions[node_id] = position
        nodes.append(
            PresentationRouteNode(
                id=node_id,
                position=position,
                kind=kind,
            )
        )

    for record in ordered_records:
        add_node(
            record.visual_endpoint_a_id,
            record.start_position,
            "endpoint",
        )
        add_node(
            record.visual_endpoint_b_id,
            record.end_position,
            "endpoint",
        )

    for branch_id, _ in normalized_branches:
        add_node(
            f"presentation-source-pair:{branch_id}",
            source_pair_positions[branch_id],
            "branch_point",
        )

    add_node(
        "presentation-shared-entry",
        shared_entry,
        "branch_point",
    )


    for branch_id, _ in normalized_branches:
        add_node(
            f"presentation-terminal-pair:{branch_id}",
            terminal_pair_positions[branch_id],
            "branch_point",
        )

    segments: list[PresentationRouteSegment] = []

    def add_segment(
        segment_id: str,
        start_node_id: str,
        end_node_id: str,
        members: Sequence[str],
        path: Sequence[Point2D],
    ) -> bool:
        cleaned = _clean_path(path)
        if len(cleaned) < 2 or not _is_orthogonal(cleaned):
            return False

        segments.append(
            PresentationRouteSegment(
                id=segment_id,
                start_node_id=start_node_id,
                end_node_id=end_node_id,
                member_connection_ids=tuple(members),
                points=cleaned,
            )
        )
        return True

    # Individual endpoint fan-ins to the two explicit pair merge nodes.
    for branch_id, members in normalized_branches:
        pair_node_id = f"presentation-source-pair:{branch_id}"

        for connection_id in members:
            record = by_id[connection_id]
            escape_end = record.start_escape_points[-1]
            pair_position = source_pair_positions[branch_id]

            routed = _request_route(
                start=escape_end,
                end=pair_position,
                start_direction=record.start_direction,
                end_direction="none",
                obstacles=obstacles,
                existing_segments=segments,
                start_node_id=record.visual_endpoint_a_id,
                end_node_id=pair_node_id,
                route_between=route_between,
                allow_same_point=True,
            )
            if routed is None:
                return None

            entry_path = _clean_path(
                (
                    record.start_position,
                    record.start_route_position,
                    *record.start_escape_points[1:],
                    *routed[1:],
                )
            )
            if not add_segment(
                f"presentation-entry:{connection_id}",
                record.visual_endpoint_a_id,
                pair_node_id,
                (connection_id,),
                entry_path,
            ):
                return None

    # Each two-member pair feeds the four-member shared trunk.
    for branch_id, members in normalized_branches:
        pair_node_id = f"presentation-source-pair:{branch_id}"
        pair_position = source_pair_positions[branch_id]

        routed = _request_route(
            start=pair_position,
            end=shared_entry,
            start_direction=source_route_direction,
            end_direction="none",
            obstacles=obstacles,
            existing_segments=segments,
            start_node_id=pair_node_id,
            end_node_id="presentation-shared-entry",
            route_between=route_between,
            allow_same_point=False,
        )
        if routed is None or not add_segment(
            f"presentation-source-pair-route:{branch_id}",
            pair_node_id,
            "presentation-shared-entry",
            members,
            routed,
        ):
            return None

    # Route the trunk first, then branch at a usable point on its path.
    end_route_direction = {
        "right": "left",
        "left": "right",
        "up": "down",
        "down": "up",
    }[source_route_direction]
    trunk_candidate = _request_route(
        start=shared_entry,
        end=nominal_split,
        start_direction=source_route_direction,
        end_direction=end_route_direction,
        obstacles=obstacles,
        existing_segments=segments,
        start_node_id="presentation-shared-entry",
        end_node_id="presentation-trunk-target",
        route_between=route_between,
        allow_same_point=False,
    )
    if trunk_candidate is None:
        return None

    if len(trunk_candidate) >= 3:
        split = trunk_candidate[-2]
        trunk_points = trunk_candidate[:-1]
    else:
        first = trunk_candidate[0]
        last = trunk_candidate[-1]
        split = (
            first[0] + (last[0] - first[0]) * 0.8,
            first[1] + (last[1] - first[1]) * 0.8,
        )
        trunk_points = (first, split)

    if _same(shared_entry, split):
        return None

    add_node(
        "presentation-trunk-split",
        split,
        "branch_point",
    )

    if not add_segment(
        "presentation-shared-trunk",
        "presentation-shared-entry",
        "presentation-trunk-split",
        expected_ids,
        trunk_points,
    ):
        return None

    # The shared trunk splits into the two explicitly declared member pairs.
    for branch_id, members in normalized_branches:
        terminal_node_id = f"presentation-terminal-pair:{branch_id}"
        terminal_position = terminal_pair_positions[branch_id]

        branch_start_direction = _perpendicular_departure_direction(
            direction,
            split,
            terminal_position,
        )
        if branch_start_direction is None:
            return None

        routed = _request_route(
            start=split,
            end=terminal_position,
            start_direction=branch_start_direction,
            end_direction=end_route_direction,
            obstacles=obstacles,
            existing_segments=segments,
            start_node_id="presentation-trunk-split",
            end_node_id=terminal_node_id,
            route_between=route_between,
            allow_same_point=False,
        )
        if routed is None or not add_segment(
            f"presentation-branch:{branch_id}",
            "presentation-trunk-split",
            terminal_node_id,
            members,
            routed,
        ):
            return None

    # Individual endpoint fan-outs retain each original end escape.
    for branch_id, members in normalized_branches:
        terminal_node_id = f"presentation-terminal-pair:{branch_id}"
        terminal_position = terminal_pair_positions[branch_id]

        for connection_id in members:
            record = by_id[connection_id]
            escape_end = record.end_escape_points[-1]

            exit_start_direction = _perpendicular_departure_direction(
                direction,
                terminal_position,
                escape_end,
            )
            if exit_start_direction is None:
                return None

            routed = _request_route(
                start=terminal_position,
                end=escape_end,
                start_direction=exit_start_direction,
                end_direction=record.end_direction,
                obstacles=obstacles,
                existing_segments=segments,
                start_node_id=terminal_node_id,
                end_node_id=record.visual_endpoint_b_id,
                route_between=route_between,
                allow_same_point=True,
            )
            if routed is None:
                return None

            exit_path = _clean_path(
                (
                    *routed,
                    *reversed(record.end_escape_points[:-1]),
                    record.end_route_position,
                    record.end_position,
                )
            )
            if not add_segment(
                f"presentation-exit:{connection_id}",
                terminal_node_id,
                record.visual_endpoint_b_id,
                (connection_id,),
                exit_path,
            ):
                return None

    # Do not silently turn crossings or overlapping paths into junctions.
    if not _segments_have_only_declared_joins(segments, node_positions):
        return None

    branch_id_for_connection = {
        connection_id: branch_id
        for branch_id, members in normalized_branches
        for connection_id in members
    }

    routes = []
    for record in ordered_records:
        branch_id = branch_id_for_connection[record.connection_id]
        routes.append(
            PresentationConnectionRoute(
                connection_id=record.connection_id,
                canonical_endpoint_a_id=record.canonical_endpoint_a_id,
                canonical_endpoint_b_id=record.canonical_endpoint_b_id,
                visual_endpoint_a_id=record.visual_endpoint_a_id,
                visual_endpoint_b_id=record.visual_endpoint_b_id,
                segment_ids=(
                    f"presentation-entry:{record.connection_id}",
                    f"presentation-source-pair-route:{branch_id}",
                    "presentation-shared-trunk",
                    f"presentation-branch:{branch_id}",
                    f"presentation-exit:{record.connection_id}",
                ),
            )
        )

    return PresentationRouteGraph(
        nodes=tuple(nodes),
        segments=tuple(segments),
        connection_routes=tuple(routes),
        expected_connection_ids=expected_ids,
    )