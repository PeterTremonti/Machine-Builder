"""Runtime-only presentation route graph over existing connections.

This graph describes displayed route topology. It is not a canonical machine
entity, an electrical connectivity graph, a physical path, or a Harness.

Coordinates are plain canvas-space (x, y) tuples so this module has no Qt
dependency and can be tested independently of the graphics scene.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


Point2D = tuple[float, float]

_ALLOWED_NODE_KINDS = frozenset(
    {
        "endpoint",
        "waypoint",
        "branch_point",
    }
)
_POINT_TOLERANCE = 1e-6


def _require_identifier(value: object, field_name: str) -> str:
    """Return a nonblank identifier or reject the record."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonblank string")
    return value


def _normalize_identifiers(
    values: object,
    field_name: str,
    *,
    minimum: int,
) -> tuple[str, ...]:
    """Normalize an ordered collection of unique, nonblank identifiers."""
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{field_name} must be a collection of identifiers")

    try:
        result = tuple(values)
    except TypeError as exc:
        raise ValueError(
            f"{field_name} must be a collection of identifiers"
        ) from exc

    if len(result) < minimum:
        raise ValueError(
            f"{field_name} must contain at least {minimum} identifier(s)"
        )

    normalized = tuple(
        _require_identifier(value, field_name)
        for value in result
    )
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")

    return normalized


def _normalize_point(value: object, field_name: str) -> Point2D:
    """Normalize one finite two-dimensional point."""
    if isinstance(value, (str, bytes)):
        raise ValueError(f"{field_name} must be a two-number point")

    try:
        coordinates = tuple(value)
    except TypeError as exc:
        raise ValueError(
            f"{field_name} must be a two-number point"
        ) from exc

    if len(coordinates) != 2:
        raise ValueError(f"{field_name} must contain exactly two coordinates")

    normalized: list[float] = []
    for coordinate in coordinates:
        if isinstance(coordinate, bool):
            raise ValueError(f"{field_name} coordinates must be finite numbers")
        try:
            number = float(coordinate)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(
                f"{field_name} coordinates must be finite numbers"
            ) from exc
        if not math.isfinite(number):
            raise ValueError(f"{field_name} coordinates must be finite numbers")
        normalized.append(number)

    return (normalized[0], normalized[1])


def _normalize_points(
    values: object,
    field_name: str,
    *,
    minimum: int,
) -> tuple[Point2D, ...]:
    """Normalize an ordered polyline."""
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{field_name} must be a collection of points")

    try:
        raw_points = tuple(values)
    except TypeError as exc:
        raise ValueError(
            f"{field_name} must be a collection of points"
        ) from exc

    if len(raw_points) < minimum:
        raise ValueError(
            f"{field_name} must contain at least {minimum} point(s)"
        )

    return tuple(
        _normalize_point(point, f"{field_name}[{index}]")
        for index, point in enumerate(raw_points)
    )


def _same_point(first: Point2D, second: Point2D) -> bool:
    """Return whether two points agree within the geometry tolerance."""
    return (
        abs(first[0] - second[0]) <= _POINT_TOLERANCE
        and abs(first[1] - second[1]) <= _POINT_TOLERANCE
    )


@dataclass(frozen=True, slots=True)
class PresentationRouteNode:
    """A derived endpoint, waypoint, or visual branch point."""

    id: str
    position: Point2D
    kind: str = "waypoint"

    def __post_init__(self) -> None:
        _require_identifier(self.id, "node id")
        object.__setattr__(
            self,
            "position",
            _normalize_point(self.position, "node position"),
        )
        if self.kind not in _ALLOWED_NODE_KINDS:
            raise ValueError(
                f"node kind must be one of {sorted(_ALLOWED_NODE_KINDS)}"
            )


@dataclass(frozen=True, slots=True)
class PresentationRouteSegment:
    """One displayed polyline and its exact canonical connection membership.

    ``points`` runs from ``start_node_id`` to ``end_node_id``.
    Membership is explicit; it is never inferred from overlapping geometry.
    """

    id: str
    start_node_id: str
    end_node_id: str
    member_connection_ids: tuple[str, ...]
    points: tuple[Point2D, ...]

    def __post_init__(self) -> None:
        _require_identifier(self.id, "segment id")
        _require_identifier(self.start_node_id, "segment start node id")
        _require_identifier(self.end_node_id, "segment end node id")
        if self.start_node_id == self.end_node_id:
            raise ValueError("a route segment must have distinct endpoint nodes")

        object.__setattr__(
            self,
            "member_connection_ids",
            _normalize_identifiers(
                self.member_connection_ids,
                "segment member_connection_ids",
                minimum=1,
            ),
        )
        object.__setattr__(
            self,
            "points",
            _normalize_points(
                self.points,
                "segment points",
                minimum=2,
            ),
        )


@dataclass(frozen=True, slots=True)
class PresentationConnectionRoute:
    """One canonical connection's traversal through presentation segments.

    Canonical endpoint IDs are retained unchanged. Visual endpoint IDs refer
    to the corresponding VisualConnection endpoint ports and anchor the
    presentation traversal. ``segment_ids`` is ordered from visual endpoint A
    to visual endpoint B; individual fan-out segments are included.
    """

    connection_id: str
    canonical_endpoint_a_id: str
    canonical_endpoint_b_id: str
    visual_endpoint_a_id: str
    visual_endpoint_b_id: str
    segment_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_identifier(self.connection_id, "connection id")
        _require_identifier(
            self.canonical_endpoint_a_id,
            "canonical endpoint A id",
        )
        _require_identifier(
            self.canonical_endpoint_b_id,
            "canonical endpoint B id",
        )
        _require_identifier(
            self.visual_endpoint_a_id,
            "visual endpoint A id",
        )
        _require_identifier(
            self.visual_endpoint_b_id,
            "visual endpoint B id",
        )
        object.__setattr__(
            self,
            "segment_ids",
            _normalize_identifiers(
                self.segment_ids,
                "connection segment_ids",
                minimum=1,
            ),
        )


@dataclass(frozen=True, slots=True)
class PresentationRouteGraph:
    """Validated, immutable presentation topology over existing connections.

    The graph is deliberately independent of SemanticModel, VisualModel,
    Qt, persistence, and Harness. Its caller supplies an explicit grouping
    decision and the exact endpoints/geometry derived from current state.

    Construction validates:
    - unique node, segment, and connection-route identities;
    - valid segment endpoints and endpoint geometry;
    - continuous traversal for every represented connection;
    - exact agreement between segment membership and connection traversals;
    - complete coverage of the explicitly supplied expected connection IDs;
    - absence of unreferenced segments or unknown members.

    Rebuild this value when its source connections, layout, or route geometry
    changes. It has no persistent machine identity.
    """

    nodes: tuple[PresentationRouteNode, ...]
    segments: tuple[PresentationRouteSegment, ...]
    connection_routes: tuple[PresentationConnectionRoute, ...]
    expected_connection_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "nodes", tuple(self.nodes))
        object.__setattr__(self, "segments", tuple(self.segments))
        object.__setattr__(
            self,
            "connection_routes",
            tuple(self.connection_routes),
        )
        object.__setattr__(
            self,
            "expected_connection_ids",
            _normalize_identifiers(
                self.expected_connection_ids,
                "expected_connection_ids",
                minimum=1,
            ),
        )
        self.validate()

    def validate(self) -> None:
        """Raise ValueError when topology or exact membership is inconsistent."""
        if any(not isinstance(node, PresentationRouteNode) for node in self.nodes):
            raise ValueError("nodes must contain PresentationRouteNode records")
        if any(
            not isinstance(segment, PresentationRouteSegment)
            for segment in self.segments
        ):
            raise ValueError(
                "segments must contain PresentationRouteSegment records"
            )
        if any(
            not isinstance(route, PresentationConnectionRoute)
            for route in self.connection_routes
        ):
            raise ValueError(
                "connection_routes must contain PresentationConnectionRoute records"
            )

        node_by_id = {node.id: node for node in self.nodes}
        if len(node_by_id) != len(self.nodes):
            raise ValueError("node ids must be unique")

        segment_by_id = {segment.id: segment for segment in self.segments}
        if len(segment_by_id) != len(self.segments):
            raise ValueError("segment ids must be unique")

        route_by_connection_id = {
            route.connection_id: route for route in self.connection_routes
        }
        if len(route_by_connection_id) != len(self.connection_routes):
            raise ValueError("connection route ids must be unique")
        expected_connection_ids = set(self.expected_connection_ids)
        actual_connection_ids = set(route_by_connection_id)
        if actual_connection_ids != expected_connection_ids:
            missing = sorted(expected_connection_ids - actual_connection_ids)
            unexpected = sorted(actual_connection_ids - expected_connection_ids)
            raise ValueError(
                "connection route coverage mismatch: "
                f"missing {missing}, unexpected {unexpected}"
            )

        for segment in self.segments:
            start_node = node_by_id.get(segment.start_node_id)
            end_node = node_by_id.get(segment.end_node_id)
            if start_node is None or end_node is None:
                raise ValueError(
                    f"segment {segment.id!r} references an unknown route node"
                )
            if not _same_point(segment.points[0], start_node.position):
                raise ValueError(
                    f"segment {segment.id!r} geometry does not start at its node"
                )
            if not _same_point(segment.points[-1], end_node.position):
                raise ValueError(
                    f"segment {segment.id!r} geometry does not end at its node"
                )

        derived_members: dict[str, set[str]] = {
            segment.id: set() for segment in self.segments
        }

        for route in self.connection_routes:
            start_node = node_by_id.get(route.visual_endpoint_a_id)
            end_node = node_by_id.get(route.visual_endpoint_b_id)

            if start_node is None or end_node is None:
                raise ValueError(
                    f"connection {route.connection_id!r} has an unknown "
                    "visual endpoint node"
                )
            if start_node.kind != "endpoint" or end_node.kind != "endpoint":
                raise ValueError(
                    f"connection {route.connection_id!r} visual endpoints "
                    "must use endpoint nodes"
                )

            current_node_id = route.visual_endpoint_a_id

            for segment_id in route.segment_ids:
                segment = segment_by_id.get(segment_id)
                if segment is None:
                    raise ValueError(
                        f"connection {route.connection_id!r} references "
                        f"unknown segment {segment_id!r}"
                    )

                if segment.start_node_id == current_node_id:
                    current_node_id = segment.end_node_id
                elif segment.end_node_id == current_node_id:
                    current_node_id = segment.start_node_id
                else:
                    raise ValueError(
                        f"connection {route.connection_id!r} traversal is "
                        f"disconnected at segment {segment_id!r}"
                    )

                derived_members[segment_id].add(route.connection_id)

            if current_node_id != route.visual_endpoint_b_id:
                raise ValueError(
                    f"connection {route.connection_id!r} traversal does not "
                    "reach its visual endpoint B"
                )

        for segment in self.segments:
            declared = set(segment.member_connection_ids)
            derived = derived_members[segment.id]

            if declared != derived:
                raise ValueError(
                    f"segment {segment.id!r} membership mismatch: "
                    f"declared {sorted(declared)}, traversed {sorted(derived)}"
                )

            if not derived:
                raise ValueError(
                    f"segment {segment.id!r} is not used by any connection"
                )

    def segment_for_id(self, segment_id: str) -> PresentationRouteSegment:
        """Resolve a runtime segment ID to its immutable segment record."""
        for segment in self.segments:
            if segment.id == segment_id:
                return segment
        raise KeyError(segment_id)

    def connection_route_for_id(
        self,
        connection_id: str,
    ) -> PresentationConnectionRoute:
        """Resolve a canonical connection ID to its presentation traversal."""
        for route in self.connection_routes:
            if route.connection_id == connection_id:
                return route
        raise KeyError(connection_id)

    def connection_ids_for_segment(
        self,
        segment_id: str,
    ) -> tuple[str, ...]:
        """Return the exact canonical connections represented by a segment."""
        return self.segment_for_id(segment_id).member_connection_ids

    def segment_ids_for_connection(
        self,
        connection_id: str,
    ) -> tuple[str, ...]:
        """Return the ordered presentation traversal for one connection."""
        return self.connection_route_for_id(connection_id).segment_ids