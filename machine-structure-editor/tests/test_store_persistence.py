"""Tests for ModelStore persistence integration."""

from pathlib import Path

from machine_builder.controller import Controller
from machine_builder.controller_board_fixtures import (
    DUET_2_MAESTRO_CONNECTOR_LAYOUT,
)
from machine_builder.controller_visual_mutations import (
    CreateDuet2MaestroControllerNode,
)
from machine_builder.hardware_catalog import build_duet_2_maestro
from machine_builder.mutations import CreateNode
from machine_builder.persistence import load_editor_state
from machine_builder.semantic_connection import SemanticConnection
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    HardwareDefinition,
    Machine,
    MachineComponent,
    Provenance,
    SemanticPort,
)
from machine_builder.store import ModelStore
from machine_builder.visual_model import (
    VisualConnection,
    VisualModel,
    VisualNode,
    VisualPort,
)


def test_store_save_preserves_complete_state(
    tmp_path: Path,
) -> None:
    store = ModelStore()

    node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Part Cooling Fan",
        x=120.0,
        y=240.0,
    )

    store.commit(
        CreateNode(
            node
        )
    )

    path = tmp_path / "machine.json"

    store.save(path)

    loaded = load_editor_state(path)

    assert (
        loaded.visual_model.nodes["node-1"].label
        == "Part Cooling Fan"
    )

    assert (
        loaded.visual_model.nodes["node-1"].x
        == 120.0
    )

    assert (
        loaded.visual_model.nodes["node-1"].y
        == 240.0
    )

    assert (
        "component-node-1"
        in loaded.semantic_model.components
    )


def test_store_round_trip_preserves_physical_connection_metadata_and_endpoints(
    tmp_path: Path,
) -> None:
    machine_id = "machine-connection-round-trip"
    definition_source = Provenance(
        source="fixture://controller-board",
        evidence_type="datasheet",
        method="manual_review",
        context="embedded controller hardware definition",
        date="2026-10-09",
        notes="Test provenance; no external catalog lookup is used.",
    )

    semantic_model = CanonicalMachineModel()
    semantic_model.add_machine(
        Machine(
            id=machine_id,
            name="Connection Persistence Test Machine",
        )
    )
    semantic_model.add_hardware_definition(
        HardwareDefinition(
            id="hardware-definition-controller",
            family="controller_board",
            manufacturer="Test Maker",
            variant="board-rev-a",
            properties={
                "interface": "UART",
                "logic_voltage_v": 3.3,
                "contact_count": 4,
            },
            provenance=[definition_source],
        )
    )

    controller = Controller(
        id="controller-round-trip",
        name="Controller Board",
        controller_type="motion_controller",
        hardware_definition_id="hardware-definition-controller",
        properties={"protocol": "UART"},
    )
    semantic_model.add_controller(machine_id, controller)

    component = MachineComponent(
        id="component-round-trip",
        role="temperature_sensor",
        label="Toolhead Sensor",
        properties={"location": "toolhead"},
    )
    semantic_model.add_component(machine_id, component)

    controller_port = SemanticPort(
        id="port-controller-tx",
        component_id=None,
        controller_id=controller.id,
        purpose="UART TX",
        direction="output",
        connector_id="J4",
        pin_id="3",
        properties={"logic_voltage_v": 3.3},
        provenance=[
            Provenance(
                source="fixture://controller-port",
                evidence_type="datasheet",
                notes="Controller-owned physical endpoint.",
            )
        ],
    )
    component_port = SemanticPort(
        id="port-sensor-signal",
        component_id=component.id,
        controller_id=None,
        purpose="Sensor signal",
        direction="input",
        connector_id=None,
        pin_id=None,
        properties={"signal_type": "unknown"},
    )
    semantic_model.add_port(controller_port)
    semantic_model.add_port(component_port)

    semantic_connection = SemanticConnection(
        id="connection-round-trip",
        endpoint_a_id=controller_port.id,
        endpoint_b_id=component_port.id,
        connection_type="electrical",
        properties={
            "wire_color": "blue",
            "harness_id": None,
            "notes": "Recorded during physical inspection.",
        },
    )
    semantic_model.add_connection(semantic_connection)

    visual_model = VisualModel()
    controller_node_id = "visual-controller"
    component_node_id = "visual-sensor"
    visual_controller_port_id = "visual-controller-tx"
    visual_component_port_id = "visual-sensor-signal"

    visual_model.add_node(
        VisualNode(
            id=controller_node_id,
            node_type="controller",
            label="Controller Board",
            semantic_reference=controller.id,
            ports={
                visual_controller_port_id: VisualPort(
                    id=visual_controller_port_id,
                    node_id=controller_node_id,
                    label="TX",
                    port_type="signal",
                    direction="output",
                    semantic_reference=controller_port.id,
                    side="right",
                    order=0,
                )
            },
        )
    )
    visual_model.add_node(
        VisualNode(
            id=component_node_id,
            node_type="sensor",
            label="Toolhead Sensor",
            semantic_reference=component.id,
            ports={
                visual_component_port_id: VisualPort(
                    id=visual_component_port_id,
                    node_id=component_node_id,
                    label="Signal",
                    port_type="signal",
                    direction="input",
                    semantic_reference=component_port.id,
                    side="left",
                    order=0,
                )
            },
        )
    )

    expected_geometry = {
        "points": [
            [10.0, 20.0],
            [10.0, 70.0],
            [40.0, 70.0],
        ],
        "routing_diagnostic": "geometry-only test value",
    }
    visual_model.add_connection(
        VisualConnection(
            id=semantic_connection.id,
            endpoint_a_id=visual_controller_port_id,
            endpoint_b_id=visual_component_port_id,
            connection_type="electrical",
            geometry=expected_geometry.copy(),
        )
    )

    store = ModelStore(
        model=visual_model,
        semantic_model=semantic_model,
    )
    path = tmp_path / "connection-round-trip.machine.json"
    store.save(path)

    reopened = ModelStore()
    reopened.load(path)
    loaded = reopened.state

    definition = loaded.semantic_model.hardware_definitions[
        "hardware-definition-controller"
    ]
    assert definition.family == "controller_board"
    assert definition.manufacturer == "Test Maker"
    assert definition.variant == "board-rev-a"
    assert definition.properties == {
        "interface": "UART",
        "logic_voltage_v": 3.3,
        "contact_count": 4,
    }
    assert definition.provenance == [definition_source]

    restored_machine = loaded.semantic_model.machines[machine_id]
    restored_controller = loaded.semantic_model.controllers[
        controller.id
    ]
    restored_component = loaded.semantic_model.components[
        component.id
    ]
    assert restored_machine.controller_ids == [controller.id]
    assert restored_machine.component_ids == [component.id]
    assert restored_controller.hardware_definition_id == (
        "hardware-definition-controller"
    )
    assert restored_controller.port_ids == [controller_port.id]
    assert restored_component.port_ids == [component_port.id]

    restored_controller_port = loaded.semantic_model.ports[
        controller_port.id
    ]
    restored_component_port = loaded.semantic_model.ports[
        component_port.id
    ]
    assert restored_controller_port.controller_id == controller.id
    assert restored_controller_port.component_id is None
    assert restored_controller_port.connector_id == "J4"
    assert restored_controller_port.pin_id == "3"
    assert restored_controller_port.properties == {
        "logic_voltage_v": 3.3
    }
    assert restored_component_port.component_id == component.id
    assert restored_component_port.controller_id is None
    assert restored_component_port.connector_id is None
    assert restored_component_port.pin_id is None

    restored_connection = loaded.semantic_model.connections[
        "connection-round-trip"
    ]
    assert isinstance(restored_connection, SemanticConnection)
    assert restored_connection.id == semantic_connection.id
    assert {
        restored_connection.endpoint_a_id,
        restored_connection.endpoint_b_id,
    } == {controller_port.id, component_port.id}
    assert restored_connection.properties == {
        "wire_color": "blue",
        "harness_id": None,
        "notes": "Recorded during physical inspection.",
    }

    restored_visual_connection = loaded.visual_model.connections[
        "connection-round-trip"
    ]
    assert isinstance(restored_visual_connection, VisualConnection)
    assert restored_visual_connection.endpoint_a_id == (
        visual_controller_port_id
    )
    assert restored_visual_connection.endpoint_b_id == (
        visual_component_port_id
    )
    assert restored_visual_connection.geometry == expected_geometry
    assert {
        "wire_color",
        "harness_id",
        "notes",
    }.isdisjoint(restored_visual_connection.geometry)

def test_store_save_does_not_change_history(
    tmp_path: Path,
) -> None:
    store = ModelStore()

    store.commit(
        CreateNode(
            VisualNode(
                id="node-1",
                node_type="fan",
                label="Fan",
            )
        )
    )

    assert store.can_undo
    assert not store.can_redo

    path = tmp_path / "machine.json"

    store.save(path)

    assert store.can_undo
    assert not store.can_redo


def test_store_load_replaces_complete_state(
    tmp_path: Path,
) -> None:
    source = ModelStore()

    source.commit(
        CreateNode(
            VisualNode(
                id="saved-node",
                node_type="heater",
                label="Saved Heater",
                x=50.0,
                y=75.0,
            )
        )
    )

    path = tmp_path / "machine.json"
    source.save(path)

    target = ModelStore()

    target.commit(
        CreateNode(
            VisualNode(
                id="old-node",
                node_type="fan",
                label="Old Fan",
            )
        )
    )

    assert "old-node" in target.model.nodes
    assert target.can_undo

    target.load(path)

    assert "saved-node" in target.model.nodes
    assert "old-node" not in target.model.nodes

    assert (
        target.model.nodes[
            "saved-node"
        ].label
        == "Saved Heater"
    )

    assert (
        target.semantic_model.components[
            "component-saved-node"
        ].label
        == "Saved Heater"
    )


def test_store_load_clears_history(
    tmp_path: Path,
) -> None:
    source = ModelStore()

    source.commit(
        CreateNode(
            VisualNode(
                id="saved-node",
                node_type="motor",
                label="Saved Motor",
            )
        )
    )

    path = tmp_path / "machine.json"
    source.save(path)

    target = ModelStore()

    target.commit(
        CreateNode(
            VisualNode(
                id="old-node",
                node_type="fan",
                label="Old Fan",
            )
        )
    )

    assert target.can_undo

    target.load(path)

    assert not target.can_undo
    assert not target.can_redo

    assert not target.undo()


def test_store_load_notifies_listeners(
    tmp_path: Path,
) -> None:
    source = ModelStore()

    source.commit(
        CreateNode(
            VisualNode(
                id="saved-node",
                node_type="heater",
                label="Saved Heater",
            )
        )
    )

    path = tmp_path / "machine.json"
    source.save(path)

    target = ModelStore()

    notifications: list[object] = []

    def listener(model: object) -> None:
        notifications.append(model)

    target.subscribe(listener)

    target.load(path)

    assert len(notifications) == 1
    assert notifications[0] is target.model


def test_store_save_creates_parent_directory(
    tmp_path: Path,
) -> None:
    store = ModelStore()

    path = (
        tmp_path
        / "projects"
        / "machine"
        / "machine.json"
    )

    store.save(path)

    assert path.exists()

def test_maestro_controller_round_trips_with_definition_ports_and_visual_links(
    tmp_path: Path,
) -> None:
    store = ModelStore()
    controller_id = "promega-maestro-controller"
    visual_node_id = "promega-maestro-visual-node"

    node = VisualNode(
        id=visual_node_id,
        node_type="controller",
        label="Duet 2 Maestro v1.0",
        x=144.0,
        y=288.0,
    )
    store.commit(
        CreateDuet2MaestroControllerNode(
            controller_id=controller_id,
            node=node,
        )
    )

    before_controller = store.semantic_model.controllers[controller_id]
    before_definition = store.semantic_model.hardware_definitions[
        "duet-2-maestro-v1-0"
    ]
    expected_definition = build_duet_2_maestro()
    expected_port_provenance = {
        port_id: store.semantic_model.ports[port_id].provenance.copy()
        for port_id in before_controller.port_ids
    }
    expected_port_connector_pin = {
        port_id: (
            store.semantic_model.ports[port_id].connector_id,
            store.semantic_model.ports[port_id].pin_id,
        )
        for port_id in before_controller.port_ids
    }
    expected_visual_references = {
        visual_port.id: visual_port.semantic_reference
        for visual_port in store.model.nodes[visual_node_id].ports.values()
    }
    expected_port_count = sum(
        position_count
        for _connector_id, _connector_name, position_count
        in DUET_2_MAESTRO_CONNECTOR_LAYOUT
    )

    path = tmp_path / "promega-maestro-reference-specimen.machine.json"
    store.save(path)

    reopened = ModelStore()
    reopened.load(path)
    loaded = reopened.state
    semantic_model = loaded.semantic_model

    assert set(semantic_model.hardware_definitions) == {
        "duet-2-maestro-v1-0"
    }
    definition = semantic_model.hardware_definitions[
        "duet-2-maestro-v1-0"
    ]
    assert definition.id == before_definition.id
    assert definition.family == expected_definition.family
    assert definition.manufacturer == expected_definition.manufacturer
    assert definition.variant == expected_definition.variant
    assert definition.provenance
    assert definition.provenance == expected_definition.provenance
    assert definition.properties["processor"] == (
        expected_definition.properties["processor"]
    )
    assert "connector_specifications" in definition.properties

    machine = semantic_model.machines["machine-1"]
    assert machine.name == (
        "M3D Promega \u2014 Compound reference specimen "
        "(not verified as-built)"
    )
    assert machine.controller_ids == [controller_id]

    controller = semantic_model.controllers[controller_id]
    assert controller.id == controller_id
    assert controller.hardware_definition_id == definition.id
    assert controller.name == "Duet 2 Maestro v1.0"
    assert controller.controller_type == "motion_controller"
    assert controller.version is None
    assert controller.properties["physical_revision_status"] == (
        "not_verified_as_built"
    )
    assert len(controller.port_ids) == expected_port_count
    assert len(set(controller.port_ids)) == expected_port_count

    restored_ports = [
        semantic_model.ports[port_id]
        for port_id in controller.port_ids
    ]
    assert {
        port.id: (port.connector_id, port.pin_id)
        for port in restored_ports
    } == expected_port_connector_pin
    assert all(
        port.controller_id == controller_id
        and port.component_id is None
        for port in restored_ports
    )
    assert {
        port_id: semantic_model.ports[port_id].provenance
        for port_id in controller.port_ids
    } == expected_port_provenance

    j4_ports = [
        port
        for port in restored_ports
        if port.connector_id == "j4"
    ]
    assert len(j4_ports) == 4
    assert {port.pin_id for port in j4_ports} == {
        "1",
        "2",
        "3",
        "4",
    }

    visual_node = loaded.visual_model.nodes[visual_node_id]
    assert visual_node.node_type == "controller"
    assert visual_node.semantic_reference == controller_id
    assert visual_node.label == "Duet 2 Maestro v1.0"
    assert visual_node.x == 144.0
    assert visual_node.y == 288.0
    assert len(visual_node.ports) == expected_port_count
    assert {
        visual_port.id: visual_port.semantic_reference
        for visual_port in visual_node.ports.values()
    } == expected_visual_references
    assert {
        visual_port.semantic_reference
        for visual_port in visual_node.ports.values()
    } == set(controller.port_ids)
    assert set(visual_node.ports).isdisjoint(set(controller.port_ids))
