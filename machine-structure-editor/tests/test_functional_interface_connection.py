from __future__ import annotations

from copy import deepcopy

import pytest
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
    motor_port_item = motor_graphics._port_items[motor_visual.id]
    assert motor_port_item.isVisible()
    assert motor_port_item._label_side_override is None
    label_rect = motor_port_item._label_item.boundingRect()
    gap = motor_port_item.DIAMETER / 2.0 + 4.0

    if motor_port_item._side == "left":
        assert motor_port_item._label_item.pos().x() >= gap
    elif motor_port_item._side == "right":
        assert motor_port_item._label_item.pos().x() + label_rect.width() <= -gap
    elif motor_port_item._side == "top":
        assert motor_port_item._label_item.pos().y() >= gap
    elif motor_port_item._side == "bottom":
        assert motor_port_item._label_item.pos().y() + label_rect.height() <= -gap
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
        port_item = controller_graphics._port_items[visual_port.id]
        assert port_item._label_item.text() == semantic_port.properties["pin_label"]
        assert port_item._label_item.toolTip() == expected_label

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
    pre_focus_route = graphics_connection._debug_route
    pre_focus_reason = getattr(
        graphics_connection, "_routing_stability_reason", None
    )
    pre_focus_start_escape = graphics_connection._debug_start_escape
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
    assert graphics_connection._debug_route is not None, (
        "connector-focus regression: main route is None; "
        f"candidate={graphics_connection._routing_candidate_route!r}; "
        f"reason={getattr(graphics_connection, '_routing_stability_reason', None)!r}; "
        f"start_escape={graphics_connection._debug_start_escape!r}; "
        f"end_escape={graphics_connection._debug_end_escape!r}; "
        f"side_overrides={graphics_connection._endpoint_side_overrides!r}; "
        f"obstacles={graphics_connection._collect_obstacles()!r}; "
        f"physical_obstacles={graphics_connection._collect_physical_obstacles()!r}; "
        f"pre_focus_route={pre_focus_route!r}; "
        f"pre_focus_reason={pre_focus_reason!r}; "
        f"pre_focus_start_escape={pre_focus_start_escape!r}"
    )
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
        contact_item = controller_graphics._port_items[contact_visual.id]
        assert contact_item._label_item.text() == contact_semantic.properties["pin_label"]
        assert contact_item._label_item.toolTip() == (
            f"{contact_semantic.properties['pin_label']} — {contact_semantic.purpose}"
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
    combo = canvas.controller_connector_focus_combo
    assert combo.count() == 4
    assert {
        combo.itemData(index)
        for index in range(combo.count())
    } == {
        "",
        "__all__::all::details",
        "__all__::unused::details",
        "__all__::used::details",
    }
    assert any(
        canvas.controller_connector_focus_combo.itemData(index)
        == "__all__::all::details"
        for index in range(canvas.controller_connector_focus_combo.count())
    )
    assert "generic Controller has no hardware-specific ports" in (
        canvas.controller_connector_focus_help.text()
    )

# MB4_DETAIL_FILTER_AND_CONE_TESTS

def test_detail_modes_filter_individual_ports_and_hide_stranded_connections():
    from machine_builder.mutations import CreateConnection

    canvas, controller_node, motor_node, controller_id = _make_canvas()
    motor_component_id = motor_node.semantic_reference
    assert motor_component_id is not None

    controller_port = _visual_port(
        controller_node, f"{controller_id}-x-motor-interface"
    )
    motor_port = _visual_port(
        motor_node, f"{motor_component_id}-motor-electrical-interface"
    )
    connection_id = "detail-filter-functional-reference"
    canvas.store.commit(
        CreateConnection(
            connection_id=connection_id,
            endpoint_a_id=controller_port.id,
            endpoint_b_id=motor_port.id,
            connection_type="electrical",
        )
    )
    connection_graphics = canvas._connection_items[connection_id]
    assert connection_graphics.isVisible()

    canvas._controller_port_focus = ("__all__", "used", "details")
    canvas._apply_controller_connector_focus()

    controller_graphics = canvas._node_items[controller_node.id]
    motor_graphics = canvas._node_items[motor_node.id]
    assert controller_graphics._port_items[controller_port.id].isVisible()
    assert motor_graphics._port_items[motor_port.id].isVisible()
    assert all(
        not controller_graphics._port_items[port.id].isVisible()
        for port in controller_node.ports.values()
        if port.id != controller_port.id
    )
    assert all(
        not motor_graphics._port_items[port.id].isVisible()
        for port in motor_node.ports.values()
        if port.id != motor_port.id
    )
    assert connection_graphics.isVisible()

    canvas._controller_port_focus = ("__all__", "unused", "details")
    canvas._apply_controller_connector_focus()
    assert not controller_graphics._port_items[controller_port.id].isVisible()
    assert not motor_graphics._port_items[motor_port.id].isVisible()
    assert not connection_graphics.isVisible()

    unconnected_contact = _visual_port(
        controller_node, f"{controller_id}-x-motor-pin-1"
    )
    assert controller_graphics._port_items[unconnected_contact.id].isVisible()

    _focus(canvas, controller_id, "x-motor", "contacts")
    controller_node = canvas.store.model.nodes[controller_node.id]
    controller_graphics = canvas._node_items[controller_node.id]
    assert connection_graphics.isVisible()
    assert controller_graphics._connector_group_cone.isVisible()

    model = canvas.store.semantic_model
    contacts = [
        visual_port
        for visual_port in controller_node.ports.values()
        if (
            (port := model.ports.get(visual_port.semantic_reference)) is not None
            and port.controller_id == controller_id
            and port.connector_id == "x-motor"
            and port.pin_id is not None
        )
    ]
    sides = [
        str(port.side).lower().strip()
        for port in contacts
        if str(port.side).lower().strip() in {"left", "right"}
    ]
    group_port = model.ports[f"{controller_id}-x-motor-interface"]
    fallback_side = str(group_port.properties.get("visual_side") or "right").lower()
    if fallback_side not in {"left", "right"}:
        fallback_side = "right"
    left_count = sides.count("left")
    right_count = sides.count("right")
    if left_count > right_count:
        expected_direction = "left"
    elif right_count > left_count:
        expected_direction = "right"
    elif sides and fallback_side in sides:
        expected_direction = fallback_side
    elif sides:
        expected_direction = sides[0]
    else:
        expected_direction = fallback_side

    assert controller_graphics._connector_group_info["direction"] == expected_direction
    box = controller_graphics._connector_group_box.path().boundingRect()
    tip = controller_graphics._connector_group_anchor_local
    assert tip is not None
    if expected_direction == "left":
        assert tip.x() < box.left()
    else:
        assert tip.x() > box.right()
    assert controller_graphics._connector_group_cone.zValue() > connection_graphics.zValue()


def test_contact_focus_shows_the_motor_terminal_connected_to_a_board_contact():
    from machine_builder.mutations import CreateConnection
    from machine_builder.semantic_component_mutations import (
        UpdateMachineComponentWithStepperTerminalProfile,
    )

    canvas, controller_node, motor_node, controller_id = _make_canvas()
    motor_component_id = motor_node.semantic_reference
    assert motor_component_id is not None
    component = canvas.store.semantic_model.components[motor_component_id]
    properties = dict(component.properties)
    properties["motor_terminal_profile"] = "stepper_four_lead"

    canvas.store.commit(
        UpdateMachineComponentWithStepperTerminalProfile(
            component_id=component.id,
            role=component.role,
            label=component.label,
            properties=properties,
            provenance_entries=component.provenance.copy(),
        )
    )

    controller_node = canvas.store.model.nodes[controller_node.id]
    motor_node = canvas.store.model.nodes[motor_node.id]
    board_contact = _visual_port(
        controller_node, f"{controller_id}-x-motor-pin-1"
    )
    motor_lead_1 = _visual_port(
        motor_node, f"{motor_component_id}-stepper-lead-1"
    )
    motor_lead_2 = _visual_port(
        motor_node, f"{motor_component_id}-stepper-lead-2"
    )
    connection_id = "focused-contact-to-motor-lead-1"
    canvas.store.commit(
        CreateConnection(
            connection_id=connection_id,
            endpoint_a_id=board_contact.id,
            endpoint_b_id=motor_lead_1.id,
            connection_type="electrical",
            connection_properties={
                "wire_color": "black",
                "harness_id": "illustrative-test",
                "notes": "Test connection only; no coil mapping asserted.",
            },
        )
    )

    _focus(canvas, controller_id, "x-motor", "contacts")
    controller_graphics = canvas._node_items[controller_node.id]
    motor_graphics = canvas._node_items[motor_node.id]

    assert controller_graphics._connector_group_cone.isVisible()
    assert controller_graphics._connector_group_cone.zValue() > -10.0
    assert motor_graphics._port_items[motor_lead_1.id].isVisible()
    assert motor_graphics._port_items[motor_lead_2.id].isVisible()
    assert canvas._connection_items[connection_id].isVisible()
    assert canvas._connection_items[connection_id].pen().color().name() == "#000000"

def test_contact_focus_groups_explicit_stepper_motor_terminals_for_presentation_only():
    from machine_builder.mutations import CreateConnection
    from machine_builder.semantic_component_mutations import (
        UpdateMachineComponentWithStepperTerminalProfile,
    )

    canvas, controller_node, motor_node, controller_id = _make_canvas()
    motor_component_id = motor_node.semantic_reference
    assert motor_component_id is not None
    component = canvas.store.semantic_model.components[motor_component_id]
    properties = dict(component.properties)
    properties["motor_terminal_profile"] = "stepper_four_lead"

    canvas.store.commit(
        UpdateMachineComponentWithStepperTerminalProfile(
            component_id=component.id,
            role=component.role,
            label=component.label,
            properties=properties,
            provenance_entries=component.provenance.copy(),
        )
    )

    controller_node = canvas.store.model.nodes[controller_node.id]
    motor_node = canvas.store.model.nodes[motor_node.id]
    board_contact = _visual_port(
        controller_node, f"{controller_id}-x-motor-pin-1"
    )
    motor_leads = [
        _visual_port(
            motor_node, f"{motor_component_id}-stepper-lead-{index}"
        )
        for index in range(1, 5)
    ]
    motor_interface = next(
        port
        for port in canvas.store.semantic_model.ports.values()
        if (
            port.component_id == motor_component_id
            and port.properties.get("interface_granularity")
            == "functional_interface"
            and port.properties.get("interface_role")
            == "motor_electrical_interface"
        )
    )
    motor_interface_visual = _visual_port(motor_node, motor_interface.id)
    connection_id = "focused-contact-to-motor-lead-1"
    canvas.store.commit(
        CreateConnection(
            connection_id=connection_id,
            endpoint_a_id=board_contact.id,
            endpoint_b_id=motor_leads[0].id,
            connection_type="electrical",
            connection_properties={
                "wire_color": "black",
                "harness_id": "illustrative-test",
                "notes": "Test connection only; no coil mapping asserted.",
            },
        )
    )

    semantic_port_ids = set(canvas.store.semantic_model.ports)
    semantic_connections = {
        item.id: (item.endpoint_a_id, item.endpoint_b_id)
        for item in canvas.store.semantic_model.connections.values()
    }

    _focus(canvas, controller_id, "x-motor", "contacts")

    motor_graphics = canvas._node_items[motor_node.id]
    group_info = motor_graphics._connector_group_info
    assert group_info is not None
    assert group_info["title"] == "Motor electrical interface"
    assert group_info.get("endpoint_port_id") is None
    assert group_info["connected"] is True
    assert {
        pin_info["semantic_port_id"]
        for pin_info in group_info["pins"].values()
    } == {lead.semantic_reference for lead in motor_leads}
    assert all(
        motor_graphics._port_items[lead.id].isVisible()
        for lead in motor_leads
    )
    assert motor_graphics._connector_group_box.isVisible()
    assert motor_graphics._connector_group_cone.isVisible()
    assert not motor_graphics._port_items[motor_interface_visual.id].isVisible()

    # All four physical terminals follow the cone side; the cone stays outside
    # the enclosure regardless of which side faces the controller.
    group_side = group_info["port_side_override"]
    box_bounds = motor_graphics._connector_group_box.path().boundingRect()
    cone_bounds = motor_graphics._connector_group_cone.path().boundingRect()
    if group_side == "left":
        assert all(
            abs(motor_graphics._port_items[lead.id].pos().x() - 18.0) <= 1e-6
            for lead in motor_leads
        )
        assert cone_bounds.right() <= box_bounds.left() + 1e-6
    else:
        assert group_side == "right"
        right_x = motor_graphics.rect().width() - 18.0
        assert all(
            abs(motor_graphics._port_items[lead.id].pos().x() - right_x) <= 1e-6
            for lead in motor_leads
        )
        assert cone_bounds.left() >= box_bounds.right() - 1e-6

    # Grouping is presentation-only: do not create group ports or rewrite wires.
    assert set(canvas.store.semantic_model.ports) == semantic_port_ids
    assert {
        item.id: (item.endpoint_a_id, item.endpoint_b_id)
        for item in canvas.store.semantic_model.connections.values()
    } == semantic_connections
    assert connection_id in semantic_connections

    _focus(canvas, "__all__", "all", "details")
    assert motor_graphics._port_items[motor_interface_visual.id].isVisible()
    assert not motor_graphics._connector_group_box.isVisible()
    assert not motor_graphics._connector_group_cone.isVisible()

def test_contact_focus_routes_contacts_to_shared_cone_tip_and_contact_origins():
    from machine_builder.mutations import CreateConnection, MoveNodes
    from machine_builder.semantic_component_mutations import (
        UpdateMachineComponentWithStepperTerminalProfile,
    )

    canvas, controller_node, motor_node, controller_id = _make_canvas()
    motor_component_id = motor_node.semantic_reference
    assert motor_component_id is not None
    component = canvas.store.semantic_model.components[motor_component_id]
    properties = dict(component.properties)
    properties["motor_terminal_profile"] = "stepper_four_lead"

    canvas.store.commit(
        UpdateMachineComponentWithStepperTerminalProfile(
            component_id=component.id,
            role=component.role,
            label=component.label,
            properties=properties,
            provenance_entries=component.provenance.copy(),
        )
    )

    canvas.store.commit(
        MoveNodes(
            positions={motor_node.id: (-103.0, 204.0)}
        )
    )
    controller_node = canvas.store.model.nodes[controller_node.id]
    motor_node = canvas.store.model.nodes[motor_node.id]
    contacts = [
        _visual_port(
            controller_node,
            f"{controller_id}-x-motor-pin-{position}",
        )
        for position in range(1, 5)
    ]
    leads = [
        _visual_port(
            motor_node,
            f"{motor_component_id}-stepper-lead-{position}",
        )
        for position in range(1, 5)
    ]
    connection_ids = []

    for position, contact, lead, color in zip(
        range(1, 5),
        contacts,
        leads,
        ("black", "red", "green", "blue"),
    ):
        connection_id = f"contact-cone-landing-{position}"
        connection_ids.append(connection_id)
        canvas.store.commit(
            CreateConnection(
                connection_id=connection_id,
                endpoint_a_id=contact.id,
                endpoint_b_id=lead.id,
                connection_type="electrical",
                connection_properties={
                    "wire_color": color,
                    "harness_id": "illustrative-test",
                    "notes": "Test routing only; no coil mapping asserted.",
                },
            )
        )

    _focus(canvas, controller_id, "x-motor", "contacts")
    controller_graphics = canvas._node_items[controller_node.id]
    motor_graphics = canvas._node_items[motor_node.id]
    assert controller_graphics._connector_group_cone.isVisible()

    anchors = [
        controller_graphics.connector_group_anchor_for_port(
            contact.semantic_reference
        )
        for contact in contacts
    ]
    assert all(anchor is not None for anchor in anchors)
    assert abs(anchors[0].x() - anchors[1].x()) <= 1e-6
    assert abs(anchors[0].y() - anchors[1].y()) <= 1e-6

    contact_origins = [
        controller_graphics.connector_group_contact_origin_for_port(
            contact.semantic_reference
        )
        for contact in contacts
    ]
    port_centers = [
        controller_graphics._port_items[contact.id].mapToScene(
            controller_graphics._port_items[contact.id].boundingRect().center()
        )
        for contact in contacts
    ]
    assert all(origin is not None for origin in contact_origins)
    for origin, port_center in zip(contact_origins, port_centers):
        assert abs(origin.x() - port_center.x()) <= 1e-6
        assert abs(origin.y() - port_center.y()) <= 1e-6
    assert (
        abs(contact_origins[0].x() - contact_origins[1].x())
        + abs(contact_origins[0].y() - contact_origins[1].y())
        > 1.0
    )
    assert any(
        abs(origin.y() - anchor.y()) > 1e-6
        for origin, anchor in zip(contact_origins, anchors)
    )

    fanout_start_coordinates = []

    def _is_segment_endpoint(point, start, end):
        tolerance = 1e-6
        return (
            (
                abs(point.x() - start.x()) <= tolerance
                and abs(point.y() - start.y()) <= tolerance
            )
            or (
                abs(point.x() - end.x()) <= tolerance
                and abs(point.y() - end.y()) <= tolerance
            )
        )

    def routes_have_unintended_crossing(first_route, second_route):
        tolerance = 1e-6
        for first_start, first_end in zip(first_route, first_route[1:]):
            first_horizontal = abs(first_start.y() - first_end.y()) <= tolerance
            first_vertical = abs(first_start.x() - first_end.x()) <= tolerance
            assert first_horizontal or first_vertical, "Expected orthogonal first route"

            for second_start, second_end in zip(second_route, second_route[1:]):
                second_horizontal = abs(second_start.y() - second_end.y()) <= tolerance
                second_vertical = abs(second_start.x() - second_end.x()) <= tolerance
                assert second_horizontal or second_vertical, "Expected orthogonal second route"

                if first_horizontal and second_horizontal:
                    if abs(first_start.y() - second_start.y()) > tolerance:
                        continue
                    overlap_start = max(
                        min(first_start.x(), first_end.x()),
                        min(second_start.x(), second_end.x()),
                    )
                    overlap_end = min(
                        max(first_start.x(), first_end.x()),
                        max(second_start.x(), second_end.x()),
                    )
                    if overlap_end < overlap_start - tolerance:
                        continue
                    if overlap_end > overlap_start + tolerance:
                        return True
                    intersection = QPointF(
                        (overlap_start + overlap_end) / 2.0,
                        (first_start.y() + second_start.y()) / 2.0,
                    )
                    if not (
                        _is_segment_endpoint(intersection, first_start, first_end)
                        and _is_segment_endpoint(intersection, second_start, second_end)
                    ):
                        return True

                elif first_vertical and second_vertical:
                    if abs(first_start.x() - second_start.x()) > tolerance:
                        continue
                    overlap_start = max(
                        min(first_start.y(), first_end.y()),
                        min(second_start.y(), second_end.y()),
                    )
                    overlap_end = min(
                        max(first_start.y(), first_end.y()),
                        max(second_start.y(), second_end.y()),
                    )
                    if overlap_end < overlap_start - tolerance:
                        continue
                    if overlap_end > overlap_start + tolerance:
                        return True
                    intersection = QPointF(
                        (first_start.x() + second_start.x()) / 2.0,
                        (overlap_start + overlap_end) / 2.0,
                    )
                    if not (
                        _is_segment_endpoint(intersection, first_start, first_end)
                        and _is_segment_endpoint(intersection, second_start, second_end)
                    ):
                        return True

                else:
                    if first_horizontal:
                        horizontal_start, horizontal_end = first_start, first_end
                        vertical_start, vertical_end = second_start, second_end
                    else:
                        horizontal_start, horizontal_end = second_start, second_end
                        vertical_start, vertical_end = first_start, first_end

                    intersection = QPointF(
                        vertical_start.x(),
                        horizontal_start.y(),
                    )
                    horizontal_min = min(horizontal_start.x(), horizontal_end.x())
                    horizontal_max = max(horizontal_start.x(), horizontal_end.x())
                    vertical_min = min(vertical_start.y(), vertical_end.y())
                    vertical_max = max(vertical_start.y(), vertical_end.y())

                    if (
                        horizontal_min - tolerance
                        <= intersection.x()
                        <= horizontal_max + tolerance
                        and vertical_min - tolerance
                        <= intersection.y()
                        <= vertical_max + tolerance
                    ):
                        if not (
                            _is_segment_endpoint(
                                intersection, first_start, first_end
                            )
                            and _is_segment_endpoint(
                                intersection, second_start, second_end
                            )
                        ):
                            return True

        return False
    for connection_id, anchor, contact_origin, lead, expected_color in zip(
        connection_ids,
        anchors,
        contact_origins,
        leads,
        ("#000000", "#ff0000", "#008000", "#0000ff"),
    ):
        graphics = canvas._connection_items[connection_id]
        assert graphics.isVisible()
        assert motor_graphics._port_items[lead.id].isVisible()
        rendered_start = graphics.mapToScene(
            graphics.path().pointAtPercent(0.0)
        )
        assert abs(rendered_start.x() - anchor.x()) <= 1e-6
        assert abs(rendered_start.y() - anchor.y()) <= 1e-6

        # The rendered path leaves the shared tip through a unique fan-out point.
        escape = graphics._debug_start_escape
        assert len(escape) == 2
        escape_start, escape_end = escape
        fanout_start_coordinates.append((escape_start.x(), escape_start.y()))
        side = graphics._endpoint_side_overrides[graphics.endpoint_a_id]
        assert side in {"left", "right"}
        expected_dx = -18.0 if side == "left" else 18.0
        assert abs(escape_start.x() - (anchor.x() + expected_dx)) <= 1e-6
        assert abs(escape_start.y() - anchor.y()) >= 3.0
        assert abs(escape_end.y() - escape_start.y()) <= 1e-6
        if side == "left":
            assert escape_end.x() < escape_start.x()
        else:
            assert escape_end.x() > escape_start.x()

        # Each conductor begins at its real contact and converges at the shared tip.
        stub = canvas._scene_controller._connector_wire_stub_items[
            (connection_id, graphics.endpoint_a_id)
        ]
        assert stub.isVisible()
        assert stub.pen().color().name() == expected_color
        stub_path = stub.path()
        assert stub_path.elementCount() == 2
        if expected_color == "#000000":
            from PySide6.QtCore import QPointF

            def _mb4_xy(point):
                return (round(float(point.x()), 2), round(float(point.y()), 2))

            stub_scene_start = stub.mapToScene(stub_path.pointAtPercent(0.0))
            stub_scene_end = stub.mapToScene(stub_path.pointAtPercent(1.0))
            cone_path = controller_graphics._connector_group_cone.path()
            cone_scene = [
                _mb4_xy(controller_graphics.mapToScene(
                    QPointF(cone_path.elementAt(i).x, cone_path.elementAt(i).y)
                ))
                for i in range(cone_path.elementCount())
            ]
            path = graphics.path()
            path_first = [
                _mb4_xy(graphics.mapToScene(
                    QPointF(path.elementAt(i).x, path.elementAt(i).y)
                ))
                for i in range(min(path.elementCount(), 8))
            ]
            route = graphics._debug_route or ()
            print("[MB4_ROUTE_DIAG_BLACK] id/endpoints:",
                  connection_id, graphics.endpoint_a_id, "->", graphics.endpoint_b_id)
            print("[MB4_ROUTE_DIAG_BLACK] stub scene:",
                  _mb4_xy(stub_scene_start), "->", _mb4_xy(stub_scene_end))
            print("[MB4_ROUTE_DIAG_BLACK] cone scene vertices:", cone_scene)
            print("[MB4_ROUTE_DIAG_BLACK] side/offset:",
                  graphics._endpoint_side_overrides.get(graphics.endpoint_a_id),
                  graphics._endpoint_route_fanout_offsets.get(graphics.endpoint_a_id))
            print("[MB4_ROUTE_DIAG_BLACK] start escape:",
                  [_mb4_xy(p) for p in graphics._debug_start_escape])
            print("[MB4_ROUTE_DIAG_BLACK] first core-route points:",
                  [_mb4_xy(p) for p in route[:5]])
            print("[MB4_ROUTE_DIAG_BLACK] end escape:",
                  [_mb4_xy(p) for p in graphics._debug_end_escape])
            print("[MB4_ROUTE_DIAG_BLACK] first rendered path points:", path_first)
        stub_start = stub_path.pointAtPercent(0.0)
        stub_end = stub_path.pointAtPercent(1.0)
        assert abs(stub_start.x() - contact_origin.x()) <= 1e-6
        assert abs(stub_start.y() - contact_origin.y()) <= 1e-6
        from PySide6.QtCore import QPointF
        cone_path = controller_graphics._connector_group_cone.path()
        base_top = cone_path.elementAt(1)
        base_bottom = cone_path.elementAt(2)
        base_start = controller_graphics.mapToScene(
            QPointF(base_top.x, base_top.y)
        )
        base_end = controller_graphics.mapToScene(
            QPointF(base_bottom.x, base_bottom.y)
        )
        base_dx = base_end.x() - base_start.x()
        base_dy = base_end.y() - base_start.y()
        base_length_squared = base_dx * base_dx + base_dy * base_dy
        assert base_length_squared > 1e-9
        projection = (
            (stub_end.x() - base_start.x()) * base_dx
            + (stub_end.y() - base_start.y()) * base_dy
        ) / base_length_squared
        assert 0.0 <= projection <= 1.0
        closest_x = base_start.x() + projection * base_dx
        closest_y = base_start.y() + projection * base_dy
        base_distance = (
            (stub_end.x() - closest_x) ** 2
            + (stub_end.y() - closest_y) ** 2
        ) ** 0.5
        assert 0.7 <= base_distance <= 1.1
        assert abs(stub_start.x() - stub_end.x()) > 1e-6
        assert abs(stub_start.y() - stub_end.y()) > 1e-6

    assert len(fanout_start_coordinates) == 4
    assert len(set(fanout_start_coordinates)) == 4

    # Every grouped contact uses a lane at least the router's required
    # separation from every other contact on the same connector group.
    for grouped_endpoints, group_name in (
        (contacts, "controller"),
        (leads, "motor"),
    ):
        lane_offsets = [
            canvas._connection_items[connection_id]
            ._endpoint_route_fanout_offsets[endpoint.id]
            for connection_id, endpoint in zip(connection_ids, grouped_endpoints)
        ]
        assert all(
            abs(lane_offsets[first] - lane_offsets[second]) >= 8.0 - 1e-3
            for first in range(len(lane_offsets))
            for second in range(first + 1, len(lane_offsets))
        ), f"{group_name} fan-out lanes are too close: {lane_offsets}"

    core_routes = []
    for connection_id in connection_ids:
        graphics = canvas._connection_items[connection_id]
        route = graphics._debug_route
        assert route is not None and len(route) >= 2, (
            f"Missing core route for {connection_id}; "
            f"reason={graphics._routing_stability_reason!r}; "
            f"candidate={graphics._routing_candidate_route!r}; "
            f"selected={graphics._routing_selected_route!r}; "
            f"start_escape={graphics._debug_start_escape!r}; "
            f"end_escape={graphics._debug_end_escape!r}"
        )
        core_routes.append((connection_id, route))

    for first_index, (first_id, first_route) in enumerate(core_routes):
        for second_id, second_route in core_routes[first_index + 1:]:
            assert not routes_have_unintended_crossing(
                first_route, second_route
            ), f"Core routes cross or overlap: {first_id} and {second_id}"
    _movement_origin = QPointF(motor_graphics.pos())
    try:
        for _movement_dx, _movement_dy in (
            (10.0, 5.0),
            (20.0, 10.0),
            (30.0, 15.0),
            (40.0, 20.0),
            (50.0, 25.0),
        ):
            motor_graphics.setPos(
                _movement_origin.x() + _movement_dx,
                _movement_origin.y() + _movement_dy,
            )
            _moved_routes = []
            for _connection_id in connection_ids:
                _graphics = canvas._connection_items[_connection_id]
                _route = _graphics._debug_route
                assert _route is not None and len(_route) >= 2, (
                    f"Route disappeared while moving motor by "
                    f"({_movement_dx}, {_movement_dy}): {_connection_id}; "
                    f"reason={_graphics._routing_stability_reason!r}; "
                    f"candidate={_graphics._routing_candidate_route!r}"
                )
                _length = sum(
                    abs(_route_point_b.x() - _route_point_a.x())
                    + abs(_route_point_b.y() - _route_point_a.y())
                    for _route_point_a, _route_point_b in zip(
                        _route, _route[1:]
                    )
                )
                assert _length < 400.0, (
                    f"Excessive route detour during movement: "
                    f"{_connection_id} length={_length}"
                )
                _moved_routes.append((_connection_id, _route))

            for _first_index, (_first_id, _first_route) in enumerate(_moved_routes):
                for _second_id, _second_route in _moved_routes[_first_index + 1:]:
                    assert not routes_have_unintended_crossing(
                        _first_route, _second_route
                    ), (
                        f"Moved core routes cross or overlap: "
                        f"{_first_id} and {_second_id}"
                    )
    finally:
        motor_graphics.setPos(_movement_origin)

    for _connection_id in connection_ids:
        _restored_route = canvas._connection_items[_connection_id]._debug_route
        assert _restored_route is not None and len(_restored_route) >= 2, (
            f"Route did not recover after restoring motor position: {_connection_id}"
        )


    # Moving out of connector-contact focus must remove transient cone stubs.
    expected_stub_keys = {
        (connection_id, endpoint.id)
        for connection_id, contact, lead in zip(connection_ids, contacts, leads)
        for endpoint in (contact, lead)
    }
    assert set(canvas._scene_controller._connector_wire_stub_items) == expected_stub_keys
    _focus(canvas, "__all__", "all", "details")
    assert canvas._scene_controller._connector_wire_stub_items == {}

def test_contact_focus_hides_refined_contact_functional_link():
    from machine_builder.mutations import CreateConnection
    from machine_builder.semantic_component_mutations import (
        UpdateMachineComponentWithStepperTerminalProfile,
    )

    canvas, controller_node, motor_node, controller_id = _make_canvas()
    motor_component_id = motor_node.semantic_reference
    assert motor_component_id is not None

    component = canvas.store.semantic_model.components[motor_component_id]
    properties = dict(component.properties)
    properties["visual_node_type"] = "motor"
    properties["motor_terminal_profile"] = "stepper_four_lead"
    canvas.store.commit(
        UpdateMachineComponentWithStepperTerminalProfile(
            component_id=component.id,
            role=component.role,
            label=component.label,
            properties=properties,
            provenance_entries=component.provenance.copy(),
        )
    )

    controller_node = canvas.store.model.nodes[controller_node.id]
    motor_node = canvas.store.model.nodes[motor_node.id]
    contact = _visual_port(
        controller_node,
        f"{controller_id}-x-motor-pin-1",
    )
    lead = _visual_port(
        motor_node,
        f"{motor_component_id}-stepper-lead-1",
    )
    motor_interface = next(
        port
        for port in canvas.store.semantic_model.ports.values()
        if (
            port.component_id == motor_component_id
            and port.properties.get("interface_granularity")
            == "functional_interface"
            and port.properties.get("interface_role")
            == "motor_electrical_interface"
        )
    )
    interface_visual = _visual_port(motor_node, motor_interface.id)

    duplicate_id = "test-contact-to-functional-interface"
    conductor_id = "test-contact-to-physical-terminal"
    for connection_id, target, note in (
        (duplicate_id, interface_visual, "coarse interface reference"),
        (conductor_id, lead, "direct physical terminal path"),
    ):
        canvas.store.commit(
            CreateConnection(
                connection_id=connection_id,
                endpoint_a_id=contact.id,
                endpoint_b_id=target.id,
                connection_type="electrical",
                connection_properties={
                    "wire_color": "black",
                    "notes": note,
                },
            )
        )

    # Connector contact focus should render the direct conductor without
    # painting a second contact-to-functional-interface route over it.
    _focus(canvas, controller_id, "x-motor", "contacts")
    assert duplicate_id in canvas.store.semantic_model.connections
    assert conductor_id in canvas.store.semantic_model.connections
    assert not canvas._connection_items[duplicate_id].isVisible()
    assert canvas._connection_items[conductor_id].isVisible()

    # Detailed-all is diagnostic presentation: both stored relationships
    # remain accessible and the filter does not remove or rewrite either.
    all_key = "__all__::all::details"
    all_index = next(
        index
        for index in range(canvas.controller_connector_focus_combo.count())
        if canvas.controller_connector_focus_combo.itemData(index) == all_key
    )
    canvas.controller_connector_focus_combo.setCurrentIndex(all_index)
    assert canvas._connection_items[duplicate_id].isVisible()
    assert canvas._connection_items[conductor_id].isVisible()
    assert duplicate_id in canvas.store.model.connections
    assert conductor_id in canvas.store.model.connections

    _focus(canvas, controller_id, "x-motor", "contacts")
    assert not canvas._connection_items[duplicate_id].isVisible()
    assert canvas._connection_items[conductor_id].isVisible()
    assert duplicate_id in canvas.store.semantic_model.connections
    assert conductor_id in canvas.store.semantic_model.connections


def test_loading_document_schedules_canvas_framing(monkeypatch, tmp_path):
    source_canvas, _, _, _ = _make_canvas()
    document_path = tmp_path / "loaded-machine.machine.json"
    source_canvas.store.save(document_path)

    canvas, _, _, _ = _make_canvas()
    frame_calls = []
    monkeypatch.setattr(canvas, "_frame_all", lambda: frame_calls.append(True))

    canvas.store.load(document_path)
    _app().processEvents()

    assert frame_calls == [True]

@pytest.mark.parametrize(
    ("conflict_field", "wrong_value"),
    [
        ("component_id", "different-owner"),
        ("interface_role", "different_role"),
        ("interface_granularity", "connector_level"),
        ("motor_terminal_profile", "different_profile"),
        ("terminal_display_index", "2"),
    ],
)
def test_stepper_terminal_profile_rejects_conflicting_existing_terminal_metadata(
    conflict_field,
    wrong_value,
):
    from machine_builder.semantic_component_mutations import (
        UpdateMachineComponentWithStepperTerminalProfile,
    )
    from machine_builder.semantic_model import SemanticPort

    canvas, _, motor_node, _ = _make_canvas()
    component_id = motor_node.semantic_reference
    assert component_id is not None
    component = canvas.store.semantic_model.components[component_id]
    terminal_id = f"{component_id}-stepper-lead-1"

    properties = {
        "interface_role": "motor_conductor_terminal",
        "interface_granularity": "physical_terminal",
        "motor_terminal_profile": "stepper_four_lead",
        "terminal_display_index": "1",
        "terminal_identity_status": "unassigned",
        "motor_coil_mapping_status": "not_established",
        "controller_contact_mapping_status": "not_established",
        "physical_wiring_status": "not_verified_as_built",
        "visual_port_type": "motor",
        "visual_side": "left",
    }
    port_component_id = component_id
    if conflict_field != "component_id":
        properties[conflict_field] = wrong_value

    canvas.store.semantic_model.add_port(
        SemanticPort(
            id=terminal_id,
            component_id=port_component_id,
            controller_id=None,
            purpose="Intentional conflicting test endpoint",
            direction="unknown",
            connector_id=None,
            pin_id=None,
            properties=properties,
            provenance=[
                Provenance(
                    source="Machine Builder regression test",
                    evidence_type="authored",
                    method="pytest",
                    context="Intentionally conflicting terminal metadata.",
                    date="2026-10-22",
                    notes="Test-only endpoint; no physical wiring is asserted.",
                )
            ],
        )
    )

    if conflict_field == "component_id":
        # Deliberately corrupt only the test fixture after add_port validates it.
        canvas.store.semantic_model.ports[terminal_id].component_id = wrong_value

    before_component = deepcopy(
        canvas.store.semantic_model.components[component_id]
    )
    before_port = deepcopy(canvas.store.semantic_model.ports[terminal_id])
    before_node = canvas.store.model.nodes[motor_node.id]
    before_node_label = before_node.label
    before_visual_port_ids = set(before_node.ports)
    before_undo_depth = len(canvas.store._undo_stack)
    before_redo_depth = len(canvas.store._redo_stack)
    before_modified = canvas.store.is_modified

    requested_properties = deepcopy(before_component.properties)
    requested_properties["visual_node_type"] = "motor"
    requested_properties["motor_terminal_profile"] = "stepper_four_lead"

    with pytest.raises(ValueError, match="Conflicting existing motor terminal port"):
        canvas.store.commit(
            UpdateMachineComponentWithStepperTerminalProfile(
                component_id=component_id,
                role=before_component.role,
                label="Rejected terminal-profile update",
                properties=requested_properties,
                provenance_entries=deepcopy(before_component.provenance),
            )
        )

    after_component = canvas.store.semantic_model.components[component_id]
    assert after_component.properties == before_component.properties
    assert after_component.role == before_component.role
    assert after_component.label == before_component.label
    assert after_component.provenance == before_component.provenance
    assert canvas.store.semantic_model.ports[terminal_id] == before_port
    assert not any(
        f"{component_id}-stepper-lead-{index}" in canvas.store.semantic_model.ports
        for index in (2, 3, 4)
    )
    after_node = canvas.store.model.nodes[motor_node.id]
    assert after_node.label == before_node_label
    assert set(after_node.ports) == before_visual_port_ids
    assert len(canvas.store._undo_stack) == before_undo_depth
    assert len(canvas.store._redo_stack) == before_redo_depth
    assert canvas.store.is_modified == before_modified


def test_stepper_terminal_profile_rejects_non_motor_component_atomically():
    from machine_builder.semantic_component_mutations import (
        UpdateMachineComponentWithStepperTerminalProfile,
    )

    canvas, _, motor_node, _ = _make_canvas()
    component_id = motor_node.semantic_reference
    assert component_id is not None
    component = canvas.store.semantic_model.components[component_id]
    before_properties = deepcopy(component.properties)
    before_label = component.label
    before_undo_depth = len(canvas.store._undo_stack)
    before_modified = canvas.store.is_modified

    requested_properties = deepcopy(before_properties)
    requested_properties["visual_node_type"] = "not_a_motor"
    requested_properties["motor_terminal_profile"] = "stepper_four_lead"

    with pytest.raises(
        ValueError,
        match="requires a component whose visual_node_type is 'motor'",
    ):
        canvas.store.commit(
            UpdateMachineComponentWithStepperTerminalProfile(
                component_id=component_id,
                role=component.role,
                label="Rejected invalid component type",
                properties=requested_properties,
                provenance_entries=deepcopy(component.provenance),
            )
        )

    component_after = canvas.store.semantic_model.components[component_id]
    assert component_after.properties == before_properties
    assert component_after.label == before_label
    assert not any(
        f"{component_id}-stepper-lead-{index}" in canvas.store.semantic_model.ports
        for index in (1, 2, 3, 4)
    )
    assert len(canvas.store._undo_stack) == before_undo_depth
    assert canvas.store.is_modified == before_modified


def test_stepper_terminal_profile_undo_redo_and_persistence(tmp_path):
    from machine_builder.semantic_component_mutations import (
        UpdateMachineComponentWithStepperTerminalProfile,
    )

    canvas, _, motor_node, _ = _make_canvas()
    component_id = motor_node.semantic_reference
    assert component_id is not None
    component = canvas.store.semantic_model.components[component_id]
    before_properties = deepcopy(component.properties)
    terminal_ids = tuple(
        f"{component_id}-stepper-lead-{index}"
        for index in range(1, 5)
    )
    assert not any(
        terminal_id in canvas.store.semantic_model.ports
        for terminal_id in terminal_ids
    )

    requested_properties = deepcopy(component.properties)
    requested_properties["visual_node_type"] = "motor"
    requested_properties["motor_terminal_profile"] = "stepper_four_lead"
    canvas.store.commit(
        UpdateMachineComponentWithStepperTerminalProfile(
            component_id=component_id,
            role=component.role,
            label=component.label,
            properties=requested_properties,
            provenance_entries=deepcopy(component.provenance),
        )
    )

    assert set(terminal_ids).issubset(canvas.store.semantic_model.ports)
    assert canvas.store.undo()
    assert canvas.store.semantic_model.components[component_id].properties == before_properties
    assert not any(
        terminal_id in canvas.store.semantic_model.ports
        for terminal_id in terminal_ids
    )

    assert canvas.store.redo()
    assert set(terminal_ids).issubset(canvas.store.semantic_model.ports)
    for index, terminal_id in enumerate(terminal_ids, start=1):
        port = canvas.store.semantic_model.ports[terminal_id]
        assert port.component_id == component_id
        assert port.properties["interface_role"] == "motor_conductor_terminal"
        assert port.properties["interface_granularity"] == "physical_terminal"
        assert port.properties["motor_terminal_profile"] == "stepper_four_lead"
        assert port.properties["terminal_display_index"] == str(index)

    visual_node = canvas.store.model.nodes[motor_node.id]
    projected_references = {
        visual_port.semantic_reference
        for visual_port in visual_node.ports.values()
    }
    assert set(terminal_ids).issubset(projected_references)

    save_path = tmp_path / "stepper-terminal-profile.machine.json"
    canvas.store.save(save_path)
    restored = load_editor_state(save_path)
    assert set(terminal_ids).issubset(restored.semantic_model.ports)
    restored_node = restored.visual_model.nodes[motor_node.id]
    restored_references = {
        visual_port.semantic_reference
        for visual_port in restored_node.ports.values()
    }
    assert set(terminal_ids).issubset(restored_references)
    for index, terminal_id in enumerate(terminal_ids, start=1):
        port = restored.semantic_model.ports[terminal_id]
        assert port.properties["interface_granularity"] == "physical_terminal"
        assert port.properties["motor_terminal_profile"] == "stepper_four_lead"
        assert port.properties["terminal_display_index"] == str(index)

def test_controller_port_focus_persists_across_undo_redo_save_and_reopen(tmp_path):
    canvas, _, motor_node, controller_id = _make_canvas()
    component_id = motor_node.semantic_reference
    assert component_id is not None
    component = canvas.store.semantic_model.components[component_id]

    canvas.store.commit(
        UpdateMachineComponent(
            component_id=component_id,
            label="Temporary undo/redo test label",
        )
    )
    _focus(canvas, controller_id, "x-motor", "contacts")
    expected_focus = (controller_id, "x-motor", "contacts")
    assert canvas._controller_port_focus == expected_focus
    assert canvas.store.state.view_state["controller_port_focus"] == list(expected_focus)

    assert canvas.store.undo()
    assert canvas._controller_port_focus == expected_focus
    assert canvas.store.state.view_state["controller_port_focus"] == list(expected_focus)

    assert canvas.store.redo()
    assert canvas._controller_port_focus == expected_focus
    assert canvas.store.state.view_state["controller_port_focus"] == list(expected_focus)

    document_path = tmp_path / "focused-view.machine.json"
    canvas.store.save(document_path)
    restored_state = load_editor_state(document_path)
    assert restored_state.view_state["controller_port_focus"] == list(expected_focus)

    _app()
    restored_canvas = MachineCanvas()
    # Simulate opening the saved document over another active view selection.
    restored_canvas._controller_port_focus = ("__all__", "all", "details")
    restored_canvas.store.state.view_state["controller_port_focus"] = [
        "__all__", "all", "details"
    ]
    restored_canvas.store.load(document_path)
    assert restored_canvas._controller_port_focus == expected_focus
    assert restored_canvas.controller_connector_focus_combo.currentData() == "::".join(expected_focus)
