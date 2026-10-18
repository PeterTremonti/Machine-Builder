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
from machine_builder.promega_fixtures import (
    _xy_motor_board_contact_ports,
    add_promega_xy_motor_reference_connections,
)
from machine_builder.semantic_component_mutations import UpdateMachineComponent
from machine_builder.semantic_model import Provenance
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

    canvas.create_node_from_template(
        node_type="motor",
        scene_position=QPointF(100.0, 100.0),
    )
    motor_node = next(
        node
        for node in canvas.store.model.nodes.values()
        if node.node_type == "motor"
    )
    return canvas, controller_node, motor_node, "test-maestro"


def _create_reference_cable_component(canvas, role, position):
    """Create a synthetic cable-reference component for regression setup."""
    existing_node_ids = set(canvas.store.model.nodes)
    canvas.create_node_from_template("component", position)
    new_nodes = [
        node for node in canvas.store.model.nodes.values()
        if node.id not in existing_node_ids and node.node_type == "component"
    ]
    assert len(new_nodes) == 1
    component_id = new_nodes[0].semantic_reference
    assert component_id is not None

    component = canvas.store.semantic_model.components[component_id]
    evidence = Provenance(
        source="Machine Builder regression fixture",
        evidence_type="authored",
        method="synthetic test setup",
        context=f"{role} exists only to seed pre-existing contact connections.",
        date="2026-10-15",
        notes="Not evidence of installed hardware or as-built wiring.",
    )
    properties = dict(component.properties)
    properties.update({
        "specimen_scope": "promega_compound_reference",
        "physical_presence_status": "not_verified_as_built",
        "physical_wiring_status": "not_verified_as_built",
        "firmware_assignment_status": "not_established",
    })
    canvas.store.commit(
        UpdateMachineComponent(
            component_id=component_id,
            role=role,
            label=role,
            properties=properties,
            provenance_entries=list(component.provenance) + [evidence],
        )
    )
    return component_id


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
    motor_graphics = canvas._node_items[motor_node.id]
    assert motor_graphics._port_items[motor_visual.id].isVisible()
    motor_detail_ids = [
        port.id
        for port in motor_node.ports.values()
        if port.semantic_reference is None
    ]
    assert len(motor_detail_ids) == 2
    assert all(
        not motor_graphics._port_items[port_id].isVisible()
        for port_id in motor_detail_ids
    )

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
    assert controller_graphics._connector_group_box.isVisible()
    assert controller_graphics._connector_group_title.text() == "J9 / X Motor"
    assert not controller_graphics._connector_group_cone.isVisible()
    group_id = f"{controller_id}-x-motor-interface"
    assert controller_graphics.connector_group_anchor_for_port(group_id) is None

    for visual_port in contacts.values():
        semantic_port = model.ports[visual_port.semantic_reference]
        expected_label = (
            f"{semantic_port.properties['pin_label']} — {semantic_port.purpose}"
        )
        assert (
            controller_graphics._port_items[visual_port.id]._label_item.text()
            == expected_label
        )

    assert controller_graphics.rect().height() >= 48.0 + 34.0 * 4
    ys = sorted(item.pos().y() for item in contact_items)
    assert all(right - left >= 30.0 for left, right in zip(ys, ys[1:]))

    _focus(canvas, controller_id, "z-probe", "contacts")
    _focus(canvas, controller_id, "x-motor", "contacts")
    canvas.controller_connector_focus_combo.setCurrentIndex(0)
    details_index = next(
        index
        for index in range(canvas.controller_connector_focus_combo.count())
        if canvas.controller_connector_focus_combo.itemData(index)
        == "__all__::all::details"
    )
    canvas.controller_connector_focus_combo.setCurrentIndex(details_index)
    assert all(
        item.isVisible()
        for graphics in canvas._node_items.values()
        for item in graphics._port_items.values()
    )
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

    x_cable_id = _create_reference_cable_component(
        canvas, "X motor cable reference", QPointF(260.0, 80.0)
    )
    y_cable_id = _create_reference_cable_component(
        canvas, "Y motor cable reference", QPointF(260.0, 300.0)
    )
    _, fixture_connections = add_promega_xy_motor_reference_connections(
        canvas,
        x_cable_component_id=x_cable_id,
        y_cable_component_id=y_cable_id,
        controller_id=controller_id,
    )

    j9_connection_ids = {
        connection_id
        for connection_id, values in fixture_connections.items()
        if values[0] == "X"
    }
    assert len(j9_connection_ids) == 4

    contact_ids = {
        f"{controller_id}-x-motor-pin-{position}"
        for position in range(1, 5)
    }
    original_contact_ports = {
        port_id: deepcopy(canvas.store.semantic_model.ports[port_id])
        for port_id in contact_ids
    }
    original_semantic_connections = deepcopy(
        canvas.store.semantic_model.connections
    )
    original_visual_connections = deepcopy(canvas.store.model.connections)
    original_j9_semantic_connections = {
        connection_id: deepcopy(
            canvas.store.semantic_model.connections[connection_id]
        )
        for connection_id in j9_connection_ids
    }
    original_j9_visual_connections = {
        connection_id: deepcopy(canvas.store.model.connections[connection_id])
        for connection_id in j9_connection_ids
    }

    controller_node = canvas.store.model.nodes[controller_node.id]
    motor_node = canvas.store.model.nodes[motor_node.id]
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
    assert canvas_interaction.check_port_compatibility(
        controller_visual,
        motor_visual,
    ) == CompatibilityResult.UNKNOWN
    monkeypatch.setattr(
        canvas_interaction,
        "confirm_unknown_compatibility",
        lambda *_args: True,
    )
    monkeypatch.setattr(
        canvas._scene_controller,
        "find_port_graphics_at",
        lambda _position: target_item,
    )

    canvas._start_connection_drag(controller_visual.id, source_item.scenePos())
    canvas._finish_connection_drag(controller_visual.id, target_item.scenePos())

    assert len(canvas.store.semantic_model.connections) == (
        len(original_semantic_connections) + 1
    )
    new_connection_ids = (
        set(canvas.store.semantic_model.connections)
        - set(original_semantic_connections)
    )
    assert len(new_connection_ids) == 1
    connection = canvas.store.semantic_model.connections[
        next(iter(new_connection_ids))
    ]
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

    functional_semantic_record = deepcopy(connection)
    functional_visual_record = deepcopy(
        canvas.store.model.connections[connection.id]
    )
    expected_semantic_after = dict(original_semantic_connections)
    expected_semantic_after[connection.id] = functional_semantic_record
    expected_visual_after = dict(original_visual_connections)
    expected_visual_after[connection.id] = functional_visual_record

    assert canvas.store.semantic_model.connections == expected_semantic_after
    assert canvas.store.model.connections == expected_visual_after
    assert {
        connection_id: canvas.store.semantic_model.connections[connection_id]
        for connection_id in j9_connection_ids
    } == original_j9_semantic_connections
    assert {
        connection_id: canvas.store.model.connections[connection_id]
        for connection_id in j9_connection_ids
    } == original_j9_visual_connections
    assert {
        port_id: canvas.store.semantic_model.ports[port_id]
        for port_id in contact_ids
    } == original_contact_ports

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

    controller_graphics = canvas._node_items[controller_node.id]
    assert controller_graphics._connector_group_box.isVisible()
    assert controller_graphics._connector_group_title.text() == "J9 / X Motor"
    assert controller_graphics._connector_group_cone.isVisible()
    anchor = controller_graphics.connector_group_anchor_for_port(
        controller_port_id
    )
    assert anchor is not None

    # The routed path must terminate at the cone tip, not merely expose an
    # anchor while leaving the visible connection attached to the hidden port.
    path = graphics_connection.path()
    assert path.elementCount() >= 2
    if graphics_connection.endpoint_a_id == controller_visual.id:
        endpoint_fraction = 0.0
    else:
        assert graphics_connection.endpoint_b_id == controller_visual.id
        endpoint_fraction = 1.0

    rendered_endpoint = graphics_connection.mapToScene(
        path.pointAtPercent(endpoint_fraction)
    )
    assert abs(rendered_endpoint.x() - anchor.x()) <= 1e-6
    assert abs(rendered_endpoint.y() - anchor.y()) <= 1e-6

    assert (
        graphics_connection._endpoint_side_overrides[controller_visual.id]
        in {"left", "right"}
    )

    for position in range(1, 5):
        contact_id = f"{controller_id}-x-motor-pin-{position}"
        contact_visual = _visual_port(controller_node, contact_id)
        contact_semantic = canvas.store.semantic_model.ports[contact_id]
        assert (
            controller_graphics._port_items[contact_visual.id]._label_item.text()
            == f"{contact_semantic.properties['pin_label']} — {contact_semantic.purpose}"
        )

    # Focus changes must not affect undo history. Undo/redo must remove and
    # restore the functional relationship while preserving J9 contacts.
    assert canvas.store.undo()
    assert canvas.store.semantic_model.connections == original_semantic_connections
    assert canvas.store.model.connections == original_visual_connections
    assert {
        port_id: canvas.store.semantic_model.ports[port_id]
        for port_id in contact_ids
    } == original_contact_ports

    assert canvas.store.redo()
    assert canvas.store.semantic_model.connections == expected_semantic_after
    assert canvas.store.model.connections == expected_visual_after
    restored_connection = canvas.store.semantic_model.connections[connection.id]
    assert {
        restored_connection.endpoint_a_id,
        restored_connection.endpoint_b_id,
    } == {controller_port_id, motor_port_id}
    assert {
        port_id: canvas.store.semantic_model.ports[port_id]
        for port_id in contact_ids
    } == original_contact_ports
    assert {
        connection_id: canvas.store.semantic_model.connections[connection_id]
        for connection_id in j9_connection_ids
    } == original_j9_semantic_connections
    assert {
        connection_id: canvas.store.model.connections[connection_id]
        for connection_id in j9_connection_ids
    } == original_j9_visual_connections

    save_path = tmp_path / "functional-connection.machine.json"
    canvas.store.save(save_path)
    restored = load_editor_state(save_path)
    assert restored.semantic_model.connections[connection.id] == connection
    assert restored.semantic_model.ports[controller_port_id].properties[
        "interface_granularity"
    ] == "connector_level"
    assert contact_ids.issubset(restored.semantic_model.ports)


def test_frame_all_ignores_routing_debug_overlay():
    canvas, _controller_node, _motor_node, _controller_id = _make_canvas()
    try:
        canvas.show()
        _app().processEvents()
        canvas._frame_all()
        _app().processEvents()
        transform = canvas.view.transform()
        assert transform.m11() > 0.05
        assert transform.m22() > 0.05
    finally:
        canvas.close()

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
    assert canvas.controller_connector_focus_combo.count() == 2
    assert any(
        canvas.controller_connector_focus_combo.itemData(index)
        == "__all__::all::details"
        for index in range(canvas.controller_connector_focus_combo.count())
    )
    assert "generic Controller has no hardware-specific ports" in (
        canvas.controller_connector_focus_help.text()
    )