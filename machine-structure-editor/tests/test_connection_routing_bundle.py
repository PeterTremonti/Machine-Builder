import pytest
from PySide6.QtCore import QPointF

from machine_builder.graphics.connection_routing_bundle import (
    bundle_envelope_half_width,
    centered_lane_offsets,
    offset_orthogonal_route,
    lane_order_is_compatible,
)


def _points(points):
    return [(round(point.x(), 6), round(point.y(), 6)) for point in points]


def test_centered_lane_offsets_are_evenly_spaced_and_centered():
    assert centered_lane_offsets(4, 8.0) == (-12.0, -4.0, 4.0, 12.0)
    assert centered_lane_offsets(3, 8.0) == (-8.0, 0.0, 8.0)
    assert centered_lane_offsets(1, 8.0) == (0.0,)


def test_centered_lane_offsets_reject_invalid_inputs():
    with pytest.raises(ValueError):
        centered_lane_offsets(0, 8.0)
    with pytest.raises(ValueError):
        centered_lane_offsets(4, 0.0)
    with pytest.raises(ValueError):
        centered_lane_offsets(4, float("inf"))


def test_bundle_envelope_accounts_for_outer_lane_wire_radius_and_clearance():
    assert bundle_envelope_half_width(
        4,
        8.0,
        conductor_radius=1.0,
        extra_clearance=3.0,
    ) == 16.0


def test_offset_route_builds_parallel_lanes_through_a_right_angle():
    centerline = [
        QPointF(0.0, 0.0),
        QPointF(100.0, 0.0),
        QPointF(100.0, 100.0),
    ]

    offsets = centered_lane_offsets(4, 8.0)
    lanes = [
        offset_orthogonal_route(centerline, offset)
        for offset in offsets
    ]

    assert all(lane is not None for lane in lanes)
    assert _points(lanes[0]) == [(0.0, -12.0), (112.0, -12.0), (112.0, 100.0)]
    assert _points(lanes[1]) == [(0.0, -4.0), (104.0, -4.0), (104.0, 100.0)]
    assert _points(lanes[2]) == [(0.0, 4.0), (96.0, 4.0), (96.0, 100.0)]
    assert _points(lanes[3]) == [(0.0, 12.0), (88.0, 12.0), (88.0, 100.0)]


def test_offset_route_simplifies_collinear_segments():
    centerline = [
        QPointF(0.0, 0.0),
        QPointF(50.0, 0.0),
        QPointF(100.0, 0.0),
        QPointF(100.0, 50.0),
    ]

    lane = offset_orthogonal_route(centerline, 4.0)

    assert _points(lane) == [(0.0, 4.0), (96.0, 4.0), (96.0, 50.0)]


def test_offset_route_rejects_diagonal_and_reversing_geometry():
    diagonal = [QPointF(0.0, 0.0), QPointF(10.0, 10.0)]
    reversing = [
        QPointF(0.0, 0.0),
        QPointF(10.0, 0.0),
        QPointF(0.0, 0.0),
    ]

    assert offset_orthogonal_route(diagonal, 4.0) is None
    assert offset_orthogonal_route(reversing, 4.0) is None


def test_offset_route_rejects_offsets_that_collapse_a_short_bend():
    centerline = [
        QPointF(0.0, 0.0),
        QPointF(10.0, 0.0),
        QPointF(10.0, 100.0),
    ]

    assert offset_orthogonal_route(centerline, 4.0) is not None
    assert offset_orthogonal_route(centerline, 10.0) is None


def test_offset_route_does_not_mutate_its_input():
    centerline = [
        QPointF(0.0, 0.0),
        QPointF(100.0, 0.0),
        QPointF(100.0, 100.0),
    ]
    original = _points(centerline)

    offset_orthogonal_route(centerline, 8.0)

    assert _points(centerline) == original


def test_lane_order_is_compatible_when_member_order_is_preserved():
    start = {
        "wire-black": -12.0,
        "wire-red": -4.0,
        "wire-green": 4.0,
        "wire-blue": 12.0,
    }
    end = {
        "wire-green": 4.0,
        "wire-black": -12.0,
        "wire-blue": 12.0,
        "wire-red": -4.0,
    }

    assert lane_order_is_compatible(start, end)


def test_lane_order_is_rejected_when_member_order_is_reversed():
    start = {"wire-a": -8.0, "wire-b": 0.0, "wire-c": 8.0}
    end = {"wire-a": 8.0, "wire-b": 0.0, "wire-c": -8.0}

    assert not lane_order_is_compatible(start, end)


def test_lane_order_is_rejected_when_member_sets_differ():
    start = {"wire-a": -4.0, "wire-b": 4.0}
    missing = {"wire-a": -4.0}
    extra = {"wire-a": -4.0, "wire-b": 4.0, "wire-c": 12.0}

    assert not lane_order_is_compatible(start, missing)
    assert not lane_order_is_compatible(start, extra)


@pytest.mark.parametrize(
    ("start", "end"),
    [
        ({"wire-a": 0.0, "wire-b": 0.0}, {"wire-a": 0.0, "wire-b": 1.0}),
        ({"wire-a": 0.0, "wire-b": 1.0}, {"wire-a": 2.0, "wire-b": 2.0}),
    ],
)
def test_lane_order_is_rejected_when_offsets_are_indistinguishable(start, end):
    assert not lane_order_is_compatible(start, end)


@pytest.mark.parametrize("invalid_offset", [float("nan"), float("inf"), True])
def test_lane_order_is_rejected_when_an_offset_is_invalid(invalid_offset):
    start = {"wire-a": -1.0, "wire-b": invalid_offset}
    end = {"wire-a": -1.0, "wire-b": 1.0}

    assert not lane_order_is_compatible(start, end)


def test_lane_order_requires_multiple_members_and_nonblank_ids():
    assert not lane_order_is_compatible({"wire-a": 0.0}, {"wire-a": 0.0})
    assert not lane_order_is_compatible(
        {"wire-a": -1.0, " ": 1.0},
        {"wire-a": -1.0, " ": 1.0},
    )


@pytest.mark.parametrize("epsilon", [0.0, -1.0, float("inf")])
def test_lane_order_rejects_invalid_epsilon(epsilon):
    with pytest.raises(ValueError, match="epsilon"):
        lane_order_is_compatible(
            {"wire-a": -1.0, "wire-b": 1.0},
            {"wire-a": -1.0, "wire-b": 1.0},
            epsilon=epsilon,
        )
