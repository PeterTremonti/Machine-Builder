"""Tests for the runtime-only presentation route graph."""

from dataclasses import replace

import pytest

from machine_builder.presentation_route_graph import (
    PresentationConnectionRoute,
    PresentationRouteGraph,
    PresentationRouteNode,
    PresentationRouteSegment,
)


CONNECTION_IDS = (
    "connection-4",
    "connection-5",
    "connection-6",
    "connection-7",
)

CANONICAL_ENDPOINTS = {
    "connection-4": (
        "controller-1-x-motor-pin-1",
        "component-node-3-stepper-lead-1",
    ),
    "connection-5": (
        "controller-1-x-motor-pin-2",
        "component-node-3-stepper-lead-2",
    ),
    "connection-6": (
        "controller-1-x-motor-pin-3",
        "component-node-3-stepper-lead-3",
    ),
    "connection-7": (
        "controller-1-x-motor-pin-4",
        "component-node-3-stepper-lead-4",
    ),
}

VISUAL_ENDPOINTS = {
    "connection-4": (
        "node-1-stepper-motor-coil-b1-terminal",
        "node-3-unassigned-motor-lead-endpoint-1",
    ),
    "connection-5": (
        "node-1-stepper-motor-coil-b2-terminal",
        "node-3-unassigned-motor-lead-endpoint-2",
    ),
    "connection-6": (
        "node-1-stepper-motor-coil-a1-terminal",
        "node-3-unassigned-motor-lead-endpoint-3",
    ),
    "connection-7": (
        "node-1-stepper-motor-coil-a2-terminal",
        "node-3-unassigned-motor-lead-endpoint-4",
    ),
}


def _node(node_id, position, kind="waypoint"):
    return PresentationRouteNode(
        id=node_id,
        position=position,
        kind=kind,
    )


def _segment(segment_id, start, end, members, points):
    return PresentationRouteSegment(
        id=segment_id,
        start_node_id=start,
        end_node_id=end,
        member_connection_ids=tuple(members),
        points=tuple(points),
    )


def _four_connection_graph():
    """Build an explicit four-member trunk with two two-member branches."""
    nodes = (
        _node(VISUAL_ENDPOINTS["connection-4"][0], (0, 0), "endpoint"),
        _node(VISUAL_ENDPOINTS["connection-5"][0], (0, 10), "endpoint"),
        _node(VISUAL_ENDPOINTS["connection-6"][0], (0, 20), "endpoint"),
        _node(VISUAL_ENDPOINTS["connection-7"][0], (0, 30), "endpoint"),
        _node("trunk-entry", (40, 15), "branch_point"),
        _node("trunk-split", (120, 15), "branch_point"),
        _node("branch-left-end", (160, 5), "branch_point"),
        _node("branch-right-end", (160, 25), "branch_point"),
        _node(VISUAL_ENDPOINTS["connection-4"][1], (200, 0), "endpoint"),
        _node(VISUAL_ENDPOINTS["connection-5"][1], (200, 10), "endpoint"),
        _node(VISUAL_ENDPOINTS["connection-6"][1], (200, 20), "endpoint"),
        _node(VISUAL_ENDPOINTS["connection-7"][1], (200, 30), "endpoint"),
    )

    segments = (
        # Four individual endpoint fan-ins.
        _segment(
            "entry-4",
            VISUAL_ENDPOINTS["connection-4"][0],
            "trunk-entry",
            ("connection-4",),
            ((0, 0), (40, 15)),
        ),
        _segment(
            "entry-5",
            VISUAL_ENDPOINTS["connection-5"][0],
            "trunk-entry",
            ("connection-5",),
            ((0, 10), (40, 15)),
        ),
        _segment(
            "entry-6",
            VISUAL_ENDPOINTS["connection-6"][0],
            "trunk-entry",
            ("connection-6",),
            ((0, 20), (40, 15)),
        ),
        _segment(
            "entry-7",
            VISUAL_ENDPOINTS["connection-7"][0],
            "trunk-entry",
            ("connection-7",),
            ((0, 30), (40, 15)),
        ),

        # The common displayed trunk represents all four connections.
        _segment(
            "shared-trunk",
            "trunk-entry",
            "trunk-split",
            CONNECTION_IDS,
            ((40, 15), (120, 15)),
        ),

        # Explicit two-plus-two presentation membership.
        _segment(
            "branch-left",
            "trunk-split",
            "branch-left-end",
            ("connection-4", "connection-5"),
            ((120, 15), (160, 5)),
        ),
        _segment(
            "branch-right",
            "trunk-split",
            "branch-right-end",
            ("connection-6", "connection-7"),
            ((120, 15), (160, 25)),
        ),

        # Four individual endpoint fan-outs.
        _segment(
            "exit-4",
            "branch-left-end",
            VISUAL_ENDPOINTS["connection-4"][1],
            ("connection-4",),
            ((160, 5), (200, 0)),
        ),
        _segment(
            "exit-5",
            "branch-left-end",
            VISUAL_ENDPOINTS["connection-5"][1],
            ("connection-5",),
            ((160, 5), (200, 10)),
        ),
        _segment(
            "exit-6",
            "branch-right-end",
            VISUAL_ENDPOINTS["connection-6"][1],
            ("connection-6",),
            ((160, 25), (200, 20)),
        ),
        _segment(
            "exit-7",
            "branch-right-end",
            VISUAL_ENDPOINTS["connection-7"][1],
            ("connection-7",),
            ((160, 25), (200, 30)),
        ),
    )

    routes = tuple(
        PresentationConnectionRoute(
            connection_id=connection_id,
            canonical_endpoint_a_id=CANONICAL_ENDPOINTS[connection_id][0],
            canonical_endpoint_b_id=CANONICAL_ENDPOINTS[connection_id][1],
            visual_endpoint_a_id=VISUAL_ENDPOINTS[connection_id][0],
            visual_endpoint_b_id=VISUAL_ENDPOINTS[connection_id][1],
            segment_ids=(
                f"entry-{connection_id.removeprefix('connection-')}",
                "shared-trunk",
                (
                    "branch-left"
                    if connection_id in ("connection-4", "connection-5")
                    else "branch-right"
                ),
                f"exit-{connection_id.removeprefix('connection-')}",
            ),
        )
        for connection_id in CONNECTION_IDS
    )

    return PresentationRouteGraph(
        nodes=nodes,
        segments=segments,
        connection_routes=routes,
        expected_connection_ids=CONNECTION_IDS,
    )


def test_four_connections_share_one_trunk_and_split_two_plus_two():
    graph = _four_connection_graph()

    assert set(graph.connection_ids_for_segment("shared-trunk")) == set(
        CONNECTION_IDS
    )
    assert set(graph.connection_ids_for_segment("branch-left")) == {
        "connection-4",
        "connection-5",
    }
    assert set(graph.connection_ids_for_segment("branch-right")) == {
        "connection-6",
        "connection-7",
    }


def test_each_connection_has_a_continuous_traversal_through_its_branch():
    graph = _four_connection_graph()

    assert graph.segment_ids_for_connection("connection-4") == (
        "entry-4",
        "shared-trunk",
        "branch-left",
        "exit-4",
    )
    assert graph.segment_ids_for_connection("connection-5") == (
        "entry-5",
        "shared-trunk",
        "branch-left",
        "exit-5",
    )
    assert graph.segment_ids_for_connection("connection-6") == (
        "entry-6",
        "shared-trunk",
        "branch-right",
        "exit-6",
    )
    assert graph.segment_ids_for_connection("connection-7") == (
        "entry-7",
        "shared-trunk",
        "branch-right",
        "exit-7",
    )


@pytest.mark.parametrize("connection_id", CONNECTION_IDS)
def test_original_canonical_and_visual_endpoints_are_preserved(connection_id):
    graph = _four_connection_graph()
    route = graph.connection_route_for_id(connection_id)

    assert (
        route.canonical_endpoint_a_id,
        route.canonical_endpoint_b_id,
    ) == CANONICAL_ENDPOINTS[connection_id]

    assert (
        route.visual_endpoint_a_id,
        route.visual_endpoint_b_id,
    ) == VISUAL_ENDPOINTS[connection_id]


def test_segment_selection_resolves_exact_original_connection_ids():
    graph = _four_connection_graph()

    assert graph.connection_ids_for_segment("branch-left") == (
        "connection-4",
        "connection-5",
    )
    assert graph.connection_ids_for_segment("branch-right") == (
        "connection-6",
        "connection-7",
    )


def test_each_individual_connection_retains_its_own_fan_in_and_fan_out():
    graph = _four_connection_graph()

    for connection_id in CONNECTION_IDS:
        route = graph.connection_route_for_id(connection_id)
        assert route.segment_ids[0] == (
            f"entry-{connection_id.removeprefix('connection-')}"
        )
        assert route.segment_ids[-1] == (
            f"exit-{connection_id.removeprefix('connection-')}"
        )


def test_graph_rejects_a_trunk_with_a_missing_member():
    graph = _four_connection_graph()
    segments = tuple(
        replace(
            segment,
            member_connection_ids=(
                "connection-4",
                "connection-5",
                "connection-6",
            ),
        )
        if segment.id == "shared-trunk"
        else segment
        for segment in graph.segments
    )

    with pytest.raises(ValueError, match="membership mismatch"):
        PresentationRouteGraph(
            nodes=graph.nodes,
            segments=segments,
            connection_routes=graph.connection_routes,
            expected_connection_ids=graph.expected_connection_ids,
        )


def test_graph_rejects_an_extra_branch_member():
    graph = _four_connection_graph()
    segments = tuple(
        replace(
            segment,
            member_connection_ids=(
                "connection-4",
                "connection-5",
                "connection-7",
            ),
        )
        if segment.id == "branch-left"
        else segment
        for segment in graph.segments
    )

    with pytest.raises(ValueError, match="membership mismatch"):
        PresentationRouteGraph(
            nodes=graph.nodes,
            segments=segments,
            connection_routes=graph.connection_routes,
            expected_connection_ids=graph.expected_connection_ids,
        )


def test_graph_rejects_a_disconnected_connection_traversal():
    graph = _four_connection_graph()
    routes = tuple(
        replace(
            route,
            segment_ids=("entry-4", "branch-left", "shared-trunk", "exit-4"),
        )
        if route.connection_id == "connection-4"
        else route
        for route in graph.connection_routes
    )

    with pytest.raises(ValueError, match="traversal is disconnected"):
        PresentationRouteGraph(
            nodes=graph.nodes,
            segments=graph.segments,
            connection_routes=routes,
            expected_connection_ids=graph.expected_connection_ids,
        )


def test_graph_rejects_an_unknown_segment_reference():
    graph = _four_connection_graph()
    routes = tuple(
        replace(
            route,
            segment_ids=("entry-4", "missing-segment", "branch-left", "exit-4"),
        )
        if route.connection_id == "connection-4"
        else route
        for route in graph.connection_routes
    )

    with pytest.raises(ValueError, match="unknown segment"):
        PresentationRouteGraph(
            nodes=graph.nodes,
            segments=graph.segments,
            connection_routes=routes,
            expected_connection_ids=graph.expected_connection_ids,
        )


def test_graph_rejects_segment_geometry_that_misses_its_start_node():
    graph = _four_connection_graph()
    segments = tuple(
        replace(
            segment,
            points=((41, 15), (120, 15)),
        )
        if segment.id == "shared-trunk"
        else segment
        for segment in graph.segments
    )

    with pytest.raises(ValueError, match="does not start at its node"):
        PresentationRouteGraph(
            nodes=graph.nodes,
            segments=segments,
            connection_routes=graph.connection_routes,
            expected_connection_ids=graph.expected_connection_ids,
        )


def test_graph_rejects_a_missing_expected_connection_route():
    graph = _four_connection_graph()
    routes = graph.connection_routes[:-1]

    with pytest.raises(
        ValueError,
        match="connection route coverage mismatch",
    ) as error:
        PresentationRouteGraph(
            nodes=graph.nodes,
            segments=graph.segments,
            connection_routes=routes,
            expected_connection_ids=graph.expected_connection_ids,
        )

    assert "connection-7" in str(error.value)


def test_graph_rejects_an_unexpected_connection_route():
    graph = _four_connection_graph()
    routes = (
        replace(
            graph.connection_routes[0],
            connection_id="connection-extra",
        ),
        *graph.connection_routes[1:],
    )

    with pytest.raises(
        ValueError,
        match="connection route coverage mismatch",
    ) as error:
        PresentationRouteGraph(
            nodes=graph.nodes,
            segments=graph.segments,
            connection_routes=routes,
            expected_connection_ids=graph.expected_connection_ids,
        )

    assert "connection-4" in str(error.value)
    assert "connection-extra" in str(error.value)

def test_graph_rejects_duplicate_connection_route_ids():
    graph = _four_connection_graph()
    routes = graph.connection_routes + (graph.connection_routes[0],)

    with pytest.raises(ValueError, match="connection route ids must be unique"):
        PresentationRouteGraph(
            nodes=graph.nodes,
            segments=graph.segments,
            connection_routes=routes,
            expected_connection_ids=graph.expected_connection_ids,
        )


def test_graph_rejects_unknown_visual_endpoint_nodes():
    graph = _four_connection_graph()
    routes = tuple(
        replace(route, visual_endpoint_a_id="missing-endpoint")
        if route.connection_id == "connection-4"
        else route
        for route in graph.connection_routes
    )

    with pytest.raises(ValueError, match="unknown visual endpoint node"):
        PresentationRouteGraph(
            nodes=graph.nodes,
            segments=graph.segments,
            connection_routes=routes,
            expected_connection_ids=graph.expected_connection_ids,
        )


def test_graph_rejects_non_finite_node_coordinates():
    with pytest.raises(ValueError, match="finite numbers"):
        _node("bad-point", (float("nan"), 0.0), "endpoint")


def test_segment_and_connection_lookups_reject_unknown_ids():
    graph = _four_connection_graph()

    with pytest.raises(KeyError):
        graph.segment_for_id("missing-segment")

    with pytest.raises(KeyError):
        graph.connection_route_for_id("missing-connection")