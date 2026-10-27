from PySide6.QtCore import QPoint, QPointF
from PySide6.QtGui import QPainterPath
from PySide6.QtWidgets import QApplication, QGraphicsScene

from machine_builder.graphics.connection import ConnectionGraphicsItem
from machine_builder.graphics.view import MachineGraphicsView
from machine_builder.visual_model import VisualConnection


def _make_connection_item(connection_id: str = "test-wire"):
    connection = VisualConnection(
        id=connection_id,
        endpoint_a_id=f"{connection_id}-port-a",
        endpoint_b_id=f"{connection_id}-port-b",
        connection_type="electrical",
    )
    return ConnectionGraphicsItem(
        connection=connection,
        selection_callback=lambda *_args: None,
    )


def test_wire_color_uses_the_supplied_physical_color():
    item = _make_connection_item()
    item.set_wire_color("Red")

    assert item.pen().color().name() == "#ff0000"


def test_hex_wire_color_is_supported():
    item = _make_connection_item()
    item.set_wire_color("#008000")

    assert item.pen().color().name() == "#008000"


def test_unknown_wire_color_falls_back_to_neutral_gray():
    item = _make_connection_item()
    item.set_wire_color("not-a-valid-color")

    assert item.pen().color().name() == item.NORMAL_COLOR.name()


def test_wire_hit_area_is_wider_than_the_visible_stroke():
    item = _make_connection_item()
    path = QPainterPath()
    path.moveTo(0.0, 0.0)
    path.lineTo(100.0, 0.0)
    item.setPath(path)

    assert item.shape().contains(QPointF(40.0, 6.0))
    assert not item.shape().contains(QPointF(40.0, 8.0))
    assert item.boundingRect().contains(QPointF(40.0, 7.0))


def test_overlapping_wires_can_be_selected_by_repeated_clicks():
    app = QApplication.instance() or QApplication([])
    scene = QGraphicsScene()
    first = _make_connection_item("first-wire")
    second = _make_connection_item("second-wire")
    path = QPainterPath()
    path.moveTo(0.0, 0.0)
    path.lineTo(100.0, 0.0)
    first.setPath(path)
    second.setPath(path)
    scene.addItem(first)
    scene.addItem(second)

    point = QPointF(40.0, 0.0)
    viewport_point = QPoint(40, 0)
    top_to_bottom = [
        item
        for item in scene.items(point)
        if isinstance(item, ConnectionGraphicsItem)
    ]
    assert len(top_to_bottom) == 2

    view = MachineGraphicsView(scene, canvas=object())
    assert view._select_overlapping_connection_at(point, viewport_point)
    assert scene.selectedItems() == [top_to_bottom[0]]
    assert view._select_overlapping_connection_at(point, viewport_point)
    assert scene.selectedItems() == [top_to_bottom[1]]
