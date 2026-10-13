from __future__ import annotations

from copy import deepcopy

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication

from machine_builder import canvas_interaction
from machine_builder.canvas import MachineCanvas
from machine_builder.compatibility import CompatibilityResult
from machine_builder.controller_visual_mutations import CreateDuet2MaestroControllerNode
from machine_builder.mutations import CreateNode
from machine_builder.persistence import load_editor_state
from machine_builder.promega_fixtures import _xy_motor_board_contact_ports
from machine_builder.visual_model import VisualNode


_APP = None


def _app():
    global _APP
    _APP = QApplication.instance() or QApplication([])
    return _APP


def _make_canvas():
    _app()
    canvas = MachineCanvas()
    controller_node = VisualNode(
        id="maestro-node",
        node_type="controller",
        label="Duet 2 Maestro",
        x=450.0,
        y=100.0,
    )
    canvas.store.commit(
        CreateDuet2MaestroControllerNode(
            node=controller_node,
            controller_id="test-maestro",
        )
    )

    motor_node = VisualNode(
        id="x-motor-node",
        node_type="motor",
        label="X motor",
        x=100.0,
        y=100.0,
    )
    canvas.store.commit(CreateNode(node=motor_node))
    return canvas, controller_node, motor_node, "test-maestro"


def _visual_port(node, semantic_port_id):
    matches = [
        port for port in node.ports.values()
        if port.semantic_reference == semantic_port_id
    ]
    assert len(matches) == 1
    return matches[0]


def _focus(canvas, controller_id, connector_id, mode):
    key = f"{controller_id}::{connector_id}::{mode}"
    combo = canvas.controller_connector_focus_combo
    indexes = [
        index for index in range(combo.count())
        if combo.itemData(index) == key
    ]
    assert len(indexes) == 1
    combo.setCurrentIndex(indexes[0])


def test_interface_focus_preserves_contacts_and_persistence(tmp_path):
    canvas, controller_node, motor_node, controller_id = _make_canvas()
    model = canvas.store.semantic_model
    motor_component_id = motor_node.semantic_reference
    assert motor_component_id is not None

    group_id = f"{controller_id}-x-motor-interface"
    motor_port_id = f"{motor_component_id}-motor-electrical-interface"
    group_port = model.ports[group_id]
    motor_port = model.ports[motor_port_id]

    assert group_port.component_id is None
    assert group_port.controller_id == controller_id
    assert (group_port.connector_id, group_port.pin_id) == ("x-motor", None)
    assert group_port.properties["interface_granularity"] == "connector_level"
    assert group_port.properties["contact_mapping_status"] == "not_established"
    assert group_port.provenance

    assert motor_port.component_id == motor_component_id
    assert motor_port.controller_id is None
    assert motor_port.connector_id is None
    assert motor_port.pin_id is None
    assert motor_port.properties["interface_role"] == "motor_electrical_interface"
    assert motor_port.provenance

    contact_ids = {
        f"{controller_id}-x-motor-pin-{position}"
        for position in range(1, 5)
    }
    assert contact_ids.issubset(model.ports)
    assert {
        port.id
        for port in _xy_motor_board_contact_ports(
            canvas, controller_id, "x-motor"
        ).values()
    } == contact_ids

    ports_before = deepcopy(model.ports)
    connections_before = deepcopy(model.connections)
    visuals_before = deepcopy(canvas.store.model.connections)
    undo_depth = len(canvas.store._undo_stack)
    redo_depth = len(canvas.store._redo_stack)
    modified_before = canvas.store.is_modified

    controller_graphics = canvas._node_items[controller_node.id]
    group_visual = _visual_port(controller_node, group_id)
    motor_visual = _visual_port(motor_node, motor_port_id)

    assert canvas.controller_connector_focus_combo.currentData() == ""
    assert controller_graphics._port_items[group_visual.id].isVisible()
    assert canvas._node_items[motor_node.id]._port_items[motor_visual.id].isVisible()

    contacts = {
        port_id: _visual_port(controller_node, port_id)
        for port_id in contact_ids
    }
    assert all(
        not controller_graphics._port_items[port.id].isVisible()
        for port in contacts.values()
    )

    _focus(canvas, controller_id, "x-motor", "contacts")
    assert not controller_graphics._port_items[group_visual.id].isVisible()
    contact_items = [
        controller_graphics._port_items[port.id]
        for port in contacts.values()
    ]
    assert all(item.isVisible() for item in contact_items)
    assert controller_graphics.rect().height() >= 48.0 + 34.0 * 4
    ys = sorted(item.pos().y() for item in contact_items)
    assert all(right - left >= 30.0 for left, right in zip(ys, ys[1:]))

    _focus(canvas, controller_id, "z-probe", "contacts")
    _focus(canvas, controller_id, "x-motor", "contacts")
    canvas.controller_connector_focus_combo.setCurrentIndex(0)

    assert model.ports == ports_before
    assert model.connections == connections_before
    assert canvas.store.model.connections == visuals_before
    assert len(canvas.store._undo_stack) == undo_depth
    assert len(canvas.store._redo_stack) == redo_depth
    assert canvas.store.is_modified == modified_before

    save_path = tmp_path / "functional-interface.machine.json"
    canvas.store.save(save_path)
    restored = load_editor_state(save_path)
    assert restored.semantic_model.ports == ports_before
    assert restored.semantic_model.connections == connections_before
    assert restored.visual_model.connections == visuals_before


def test_interface_drag_creates_reference_scoped_connection(monkeypatch, tmp_path):
    canvas, controller_node, motor_node, controller_id = _make_canvas()
    motor_component_id = motor_node.semantic_reference
    assert motor_component_id is not None

    controller_port_id = f"{controller_id}-x-motor-interface"
    motor_port_id = f"{motor_component_id}-motor-electrical-interface"
    controller_visual = _visual_port(controller_node, controller_port_id)
    motor_visual = _visual_port(motor_node, motor_port_id)
    source_item = canvas._node_items[controller_node.id]._port_items[controller_visual.id]
    target_item = canvas._node_items[motor_node.id]._port_items[motor_visual.id]
    assert source_item.isVisible() and target_item.isVisible()

    class AcceptedDialog:
        class DialogCode:
            Accepted = 1

        def __init__(self, *args, **kwargs):
            pass

        def exec(self):
            return self.DialogCode.Accepted

        def result_data(self):
            return {"wire_color": None, "harness_id": None, "notes": None}

    monkeypatch.setattr(
        canvas_interaction,
        "PhysicalConnectionDetailsDialog",
        AcceptedDialog,
    )
    monkeypatch.setattr(
        canvas_interaction,
        "check_port_compatibility",
        lambda *_args: CompatibilityResult.COMPATIBLE,
    )
    monkeypatch.setattr(
        canvas._scene_controller,
        "find_port_graphics_at",
        lambda _position: target_item,
    )

    canvas._start_connection_drag(controller_visual.id, source_item.scenePos())
    canvas._finish_connection_drag(controller_visual.id, target_item.scenePos())

    assert len(canvas.store.semantic_model.connections) == 1
    connection = next(iter(canvas.store.semantic_model.connections.values()))
    assert {connection.endpoint_a_id, connection.endpoint_b_id} == {
        controller_port_id,
        motor_port_id,
    }
    assert connection.connection_type == "electrical"
    assert connection.properties["connection_scope"] == "functional_interface_reference"
    assert connection.properties["physical_wiring_status"] == "not_verified_as_built"
    assert connection.properties["contact_mapping_status"] == "not_established"
    assert connection.properties["firmware_assignment_status"] == "not_established"
    assert "not count it as an additional conductor path" in (
        connection.properties["refinement_policy"]
    )
    assert "direct connector mating" in connection.properties["notes"]
    assert any(
        item.method == "functional-interface reference connection"
        for item in connection.provenance
    )

    contact_ids = {
        f"{controller_id}-x-motor-pin-{position}"
        for position in range(1, 5)
    }
    assert not any(
        connection.connects_same_ports(controller_port_id, contact_id)
        for contact_id in contact_ids
        for connection in canvas.store.semantic_model.connections.values()
    )

    graphics_connection = canvas._connection_items[connection.id]
    assert graphics_connection.isVisible()
    _focus(canvas, controller_id, "x-motor", "contacts")
    assert not canvas._node_items[controller_node.id]._port_items[
        controller_visual.id
    ].isVisible()
    assert graphics_connection.isVisible()

    save_path = tmp_path / "functional-connection.machine.json"
    canvas.store.save(save_path)
    restored = load_editor_state(save_path)
    assert restored.semantic_model.connections[connection.id] == connection
    assert restored.semantic_model.ports[controller_port_id].properties[
        "interface_granularity"
    ] == "connector_level"
    assert contact_ids.issubset(restored.semantic_model.ports)


def test_generic_controller_has_explanatory_empty_state():
    _app()
    canvas = MachineCanvas()
    canvas.store.commit(
        CreateNode(
            node=VisualNode(
                id="generic-controller-node",
                node_type="controller",
                label="Controller",
                x=100.0,
                y=100.0,
            )
        )
    )
    assert canvas.store.model.nodes["generic-controller-node"].ports == {}
    assert canvas.controller_connector_focus_combo.count() == 1
    assert "generic Controller has no hardware-specific ports" in (
        canvas.controller_connector_focus_help.text()
    )