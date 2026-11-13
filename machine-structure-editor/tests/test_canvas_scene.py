"""Tests for canvas scene synchronization."""

from __future__ import annotations

import sys
from types import SimpleNamespace

import pytest
from PySide6.QtCore import QPointF
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsScene,
)

from machine_builder.canvas_scene import (
    CanvasSceneController,
)
from machine_builder.semantic_harness import Harness
from machine_builder.visual_model import (
    VisualConnection,
    VisualModel,
    VisualNode,
    VisualPort,
)


def _application() -> QApplication:
    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    return app


class SceneCanvasStub:
    """Minimal canvas surface required by CanvasSceneController."""

    def __init__(
        self,
    ) -> None:
        self.scene = QGraphicsScene()
        self._node_items = {}
        self._connection_items = {}
        self._synchronizing_scene = False

        self.store = type(
            "StoreStub",
            (),
            {
                "model": VisualModel(),
            },
        )()

        self.port_edit_requests: list[
            str
        ] = []

    def _begin_node_move(
        self,
        node_id,
    ):
        pass

    def _finish_node_move(
        self,
        node_id,
    ):
        pass

    def _node_selected(
        self,
        node_id,
        selected,
    ):
        pass

    def _focus_node(
        self,
        node_id,
    ):
        pass

    def _node_position_changed(
        self,
        node_id,
    ):
        pass

    def _start_connection_drag(
        self,
        port_id,
        scene_position,
    ):
        pass

    def _move_connection_drag(
        self,
        port_id,
        scene_position,
    ):
        pass

    def _finish_connection_drag(
        self,
        port_id,
        scene_position,
    ):
        pass

    def _connection_selected(
        self,
        connection_id,
        selected,
    ):
        pass

    def _edit_semantic_port(
        self,
        port_id,
    ):
        self.port_edit_requests.append(
            port_id
        )


def test_scene_controller_syncs_nodes() -> None:
    _application()

    canvas = SceneCanvasStub()
    controller = CanvasSceneController(
        canvas
    )

    node = VisualNode(
        id="node-1",
        node_type="motor",
        label="Motor",
        x=100,
        y=200,
    )

    canvas.store.model.add_node(
        node
    )

    controller.synchronize(
        canvas.store.model
    )

    assert "node-1" in canvas._node_items
    assert len(
        canvas.scene.items()
    ) >= 1


def test_scene_controller_removes_deleted_nodes() -> None:
    _application()

    canvas = SceneCanvasStub()
    controller = CanvasSceneController(
        canvas
    )

    node = VisualNode(
        id="node-1",
        node_type="motor",
        label="Motor",
    )

    canvas.store.model.add_node(
        node
    )

    controller.synchronize(
        canvas.store.model
    )

    assert "node-1" in canvas._node_items

    del canvas.store.model.nodes[
        "node-1"
    ]

    controller.synchronize(
        canvas.store.model
    )

    assert (
        "node-1"
        not in canvas._node_items
    )


def test_scene_controller_finds_rendered_port() -> None:
    _application()

    canvas = SceneCanvasStub()
    controller = CanvasSceneController(
        canvas
    )

    node = VisualNode(
        id="node-1",
        node_type="motor",
        label="Motor",
    )

    node.add_port(
        VisualPort(
            id="port-1",
            node_id="node-1",
            label="Power",
            port_type="power",
            direction="input",
            side="left",
            order=0,
        )
    )

    canvas.store.model.add_node(
        node
    )

    controller.synchronize(
        canvas.store.model
    )

    port_item = (
        controller.find_port_graphics_item(
            "port-1"
        )
    )

    assert port_item is not None
    assert port_item.port_id == "port-1"


def test_scene_controller_syncs_connections() -> None:
    _application()

    canvas = SceneCanvasStub()
    controller = CanvasSceneController(
        canvas
    )

    node_a = VisualNode(
        id="node-a",
        node_type="motor",
        label="Motor A",
        x=100,
        y=100,
    )

    node_b = VisualNode(
        id="node-b",
        node_type="controller",
        label="Controller",
        x=400,
        y=100,
    )

    node_a.add_port(
        VisualPort(
            id="port-a",
            node_id="node-a",
            label="Signal",
            port_type="signal",
            direction="output",
            side="right",
            order=0,
        )
    )

    node_b.add_port(
        VisualPort(
            id="port-b",
            node_id="node-b",
            label="Signal",
            port_type="signal",
            direction="input",
            side="left",
            order=0,
        )
    )

    canvas.store.model.add_node(
        node_a
    )

    canvas.store.model.add_node(
        node_b
    )

    connection = VisualConnection(
        id="connection-1",
        endpoint_a_id="port-a",
        endpoint_b_id="port-b",
    )

    canvas.store.model.add_connection(
        connection
    )

    controller.synchronize(
        canvas.store.model
    )

    assert (
        "connection-1"
        in canvas._connection_items
    )


def test_scene_controller_removes_deleted_connections() -> None:
    _application()

    canvas = SceneCanvasStub()
    controller = CanvasSceneController(
        canvas
    )

    node_a = VisualNode(
        id="node-a",
        node_type="motor",
        label="Motor A",
    )

    node_b = VisualNode(
        id="node-b",
        node_type="controller",
        label="Controller",
    )

    node_a.add_port(
        VisualPort(
            id="port-a",
            node_id="node-a",
            label="Signal",
            port_type="signal",
            direction="output",
            side="right",
            order=0,
        )
    )

    node_b.add_port(
        VisualPort(
            id="port-b",
            node_id="node-b",
            label="Signal",
            port_type="signal",
            direction="input",
            side="left",
            order=0,
        )
    )

    canvas.store.model.add_node(
        node_a
    )

    canvas.store.model.add_node(
        node_b
    )

    canvas.store.model.add_connection(
        VisualConnection(
            id="connection-1",
            endpoint_a_id="port-a",
            endpoint_b_id="port-b",
        )
    )

    controller.synchronize(
        canvas.store.model
    )

    assert (
        "connection-1"
        in canvas._connection_items
    )

    del canvas.store.model.connections[
        "connection-1"
    ]

    controller.synchronize(
        canvas.store.model
    )

    assert (
        "connection-1"
        not in canvas._connection_items
    )

def test_preview_updates_both_endpoint_stubs_when_bundle_moves():
    from types import SimpleNamespace

    from PySide6.QtCore import QPointF
    from PySide6.QtWidgets import QGraphicsPathItem

    _application()
    canvas = SceneCanvasStub()
    controller = CanvasSceneController(canvas)

    class EndpointNode:
        def __init__(self, semantic_id, origin, anchor):
            self._visual_ports = {
                semantic_id + "-visual": SimpleNamespace(
                    semantic_reference=semantic_id
                )
            }
            self._connector_group_contact_anchors_local = {
                semantic_id: QPointF(*anchor)
            }
            self.positions = {
                "origin": QPointF(*origin),
                "anchor": QPointF(*anchor),
            }

        def connector_group_contact_origin_for_port(self, semantic_id):
            return QPointF(self.positions["origin"])

        def connector_group_anchor_for_port(self, semantic_id):
            return QPointF(self.positions["anchor"])

    class EndpointPort:
        def __init__(self, port_id, node):
            self.port_id = port_id
            self._node = node

        def parentItem(self):
            return self._node

    endpoint_data = {
        "contact-port": (
            "contact-semantic",
            (10.0, 20.0),
            (30.0, 40.0),
            (15.0, 25.0),
            (35.0, 45.0),
        ),
        "terminal-port": (
            "terminal-semantic",
            (210.0, 220.0),
            (190.0, 200.0),
            (215.0, 225.0),
            (195.0, 205.0),
        ),
    }

    endpoint_items = {}
    endpoint_nodes = {}
    stubs = {}

    for endpoint_id, (
        semantic_id,
        origin,
        anchor,
        _moved_origin,
        _moved_anchor,
    ) in endpoint_data.items():
        node = EndpointNode(semantic_id, origin, anchor)
        endpoint_nodes[endpoint_id] = node
        endpoint_items[endpoint_id] = EndpointPort(
            semantic_id + "-visual", node
        )

        stub = QGraphicsPathItem()
        canvas.scene.addItem(stub)
        controller._connector_wire_stub_items[
            ("connection-1", endpoint_id)
        ] = stub
        stubs[endpoint_id] = stub

    controller.find_port_graphics_item = (
        lambda endpoint_id: endpoint_items.get(endpoint_id)
    )

    def assert_stub_matches(endpoint_id, origin, anchor):
        stub = stubs[endpoint_id]
        path = stub.path()
        actual_start = stub.mapToScene(path.pointAtPercent(0.0))
        actual_end = stub.mapToScene(path.pointAtPercent(1.0))

        assert abs(actual_start.x() - origin[0]) <= 1e-6
        assert abs(actual_start.y() - origin[1]) <= 1e-6
        assert abs(actual_end.x() - anchor[0]) <= 1e-6
        assert abs(actual_end.y() - anchor[1]) <= 1e-6

    for endpoint_id, (
        _semantic_id,
        origin,
        anchor,
        _moved_origin,
        _moved_anchor,
    ) in endpoint_data.items():
        controller._update_preview_endpoint_stub(
            "connection-1", endpoint_id
        )
        assert_stub_matches(endpoint_id, origin, anchor)

    # Simulate both physical endpoint nodes moving during the same drag.
    for endpoint_id, (
        _semantic_id,
        _origin,
        _anchor,
        moved_origin,
        moved_anchor,
    ) in endpoint_data.items():
        endpoint_nodes[endpoint_id].positions["origin"] = QPointF(*moved_origin)
        endpoint_nodes[endpoint_id].positions["anchor"] = QPointF(*moved_anchor)

    for endpoint_id, (
        _semantic_id,
        _origin,
        _anchor,
        moved_origin,
        moved_anchor,
    ) in endpoint_data.items():
        controller._update_preview_endpoint_stub(
            "connection-1", endpoint_id
        )
        assert_stub_matches(endpoint_id, moved_origin, moved_anchor)
def test_bundle_preview_uses_motor_connector_cone_tip_when_available():
    from types import SimpleNamespace

    from PySide6.QtCore import QPointF

    _application()
    canvas = SceneCanvasStub()
    controller = CanvasSceneController(canvas)

    class EndpointNode:
        def __init__(self, node_id, visual_id, semantic_id, cone_tip):
            self.node_id = node_id
            self._visual_ports = {
                visual_id: SimpleNamespace(semantic_reference=semantic_id)
            }
            self.cone_tip = QPointF(*cone_tip)
            self.anchor_requests = []

        def connector_group_anchor_for_port(self, semantic_id):
            self.anchor_requests.append(semantic_id)
            return QPointF(self.cone_tip)

    class EndpointItem:
        def __init__(self, port_id, node, position):
            self.port_id = port_id
            self._node = node
            self._position = QPointF(*position)

        def parentItem(self):
            return self._node

        def scenePos(self):
            return QPointF(self._position)

    contact_node = EndpointNode(
        "controller-node", "contact-visual", "contact-semantic", (30.0, 40.0)
    )
    terminal_node = EndpointNode(
        "motor-node", "terminal-visual", "terminal-semantic", (190.0, 200.0)
    )
    endpoint_items = {
        "contact-port": EndpointItem(
            "contact-visual", contact_node, (15.0, 25.0)
        ),
        "terminal-port": EndpointItem(
            "terminal-visual", terminal_node, (210.0, 220.0)
        ),
    }
    controller.find_port_graphics_item = (
        lambda endpoint_id: endpoint_items.get(endpoint_id)
    )
    canvas.store.model.connections["connection-1"] = SimpleNamespace(
        endpoint_a_id="contact-port",
        endpoint_b_id="terminal-port",
    )
    canvas.store.semantic_model = SimpleNamespace(
        ports={
            "contact-semantic": SimpleNamespace(
                controller_id="controller-1",
                connector_id="J9",
                pin_id="1",
                properties={},
            ),
            "terminal-semantic": SimpleNamespace(
                component_id="motor-1",
                properties={
                    "interface_role": "motor_conductor_terminal",
                    "interface_granularity": "physical_terminal",
                },
            ),
        }
    )

    details = controller._connection_routing_bundle_preview_details(
        "connection-1"
    )

    assert details is not None
    assert details["contact_position"] == contact_node.cone_tip
    assert details["terminal_position"] == terminal_node.cone_tip
    assert terminal_node.anchor_requests == ["terminal-semantic"]


def _make_harness_ordering_controller(
    connection_ids,
    member_ids,
    physical_members,
    *,
    child_members=None,
    parent_child_ids=None,
    missing_layer=None,
    missing_member_id=None,
):
    _application()
    canvas = SceneCanvasStub()
    controller = CanvasSceneController(canvas)

    for connection_id in connection_ids:
        if not (
            missing_layer == "visual"
            and connection_id == missing_member_id
        ):
            canvas._connection_items[connection_id] = object()

        if not (
            missing_layer == "model"
            and connection_id == missing_member_id
        ):
            canvas.store.model.connections[connection_id] = object()

    semantic_connections = {
        connection_id: object()
        for connection_id in connection_ids
        if not (
            missing_layer == "semantic"
            and connection_id == missing_member_id
        )
    }

    harnesses = {}
    if member_ids is not None:
        harnesses["harness-main"] = Harness(
            id="harness-main",
            name="Main harness",
            member_connection_ids=list(member_ids),
            child_harness_ids=list(parent_child_ids or []),
        )

    for child_id, child_member_ids in (child_members or {}).items():
        harnesses[child_id] = Harness(
            id=child_id,
            name="Child harness",
            member_connection_ids=list(child_member_ids),
        )

    canvas.store.semantic_model = SimpleNamespace(
        connections=semantic_connections,
        harnesses=harnesses,
        validate_harnesses=lambda: None,
    )

    member_lookup = physical_members or {}
    controller._connection_routing_bundle_member = (
        lambda connection_id: member_lookup.get(connection_id)
    )
    return controller


def _physical_bundle_members_with_opposed_id_and_lane_order():
    key = ("controller-1", "connector-1", "motor-1")
    return {
        "wire-z": (key, QPointF(0.0, 30.0), QPointF(100.0, 30.0)),
        "wire-c": (key, QPointF(0.0, 20.0), QPointF(100.0, 20.0)),
        "wire-a": (key, QPointF(0.0, 10.0), QPointF(100.0, 10.0)),
    }


def test_ordered_connection_items_groups_explicit_direct_harness_members():
    connection_ids = [
        "wire-z",
        "wire-c",
        "wire-a",
        "wire-independent",
    ]
    controller = _make_harness_ordering_controller(
        connection_ids,
        ["wire-z", "wire-c", "wire-a"],
        _physical_bundle_members_with_opposed_id_and_lane_order(),
    )

    ordered_ids = [
        connection_id
        for connection_id, _graphics in controller._ordered_connection_items()
    ]

    assert ordered_ids == [
        "wire-z",
        "wire-c",
        "wire-a",
        "wire-independent",
    ]


def test_ordered_connection_items_does_not_infer_membership_from_shared_endpoints():
    connection_ids = ["wire-a", "wire-c", "wire-independent", "wire-z"]
    controller = _make_harness_ordering_controller(
        connection_ids,
        None,
        _physical_bundle_members_with_opposed_id_and_lane_order(),
    )

    ordered_ids = [
        connection_id
        for connection_id, _graphics in controller._ordered_connection_items()
    ]

    assert ordered_ids == sorted(connection_ids)


@pytest.mark.parametrize("missing_layer", ["visual", "model", "semantic"])
def test_ordered_connection_items_rejects_partial_harness_membership(missing_layer):
    connection_ids = ["wire-z", "wire-c", "wire-a", "wire-independent"]
    controller = _make_harness_ordering_controller(
        connection_ids,
        ["wire-z", "wire-c", "wire-a"],
        _physical_bundle_members_with_opposed_id_and_lane_order(),
        missing_layer=missing_layer,
        missing_member_id="wire-z",
    )

    ordered_ids = [
        connection_id
        for connection_id, _graphics in controller._ordered_connection_items()
    ]
    expected_ids = sorted(
        connection_id
        for connection_id in connection_ids
        if not (
            missing_layer == "visual"
            and connection_id == "wire-z"
        )
    )

    assert ordered_ids == expected_ids


def test_ordered_connection_items_rejects_reversed_motor_lane_order():
    physical_members = _physical_bundle_members_with_opposed_id_and_lane_order()
    physical_members["wire-z"] = (
        ("controller-1", "connector-1", "motor-1"),
        QPointF(0.0, 30.0),
        QPointF(100.0, 10.0),
    )
    physical_members["wire-a"] = (
        ("controller-1", "connector-1", "motor-1"),
        QPointF(0.0, 10.0),
        QPointF(100.0, 30.0),
    )
    connection_ids = ["wire-a", "wire-c", "wire-z"]
    controller = _make_harness_ordering_controller(
        connection_ids, connection_ids, physical_members
    )

    ordered_ids = [
        connection_id
        for connection_id, _graphics in controller._ordered_connection_items()
    ]

    assert ordered_ids == sorted(connection_ids)


def test_ordered_connection_items_rejects_ambiguous_motor_lane_positions():
    physical_members = _physical_bundle_members_with_opposed_id_and_lane_order()
    physical_members["wire-a"] = (
        ("controller-1", "connector-1", "motor-1"),
        QPointF(0.0, 10.0),
        QPointF(100.0, 20.0),
    )
    physical_members["wire-c"] = (
        ("controller-1", "connector-1", "motor-1"),
        QPointF(0.0, 20.0),
        QPointF(100.0, 20.0),
    )
    connection_ids = ["wire-a", "wire-c", "wire-z"]
    controller = _make_harness_ordering_controller(
        connection_ids, connection_ids, physical_members
    )

    ordered_ids = [
        connection_id
        for connection_id, _graphics in controller._ordered_connection_items()
    ]

    assert ordered_ids == sorted(connection_ids)

def test_ordered_connection_items_rejects_physically_mismatched_harness_members():
    physical_members = _physical_bundle_members_with_opposed_id_and_lane_order()
    physical_members["wire-a"] = (
        ("controller-1", "different-connector", "motor-1"),
        QPointF(0.0, 10.0),
        QPointF(100.0, 10.0),
    )
    connection_ids = ["wire-a", "wire-c", "wire-z"]
    controller = _make_harness_ordering_controller(
        connection_ids,
        connection_ids,
        physical_members,
    )

    ordered_ids = [
        connection_id
        for connection_id, _graphics in controller._ordered_connection_items()
    ]

    assert ordered_ids == sorted(connection_ids)


def test_ordered_connection_items_does_not_flatten_parent_child_harnesses():
    connection_ids = [
        "wire-z",
        "wire-c",
        "wire-a",
        "wire-independent",
    ]
    controller = _make_harness_ordering_controller(
        connection_ids,
        ["wire-z", "wire-a"],
        _physical_bundle_members_with_opposed_id_and_lane_order(),
        parent_child_ids=["harness-branch"],
        child_members={"harness-branch": ["wire-c", "wire-independent"]},
    )

    ordered_ids = [
        connection_id
        for connection_id, _graphics in controller._ordered_connection_items()
    ]

    assert ordered_ids == sorted(connection_ids)


def _make_routing_priority_controller(physical_members):
    connection_ids = [
        "wire-a",
        "wire-c",
        "wire-independent-a",
        "wire-independent-b",
        "wire-z",
    ]
    return _make_harness_ordering_controller(
        connection_ids,
        None,
        physical_members,
    )


def _compatible_routing_priority_physical_members():
    key = ("controller-1", "connector-1", "motor-1")
    return {
        "wire-a": (key, QPointF(0.0, 10.0), QPointF(-100.0, 1.644)),
        "wire-c": (key, QPointF(0.0, 20.0), QPointF(-100.0, 11.644)),
        "wire-z": (key, QPointF(0.0, 30.0), QPointF(-100.0, 21.644)),
    }


def test_routing_ordered_connection_items_prioritizes_compatible_independent_lanes():
    controller = _make_routing_priority_controller(
        _compatible_routing_priority_physical_members()
    )

    original_ids = [
        connection_id
        for connection_id, _graphics in controller._ordered_connection_items()
    ]
    routing_ids = [
        connection_id
        for connection_id, _graphics in controller._routing_ordered_connection_items()
    ]

    assert controller.store.semantic_model.harnesses == {}
    assert original_ids == [
        "wire-a",
        "wire-c",
        "wire-independent-a",
        "wire-independent-b",
        "wire-z",
    ]
    assert routing_ids == [
        "wire-z",
        "wire-c",
        "wire-independent-a",
        "wire-independent-b",
        "wire-a",
    ]


def test_routing_ordered_connection_items_preserves_unrelated_slots():
    controller = _make_routing_priority_controller(
        _compatible_routing_priority_physical_members()
    )

    original = controller._ordered_connection_items()
    routed = controller._routing_ordered_connection_items()

    assert len(routed) == len(original)

    for index, (connection_id, graphics) in enumerate(original):
        if connection_id.startswith("wire-independent-"):
            assert routed[index][0] == connection_id
            assert routed[index][1] is graphics

    assert {
        connection_id: graphics
        for connection_id, graphics in routed
    } == {
        connection_id: graphics
        for connection_id, graphics in original
    }


def test_routing_ordered_connection_items_rejects_reversed_lanes():
    key = ("controller-1", "connector-1", "motor-1")
    physical_members = {
        "wire-a": (key, QPointF(0.0, 10.0), QPointF(100.0, 30.0)),
        "wire-c": (key, QPointF(0.0, 20.0), QPointF(100.0, 20.0)),
        "wire-z": (key, QPointF(0.0, 30.0), QPointF(100.0, 10.0)),
    }
    controller = _make_routing_priority_controller(physical_members)

    original_ids = [
        connection_id
        for connection_id, _graphics in controller._ordered_connection_items()
    ]
    routing_ids = [
        connection_id
        for connection_id, _graphics in controller._routing_ordered_connection_items()
    ]

    assert routing_ids == original_ids


def test_routing_ordered_connection_items_rejects_ambiguous_lanes():
    key = ("controller-1", "connector-1", "motor-1")
    physical_members = {
        "wire-a": (key, QPointF(0.0, 10.0), QPointF(100.0, 10.0)),
        "wire-c": (key, QPointF(0.0, 10.0), QPointF(100.0, 20.0)),
        "wire-z": (key, QPointF(0.0, 30.0), QPointF(100.0, 20.0)),
    }
    controller = _make_routing_priority_controller(physical_members)

    original_ids = [
        connection_id
        for connection_id, _graphics in controller._ordered_connection_items()
    ]
    routing_ids = [
        connection_id
        for connection_id, _graphics in controller._routing_ordered_connection_items()
    ]

    assert routing_ids == original_ids
def test_synchronize_clears_active_node_preview_before_rebuilding_scene():
    from types import SimpleNamespace

    from PySide6.QtWidgets import QGraphicsPathItem

    _application()
    canvas = SceneCanvasStub()
    controller = CanvasSceneController(canvas)

    canvas._active_node_drag = SimpleNamespace(
        node_ids=("node-1",),
        start_positions={"node-1": (0.0, 0.0)},
    )

    original_wire = QGraphicsPathItem()
    canvas.scene.addItem(original_wire)
    original_wire.setVisible(False)

    preview = QGraphicsPathItem()
    canvas.scene.addItem(preview)

    stale_stub = QGraphicsPathItem()
    canvas.scene.addItem(stale_stub)

    controller._drag_preview_items[
        ("controller-1", "J9", "motor-1")
    ] = preview
    controller._drag_preview_hidden_connections["connection-1"] = (
        original_wire,
        True,
    )
    controller._connector_wire_stub_items[
        ("connection-1", "contact-port")
    ] = stale_stub

    controller.request_node_move_preview()
    assert controller._drag_preview_timer.isActive()

    controller.synchronize(VisualModel())

    assert canvas._active_node_drag is None
    assert not controller._drag_preview_timer.isActive()
    assert original_wire.isVisible()
    assert original_wire.scene() is canvas.scene
    assert preview.scene() is None
    assert stale_stub.scene() is None
    assert controller._drag_preview_items == {}
    assert controller._drag_preview_hidden_connections == {}
    assert controller._connector_wire_stub_items == {}
def test_failed_node_move_preview_keeps_individual_conductors_visible(monkeypatch):
    from types import SimpleNamespace

    from PySide6.QtCore import QPointF
    from PySide6.QtWidgets import QGraphicsPathItem

    from machine_builder.graphics.connection_routing import ConnectionRoutingEngine

    _application()
    canvas = SceneCanvasStub()
    controller = CanvasSceneController(canvas)

    canvas._active_node_drag = SimpleNamespace(
        node_ids=("moving-node",),
        start_positions={"moving-node": (0.0, 0.0)},
    )

    connection = SimpleNamespace(
        endpoint_a_id="contact-port",
        endpoint_b_id="terminal-port",
    )
    canvas.store.model.connections["connection-1"] = connection

    original_wire = QGraphicsPathItem()
    canvas.scene.addItem(original_wire)
    original_wire.setVisible(False)

    old_preview = QGraphicsPathItem()
    canvas.scene.addItem(old_preview)

    bundle_key = ("controller-1", "J9", "motor-1")
    controller._drag_preview_items[bundle_key] = old_preview
    controller._drag_preview_hidden_connections["connection-1"] = (
        original_wire,
        True,
    )

    class PreparedConnection:
        endpoint_a_id = "contact-port"
        endpoint_b_id = "terminal-port"

        def __init__(self):
            self._endpoint_route_fanout_offsets = {}
            self._endpoint_route_stub_lengths = {}
            self._overlap_escape_state = {}

        def set_endpoint_route_fanout_offsets(self, offsets):
            self._endpoint_route_fanout_offsets = dict(offsets)

        def set_endpoint_route_stub_lengths(self, lengths):
            self._endpoint_route_stub_lengths = dict(lengths)

        def _prepare_line_geometry(self, x1, y1, x2, y2):
            return {
                "start": QPointF(x1, y1),
                "end": QPointF(x2, y2),
                "start_route_position": QPointF(x1, y1),
                "end_route_position": QPointF(x2, y2),
                "obstacles": [],
                "start_escape": [QPointF(x1, y1)],
                "start_direction": "right",
                "end_escape": [QPointF(x2, y2)],
                "end_direction": "left",
            }

        def _find_endpoint_node(self, endpoint_id):
            return None

    graphics = PreparedConnection()
    canvas._connection_items["connection-1"] = graphics

    details = {
        "key": bundle_key,
        "contact_endpoint_id": "contact-port",
        "terminal_endpoint_id": "terminal-port",
        "contact_position": QPointF(0.0, 0.0),
        "terminal_position": QPointF(100.0, 0.0),
        "contact_node_id": "moving-node",
        "terminal_node_id": "stationary-node",
    }
    controller._connection_routing_bundle_preview_details = (
        lambda connection_id: details
    )

    monkeypatch.setattr(
        ConnectionRoutingEngine,
        "build_route",
        staticmethod(lambda **kwargs: None),
    )

    controller._update_node_move_preview()

    assert original_wire.isVisible()
    assert original_wire.scene() is canvas.scene
    assert old_preview.scene() is None
    assert controller._drag_preview_items == {}
    assert controller._drag_preview_hidden_connections == {}
