from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF

import pytest

from machine_builder.graphics.connection_routing import ConnectionRoutingEngine
from machine_builder.presentation_route_builder import (
    PresentationEndpointGeometry,
    build_four_connection_presentation_route_graph,
)


CONNECTION_IDS = (
    "connection-4",
    "connection-5",
    "connection-6",
    "connection-7",
)

BRANCH_MEMBERS = {
    "pair-one": ("connection-4", "connection-5"),
    "pair-two": ("connection-6", "connection-7"),
}


def _endpoint_geometries():
    records = []
    for index, connection_id in enumerate(CONNECTION_IDS):
        y = float(index * 10)
        records.append(
            PresentationEndpointGeometry(
                connection_id=connection_id,
                canonical_endpoint_a_id=f"canonical-a:{connection_id}",
                canonical_endpoint_b_id=f"canonical-b:{connection_id}",
                visual_endpoint_a_id=f"visual-a:{connection_id}",
                visual_endpoint_b_id=f"visual-b:{connection_id}",
                start_position=(0.0, y),
                start_route_position=(0.0, y),
                start_escape_points=((0.0, y), (30.0, y)),
                start_direction="right",
                end_position=(300.0, y),
                end_route_position=(300.0, y),
                end_escape_points=((300.0, y), (270.0, y)),
                end_direction="left",
            )
        )
    return tuple(records)


def _orthogonal_route(
    start,
    end,
    start_direction,
    end_direction,
    obstacles,
    protected_segments,
):
    """Deterministic route geometry for topology and membership tests."""
    if (
        abs(start[0] - end[0]) <= 1e-6
        or abs(start[1] - end[1]) <= 1e-6
    ):
        return [start, end]

    if start_direction in ("up", "down"):
        # Honor vertical departures from the shared trunk and pair nodes.
        return [start, (start[0], end[1]), end]

    if start_direction in ("left", "right"):
        # Honor horizontal departures from the individual source endpoints.
        return [start, (end[0], start[1]), end]

    if start[0] >= 170.0:
        # Fallback geometry for routes without a requested departure direction.
        return [start, (start[0], end[1]), end]

    # Fallback source-side lane geometry.
    return [start, (end[0], start[1]), end]


def _build(
    route_between=_orthogonal_route,
    branch_members=BRANCH_MEMBERS,
    obstacles=(),
):
    return build_four_connection_presentation_route_graph(
        connections=_endpoint_geometries(),
        expected_connection_ids=CONNECTION_IDS,
        branch_members=branch_members,
        obstacles=obstacles,
        route_between=route_between,
    )


def _engine_route(
    start,
    end,
    start_direction,
    end_direction,
    obstacles,
    protected_segments,
):
    """Adapter from the pure builder coordinates to the Qt routing engine."""
    return ConnectionRoutingEngine.build_route(
        start=QPointF(*start),
        end=QPointF(*end),
        start_direction=start_direction,
        end_direction=end_direction,
        obstacles=list(obstacles),
        protected_segments=[
            (QPointF(*first), QPointF(*second))
            for first, second in protected_segments
        ],
    )


def _engine_presentation_route(
    start,
    end,
    start_direction,
    end_direction,
    obstacles,
    protected_segments,
):
    """Convert the Qt engine result to the builder's coordinate format."""
    route = _engine_route(
        start,
        end,
        start_direction,
        end_direction,
        obstacles,
        protected_segments,
    )
    if route is None:
        return None
    return tuple((point.x(), point.y()) for point in route)


def test_builder_routes_full_graph_around_an_obstacle_with_real_engine():
    obstacle = QRectF(120.0, 8.0, 24.0, 14.0)
    graph = _build(
        route_between=_engine_presentation_route,
        obstacles=(obstacle,),
    )

    assert graph is not None
    assert set(graph.expected_connection_ids) == set(CONNECTION_IDS)
    assert set(
        graph.connection_ids_for_segment("presentation-shared-trunk")
    ) == set(CONNECTION_IDS)

    for segment in graph.segments:
        route = [QPointF(*point) for point in segment.points]
        assert ConnectionRoutingEngine.route_is_clear(route, [obstacle])
        assert all(
            abs(first[0] - second[0]) <= 1e-6
            or abs(first[1] - second[1]) <= 1e-6
            for first, second in zip(segment.points, segment.points[1:])
        )

def test_builder_creates_four_member_trunk_and_two_explicit_branches():
    graph = _build()

    assert graph is not None
    assert set(graph.expected_connection_ids) == set(CONNECTION_IDS)

    assert set(
        graph.connection_ids_for_segment("presentation-shared-trunk")
    ) == set(CONNECTION_IDS)

    assert set(
        graph.connection_ids_for_segment("presentation-branch:pair-one")
    ) == {"connection-4", "connection-5"}

    assert set(
        graph.connection_ids_for_segment("presentation-branch:pair-two")
    ) == {"connection-6", "connection-7"}


def test_builder_preserves_each_connection_identity_and_endpoints():
    graph = _build()

    assert graph is not None
    assert len(graph.connection_routes) == 4

    for route in graph.connection_routes:
        connection_id = route.connection_id
        assert route.canonical_endpoint_a_id == f"canonical-a:{connection_id}"
        assert route.canonical_endpoint_b_id == f"canonical-b:{connection_id}"
        assert route.visual_endpoint_a_id == f"visual-a:{connection_id}"
        assert route.visual_endpoint_b_id == f"visual-b:{connection_id}"
        assert route.segment_ids[2] == "presentation-shared-trunk"
        assert len(route.segment_ids) == 5


def test_builder_creates_individual_endpoint_fan_in_and_fan_out():
    graph = _build()

    assert graph is not None

    for connection_id in CONNECTION_IDS:
        assert set(
            graph.connection_ids_for_segment(
                f"presentation-entry:{connection_id}"
            )
        ) == {connection_id}
        assert set(
            graph.connection_ids_for_segment(
                f"presentation-exit:{connection_id}"
            )
        ) == {connection_id}


def test_builder_rejects_branch_groups_that_do_not_partition_four_members():
    invalid_groups = {
        "pair-one": ("connection-4", "connection-5"),
        "pair-two": ("connection-5", "connection-6"),
    }

    with pytest.raises(ValueError, match="partition all four connections"):
        _build(branch_members=invalid_groups)


def test_builder_returns_none_when_a_required_route_fails():
    def failed_route(*args, **kwargs):
        return None

    assert _build(route_between=failed_route) is None


def test_builder_returns_none_when_route_geometry_is_diagonal():
    def diagonal_route(start, end, *args):
        return [start, end]

    assert _build(route_between=diagonal_route) is None


def test_builder_returns_none_when_branch_paths_overlap():
    def overlapping_branch_route(
        start,
        end,
        start_direction,
        end_direction,
        obstacles,
        protected_segments,
    ):
        if start_direction in ("up", "down") and start[0] < 240.0 and end[0] > start[0]:
            # Both two-member branches attempt to share the same path
            # beyond their declared split point.
            return [start, (end[0], start[1]), end]
        return _orthogonal_route(
            start,
            end,
            start_direction,
            end_direction,
            obstacles,
            protected_segments,
        )

    assert _build(route_between=overlapping_branch_route) is None


def test_connection_routing_engine_adapter_avoids_an_obstacle():
    obstacle = QRectF(40.0, -15.0, 20.0, 30.0)

    route = _engine_route(
        (0.0, 0.0),
        (100.0, 0.0),
        "right",
        "left",
        (obstacle,),
        (),
    )

    assert route is not None
    assert ConnectionRoutingEngine.route_is_clear(route, [obstacle])
    assert all(
        abs(first.x() - second.x()) <= 1e-6
        or abs(first.y() - second.y()) <= 1e-6
        for first, second in zip(route, route[1:])
    )