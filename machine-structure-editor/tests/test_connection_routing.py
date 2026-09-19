"""Tests for connection routing geometry."""

from __future__ import annotations

from types import SimpleNamespace

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsEllipseItem,
    QGraphicsRectItem,
    QGraphicsScene,
)

from machine_builder.graphics.connection import (
    ConnectionGraphicsItem,
)
from machine_builder.graphics.connection_routing import (
    ConnectionRoutingEngine,
)


def _application() -> QApplication:
    application = QApplication.instance()

    if application is None:
        application = QApplication([])

    return application


def _segment_points(
    route: list[QPointF],
) -> list[tuple[QPointF, QPointF]]:
    return [
        (
            route[index],
            route[index + 1],
        )
        for index in range(
            len(route) - 1,
        )
    ]


def _segment_clear(
    start: QPointF,
    end: QPointF,
    obstacles: list[QRectF],
) -> bool:
    """Return whether an orthogonal segment avoids the obstacles."""
    return all(
        not (
            (
                abs(start.y() - end.y()) < 0.001
                and rect.top() < start.y() < rect.bottom()
                and max(start.x(), end.x()) > rect.left()
                and min(start.x(), end.x()) < rect.right()
            )
            or (
                abs(start.x() - end.x()) < 0.001
                and rect.left() < start.x() < rect.right()
                and max(start.y(), end.y()) > rect.top()
                and min(start.y(), end.y()) < rect.bottom()
            )
        )
        for rect in obstacles
    )


def test_right_port_stub_moves_outward() -> None:
    point = QPointF(
        100.0,
        50.0,
    )

    stub, direction = (
        ConnectionRoutingEngine.build_endpoint_stub(
            point,
            "right",
        )
    )

    assert stub == QPointF(
        140.0,
        50.0,
    )

    assert direction == "right"


def test_left_port_stub_moves_outward() -> None:
    point = QPointF(
        100.0,
        50.0,
    )

    stub, direction = (
        ConnectionRoutingEngine.build_endpoint_stub(
            point,
            "left",
        )
    )

    assert stub == QPointF(
        60.0,
        50.0,
    )

    assert direction == "left"


def test_clear_endpoint_escape_uses_fixed_outward_lead() -> None:
    point = QPointF(
        100.0,
        50.0,
    )

    escape, direction = (
        ConnectionRoutingEngine.build_endpoint_escape(
            point,
            "right",
            [],
        )
    )

    assert direction == "right"

    assert escape == [
        point,
        QPointF(
            140.0,
            50.0,
        ),
    ]

def test_blocked_endpoint_escape_starts_at_stub_end() -> None:
    obstacle = QRectF(
        120.0,
        40.0,
        10.0,
        100.0,
    )

    point = QPointF(
        100.0,
        90.0,
    )

    escape, direction = (
        ConnectionRoutingEngine.build_endpoint_escape(
            point,
            "right",
            [obstacle],
        )
    )

    assert direction == "right"

    assert len(escape) == 3

    assert escape[0] == QPointF(
        100.0,
        90.0,
    )

    assert escape[1] == QPointF(
        140.0,
        90.0,
    )

    # The escape remains local to the fixed stub.
    # The turn occurs at the stub endpoint.
    assert escape[2].x() == 140.0
    assert escape[2].y() != 90.0

def test_direct_relevance_collects_nearby_obstacle() -> None:
    start = QPointF(
        0.0,
        0.0,
    )

    end = QPointF(
        300.0,
        300.0,
    )

    obstacle = QRectF(
        110.0,
        110.0,
        30.0,
        30.0,
    )

    relevant = (
        ConnectionRoutingEngine.collect_relevant_obstacles(
            direct_start=start,
            direct_end=end,
            prepared_start=start,
            prepared_end=end,
            obstacles=[obstacle],
        )
    )

    assert relevant == [
        obstacle,
    ]


def test_orthogonal_relevance_collects_obstacle_near_probe() -> None:
    start = QPointF(
        0.0,
        0.0,
    )

    end = QPointF(
        300.0,
        300.0,
    )

    obstacle = QRectF(
        140.0,
        -20.0,
        30.0,
        40.0,
    )

    relevant = (
        ConnectionRoutingEngine.collect_relevant_obstacles(
            direct_start=start,
            direct_end=end,
            prepared_start=start,
            prepared_end=end,
            obstacles=[obstacle],
        )
    )

    assert relevant == [
        obstacle,
    ]


def test_distant_obstacle_is_not_relevant() -> None:
    start = QPointF(
        0.0,
        0.0,
    )

    end = QPointF(
        300.0,
        200.0,
    )

    distant_obstacle = QRectF(
        1000.0,
        1000.0,
        180.0,
        100.0,
    )

    relevant = (
        ConnectionRoutingEngine.collect_relevant_obstacles(
            direct_start=start,
            direct_end=end,
            prepared_start=start,
            prepared_end=end,
            obstacles=[distant_obstacle],
        )
    )

    assert relevant == []


def test_distant_obstacle_does_not_change_route() -> None:
    start = QPointF(
        0.0,
        0.0,
    )

    end = QPointF(
        300.0,
        200.0,
    )

    baseline = (
        ConnectionRoutingEngine.build_route(
            start,
            end,
            "right",
            "left",
            [],
        )
    )

    distant_obstacle = QRectF(
        1000.0,
        1000.0,
        180.0,
        100.0,
    )

    with_distant_obstacle = (
        ConnectionRoutingEngine.build_route(
            start,
            end,
            "right",
            "left",
            [distant_obstacle],
        )
    )

    assert with_distant_obstacle == baseline


def test_unobstructed_route_is_orthogonal() -> None:
    route = (
        ConnectionRoutingEngine.build_route(
            QPointF(
                100.0,
                100.0,
            ),
            QPointF(
                300.0,
                200.0,
            ),
            "right",
            "left",
            [],
        )
    )

    for start, end in _segment_points(
        route
    ):
        assert (
            abs(start.x() - end.x())
            < 0.001
            or abs(start.y() - end.y())
            < 0.001
        )


def test_route_reroutes_around_blocking_obstacle() -> None:
    obstacle = QRectF(
        180.0,
        80.0,
        120.0,
        140.0,
    )

    route = (
        ConnectionRoutingEngine.build_route(
            QPointF(
                100.0,
                150.0,
            ),
            QPointF(
                380.0,
                150.0,
            ),
            "right",
            "left",
            [obstacle],
        )
    )

    assert (
        ConnectionRoutingEngine.route_is_clear(
            route,
            [obstacle],
        )
    )

    assert len(route) > 3


def test_routing_margin_is_respected() -> None:
    obstacle = QRectF(
        200.0,
        100.0,
        100.0,
        100.0,
    ).adjusted(
        -ConnectionRoutingEngine.ROUTING_MARGIN,
        -ConnectionRoutingEngine.ROUTING_MARGIN,
        ConnectionRoutingEngine.ROUTING_MARGIN,
        ConnectionRoutingEngine.ROUTING_MARGIN,
    )

    route = (
        ConnectionRoutingEngine.build_route(
            QPointF(
                100.0,
                150.0,
            ),
            QPointF(
                400.0,
                150.0,
            ),
            "right",
            "left",
            [obstacle],
        )
    )

    assert (
        ConnectionRoutingEngine.route_is_clear(
            route,
            [obstacle],
        )
    )


def test_route_stays_orthogonal_after_rerouting() -> None:
    obstacles = [
        QRectF(
            180.0,
            80.0,
            80.0,
            140.0,
        ),
        QRectF(
            300.0,
            40.0,
            100.0,
            140.0,
        ),
    ]

    route = (
        ConnectionRoutingEngine.build_route(
            QPointF(
                100.0,
                150.0,
            ),
            QPointF(
                500.0,
                150.0,
            ),
            "right",
            "left",
            obstacles,
        )
    )

    assert (
        ConnectionRoutingEngine.route_is_clear(
            route,
            obstacles,
        )
    )

    for start, end in _segment_points(
        route
    ):
        assert (
            abs(start.x() - end.x())
            < 0.001
            or abs(start.y() - end.y())
            < 0.001
        )


def test_simplifier_does_not_hide_reversal() -> None:
    route = [
        QPointF(
            0.0,
            0.0,
        ),
        QPointF(
            40.0,
            0.0,
        ),
        QPointF(
            10.0,
            0.0,
        ),
    ]

    simplified = (
        ConnectionRoutingEngine._simplify_route(
            route
        )
    )

    assert simplified == route


def test_grid_route_never_immediately_reverses() -> None:
    obstacles = [
        QRectF(
            180.0,
            80.0,
            80.0,
            140.0,
        ),
        QRectF(
            300.0,
            40.0,
            100.0,
            140.0,
        ),
    ]

    route = (
        ConnectionRoutingEngine.build_route(
            QPointF(
                100.0,
                150.0,
            ),
            QPointF(
                500.0,
                150.0,
            ),
            "right",
            "left",
            obstacles,
        )
    )

    assert not (
        ConnectionRoutingEngine._has_immediate_uturn(
            route
        )
    )


def test_endpoint_nodes_are_included_as_scene_obstacles() -> None:
    _application()

    scene = QGraphicsScene()

    start_node = QGraphicsRectItem(
        0.0,
        0.0,
        180.0,
        100.0,
    )

    end_node = QGraphicsRectItem(
        300.0,
        0.0,
        180.0,
        100.0,
    )

    scene.addItem(start_node)
    scene.addItem(end_node)

    start_port = QGraphicsEllipseItem(
        -3.0,
        -3.0,
        6.0,
        6.0,
        start_node,
    )

    start_port.port_id = "port-start"
    start_port._side = "right"

    end_port = QGraphicsEllipseItem(
        -3.0,
        -3.0,
        6.0,
        6.0,
        end_node,
    )

    end_port.port_id = "port-end"
    end_port._side = "left"

    connection = ConnectionGraphicsItem(
        connection=SimpleNamespace(
            id="connection-1",
            endpoint_a_id="port-start",
            endpoint_b_id="port-end",
        ),
        selection_callback=lambda *_: None,
    )

    scene.addItem(connection)

    obstacles = connection._collect_obstacles()

    assert len(obstacles) == 2


def test_connection_starts_pathfinding_at_fixed_stub_end() -> None:
    _application()

    scene = QGraphicsScene()

    start_node = QGraphicsRectItem(
        0.0,
        0.0,
        180.0,
        100.0,
    )

    end_node = QGraphicsRectItem(
        400.0,
        0.0,
        180.0,
        100.0,
    )

    blocking_node = QGraphicsRectItem(
        150.0,
        -20.0,
        100.0,
        140.0,
    )

    scene.addItem(start_node)
    scene.addItem(end_node)
    scene.addItem(blocking_node)

    start_port = QGraphicsEllipseItem(
        -3.0,
        -3.0,
        6.0,
        6.0,
        start_node,
    )

    start_port.port_id = "port-start"
    start_port._side = "right"

    end_port = QGraphicsEllipseItem(
        -3.0,
        -3.0,
        6.0,
        6.0,
        end_node,
    )

    end_port.port_id = "port-end"
    end_port._side = "left"

    connection = ConnectionGraphicsItem(
        connection=SimpleNamespace(
            id="connection-1",
            endpoint_a_id="port-start",
            endpoint_b_id="port-end",
        ),
        selection_callback=lambda *_: None,
    )

    scene.addItem(connection)

    connection.setLine(
        180.0,
        50.0,
        400.0,
        50.0,
    )

    path = connection.path()

    assert path.elementCount() >= 4

    first = path.elementAt(1)

    # Port is at x=180. The fixed right-facing stub ends at x=220.
    assert abs(
        first.x
        - 220.0
    ) < 0.001


def test_reported_endpoint_case_routes_around_controller_zone() -> None:
    sensor_zone = QRectF(
        -291.0,
        -379.0,
        180.0,
        100.0,
    ).adjusted(
        -ConnectionRoutingEngine.ROUTING_MARGIN,
        -ConnectionRoutingEngine.ROUTING_MARGIN,
        ConnectionRoutingEngine.ROUTING_MARGIN,
        ConnectionRoutingEngine.ROUTING_MARGIN,
    )

    controller_zone = QRectF(
        82.0,
        -372.0,
        180.0,
        100.0,
    ).adjusted(
        -ConnectionRoutingEngine.ROUTING_MARGIN,
        -ConnectionRoutingEngine.ROUTING_MARGIN,
        ConnectionRoutingEngine.ROUTING_MARGIN,
        ConnectionRoutingEngine.ROUTING_MARGIN,
    )

    sensor_port = QPointF(
        -111.0,
        -329.0,
    )

    controller_port = QPointF(
        262.0,
        -322.0,
    )

    sensor_stub, sensor_direction = (
        ConnectionRoutingEngine.build_endpoint_stub(
            sensor_port,
            "right",
        )
    )

    controller_stub, controller_direction = (
        ConnectionRoutingEngine.build_endpoint_stub(
            controller_port,
            "right",
        )
    )

    route = (
        ConnectionRoutingEngine.build_route(
            sensor_stub,
            controller_stub,
            sensor_direction,
            controller_direction,
            [
                sensor_zone,
                controller_zone,
            ],
        )
    )

    assert (
        ConnectionRoutingEngine.route_is_clear(
            route,
            [
                sensor_zone,
                controller_zone,
            ],
        )
    )


def test_unrelated_remote_component_does_not_change_graphics_route() -> None:
    _application()

    scene = QGraphicsScene()

    start_node = QGraphicsRectItem(
        0.0,
        0.0,
        180.0,
        100.0,
    )

    end_node = QGraphicsRectItem(
        400.0,
        0.0,
        180.0,
        100.0,
    )

    scene.addItem(start_node)
    scene.addItem(end_node)

    start_port = QGraphicsEllipseItem(
        -3.0,
        -3.0,
        6.0,
        6.0,
        start_node,
    )

    start_port.port_id = "port-start"
    start_port._side = "right"

    end_port = QGraphicsEllipseItem(
        -3.0,
        -3.0,
        6.0,
        6.0,
        end_node,
    )

    end_port.port_id = "port-end"
    end_port._side = "left"

    connection = ConnectionGraphicsItem(
        connection=SimpleNamespace(
            id="connection-1",
            endpoint_a_id="port-start",
            endpoint_b_id="port-end",
        ),
        selection_callback=lambda *_: None,
    )

    scene.addItem(connection)

    connection.setLine(
        180.0,
        50.0,
        400.0,
        50.0,
    )

    baseline_path = connection.path()

    remote_node = QGraphicsRectItem(
        1000.0,
        1000.0,
        180.0,
        100.0,
    )

    scene.addItem(
        remote_node,
    )

    connection.setLine(
        180.0,
        50.0,
        400.0,
        50.0,
    )

    assert connection.path() == baseline_path

def test_fixed_endpoint_route_does_not_backtrack_over_stub() -> None:
    from PySide6.QtCore import QPointF, QRectF

    from machine_builder.graphics.connection_routing import (
        ConnectionRoutingEngine,
    )

    start = QPointF(
        76.0,
        57.0,
    )

    end = QPointF(
        54.0,
        199.0,
    )

    obstacles = [
        QRectF(
            -160.0,
            -9.0,
            212.0,
            132.0,
        ),
        QRectF(
            -182.0,
            133.0,
            212.0,
            132.0,
        ),
    ]

    route = ConnectionRoutingEngine.build_route(
        start=start,
        end=end,
        start_direction="right",
        end_direction="right",
        obstacles=obstacles,
    )

    assert len(route) >= 2

    first = route[1]

    # The fixed sensor stub already traveled right to x=76.
    # The main route must not immediately travel back left across it.
    assert not (
        first.y() == start.y()
        and first.x() < start.x()
    )

def test_route_cleanup_removes_repeated_point_loop() -> None:
    from PySide6.QtCore import QPointF

    from machine_builder.graphics.connection_routing_pathfinder import (
        _clean_route_geometry,
    )

    route = [
        QPointF(0.0, 0.0),
        QPointF(40.0, 0.0),
        QPointF(40.0, 40.0),
        QPointF(0.0, 40.0),
        QPointF(0.0, 0.0),
        QPointF(0.0, 80.0),
    ]

    cleaned = _clean_route_geometry(
        route,
    )

    assert cleaned == [
        QPointF(0.0, 0.0),
        QPointF(0.0, 80.0),
    ]


def test_route_cleanup_removes_orthogonal_self_crossing() -> None:
    from PySide6.QtCore import QPointF

    from machine_builder.graphics.connection_routing_pathfinder import (
        _clean_route_geometry,
    )

    route = [
        QPointF(0.0, 0.0),
        QPointF(80.0, 0.0),
        QPointF(80.0, 80.0),
        QPointF(40.0, 80.0),
        QPointF(40.0, -20.0),
        QPointF(100.0, -20.0),
        QPointF(100.0, 100.0),
    ]

    cleaned = _clean_route_geometry(
        route,
    )

    for index in range(
        len(cleaned) - 2,
    ):
        for following in range(
            index + 2,
            len(cleaned) - 1,
        ):
            first_start = cleaned[index]
            first_end = cleaned[index + 1]
            second_start = cleaned[following]
            second_end = cleaned[following + 1]

            assert not (
                first_start.x() == first_end.x()
                and second_start.x() == second_end.x()
                and first_start.x() == second_start.x()
                and max(
                    min(
                        first_start.y(),
                        first_end.y(),
                    ),
                    min(
                        second_start.y(),
                        second_end.y(),
                    ),
                )
                <= min(
                    max(
                        first_start.y(),
                        first_end.y(),
                    ),
                    max(
                        second_start.y(),
                        second_end.y(),
                    ),
                )
            )

def test_build_route_returns_none_for_impossible_endpoint_geometry() -> None:
    from PySide6.QtCore import QPointF, QRectF

    from machine_builder.graphics.connection_routing import (
        ConnectionRoutingEngine,
    )

    route = ConnectionRoutingEngine.build_route(
        start=QPointF(
            -177.0,
            -12.0,
        ),
        end=QPointF(
            37.0,
            -12.0,
        ),
        start_direction="right",
        end_direction="right",
        obstacles=[
            QRectF(
                -413.0,
                -78.0,
                212.0,
                132.0,
            ),
            QRectF(
                -199.0,
                -78.0,
                212.0,
                132.0,
            ),
        ],
    )

    assert route is None

def test_route_does_not_enter_destination_stub_collinearly() -> None:
    from PySide6.QtCore import QPointF, QRectF

    from machine_builder.graphics.connection_routing import (
        ConnectionRoutingEngine,
    )

    route = ConnectionRoutingEngine.build_route(
        start=QPointF(
            -15.0,
            -92.0,
        ),
        end=QPointF(
            19.0,
            -289.0,
        ),
        start_direction="right",
        end_direction="right",
        obstacles=[
            QRectF(
                -251.0,
                -158.0,
                212.0,
                132.0,
            ),
            QRectF(
                -217.0,
                -355.0,
                212.0,
                132.0,
            ),
        ],
    )

    assert route is not None
    assert len(route) >= 2

    previous = route[-2]
    final = route[-1]

    # The destination stub points right. The main route must not arrive
    # horizontally from the left, because that would overlap the stub.
    assert not (
        abs(previous.y() - final.y()) < 0.001
        and final.x() > previous.x()
    )

def test_blocked_endpoint_escape_prefers_nearest_clear_direction() -> None:
    from PySide6.QtCore import QPointF, QRectF

    from machine_builder.graphics.connection_routing_endpoint import (
        build_endpoint_escape,
    )

    escape, direction = build_endpoint_escape(
        port_position=QPointF(
            0.0,
            0.0,
        ),
        side="right",
        obstacles=[
            QRectF(
                20.0,
                -5.0,
                20.0,
                35.0,
            ),
        ],
        stub_length=40.0,
        escape_clearance=1.0,
        ignored_obstacles=[],
    )

    assert direction == "right"
    assert escape[-1] == QPointF(
        40.0,
        -6.0,
    )


def test_blocked_endpoint_escape_hysteresis_holds_previous_direction() -> None:
    from PySide6.QtCore import QPointF, QRectF

    from machine_builder.graphics.connection_routing_endpoint import (
        build_endpoint_escape,
    )

    kwargs = {
        "port_position": QPointF(
            0.0,
            0.0,
        ),
        "side": "right",
        "obstacles": [
            QRectF(
                20.0,
                -5.0,
                20.0,
                35.0,
            ),
        ],
        "stub_length": 40.0,
        "escape_clearance": 1.0,
        "ignored_obstacles": [],
        "preferred_escape_direction": "down",
        "escape_hysteresis_ratio": 0.20,
        "escape_hysteresis_distance": 24.0,
    }

    held, _ = build_endpoint_escape(
        **kwargs,
        allow_escape_reselection=False,
    )

    switched, _ = build_endpoint_escape(
        **kwargs,
        allow_escape_reselection=True,
    )

    assert held[-1] == QPointF(
        40.0,
        31.0,
    )

    assert switched[-1] == QPointF(
        40.0,
        -6.0,
    )

