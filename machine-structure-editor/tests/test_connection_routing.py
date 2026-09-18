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
            len(route) - 1
        )
    ]


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

    assert direction == "horizontal"


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

    assert direction == "horizontal"


def test_unobstructed_route_uses_orthogonal_segments() -> None:
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
            "horizontal",
            "horizontal",
            [],
        )
    )

    assert len(route) == 3

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
            "horizontal",
            "horizontal",
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
            "horizontal",
            "horizontal",
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
            "horizontal",
            "horizontal",
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


def test_endpoint_nodes_are_included_as_obstacles() -> None:
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

    scene.addItem(
        start_node
    )

    scene.addItem(
        end_node
    )

    start_port = QGraphicsEllipseItem(
        -3.0,
        -3.0,
        6.0,
        6.0,
        start_node,
    )

    start_port.port_id = (
        "port-start"
    )

    start_port._side = "right"

    end_port = QGraphicsEllipseItem(
        -3.0,
        -3.0,
        6.0,
        6.0,
        end_node,
    )

    end_port.port_id = (
        "port-end"
    )

    end_port._side = "left"

    connection = ConnectionGraphicsItem(
        connection=SimpleNamespace(
            id="connection-1",
            endpoint_a_id="port-start",
            endpoint_b_id="port-end",
        ),
        selection_callback=lambda *_: None,
    )

    scene.addItem(
        connection
    )

    obstacles = (
        connection._collect_obstacles()
    )

    assert len(obstacles) == 2

    start_expected = (
        start_node.sceneBoundingRect().adjusted(
            -ConnectionRoutingEngine.ROUTING_MARGIN,
            -ConnectionRoutingEngine.ROUTING_MARGIN,
            ConnectionRoutingEngine.ROUTING_MARGIN,
            ConnectionRoutingEngine.ROUTING_MARGIN,
        )
    )

    end_expected = (
        end_node.sceneBoundingRect().adjusted(
            -ConnectionRoutingEngine.ROUTING_MARGIN,
            -ConnectionRoutingEngine.ROUTING_MARGIN,
            ConnectionRoutingEngine.ROUTING_MARGIN,
            ConnectionRoutingEngine.ROUTING_MARGIN,
        )
    )

    assert any(
        rect == start_expected
        for rect in obstacles
    )

    assert any(
        rect == end_expected
        for rect in obstacles
    )


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