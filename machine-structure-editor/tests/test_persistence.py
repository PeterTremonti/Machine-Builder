from pathlib import Path

import pytest

from machine_builder.controller import Controller
from machine_builder.controller_resource import ControllerResource
from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)
from machine_builder.editor_state import EditorState
from machine_builder.persistence import (
    FORMAT_NAME,
    FORMAT_VERSION,
    deserialize_editor_state,
    load_editor_state,
    save_editor_state,
    serialize_editor_state,
)
from machine_builder.semantic_capability import Capability
from machine_builder.semantic_connection import SemanticConnection
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
    SemanticPort,
)
from machine_builder.semantic_relationship import (
    SemanticRelationship,
)
from machine_builder.semantic_value import (
    SemanticValue,
    SemanticValueStatus,
)
from machine_builder.visual_model import (
    VisualConnection,
    VisualModel,
    VisualNode,
    VisualPort,
)


def build_state() -> EditorState:
    semantic_model = CanonicalMachineModel()

    semantic_model.add_machine(
        Machine(
            id="machine-1",
            name="Persistence Test Machine",
            properties={
                "purpose": "round_trip",
            },
        )
    )

    semantic_model.add_component(
        "machine-1",
        MachineComponent(
            id="component-1",
            role="Heater",
            label="Chamber Heater",
            properties={
                "power": SemanticValue(
                    status=SemanticValueStatus.MEASURED,
                    value=400,
                ),
            },
        ),
    )

    semantic_model.add_port(
        SemanticPort(
            id="port-heater",
            component_id="component-1",
            purpose="Power",
            direction="input",
        )
    )

    semantic_model.add_component(
        "machine-1",
        MachineComponent(
            id="component-2",
            role="Temperature Sensor",
            label="Chamber Thermistor",
        ),
    )

    semantic_model.add_port(
        SemanticPort(
            id="port-thermistor",
            component_id="component-2",
            purpose="Temperature",
            direction="input",
        )
    )

    semantic_model.add_capability(
        "machine-1",
        Capability(
            id="capability-1",
            name="Chamber Heating",
            description="Heat the machine chamber.",
        ),
    )

    semantic_model.add_controller(
        "machine-1",
        Controller(
            id="controller-1",
            name="BTT Octopus V1.1",
            controller_type="motion_controller",
            version="V1.1",
            properties={
                "manufacturer": "BigTreeTech",
            },
        ),
    )

    semantic_model.add_controller_resource(
        "machine-1",
        ControllerResource(
            id="resource-heater",
            name="Heater Output 0",
            resource_type="heater_output",
            controller_id="controller-1",
        ),
    )

    semantic_model.add_controller_resource_assignment(
        "machine-1",
        ControllerResourceAssignment(
            id="assignment-heater",
            source_id="component-1",
            resource_id="resource-heater",
            assignment_type="controls",
            properties={
                "semantic_role": "heater",
            },
        ),
    )

    semantic_model.connections[
        "connection-1"
    ] = SemanticConnection(
        id="connection-1",
        endpoint_a_id="port-heater",
        endpoint_b_id="port-thermistor",
        connection_type="test",
    )

    semantic_model.relationships[
        "relationship-1"
    ] = SemanticRelationship(
        id="relationship-1",
        source_id="component-1",
        target_id="capability-1",
        relationship_type="participates_in",
    )

    visual_model = VisualModel()

    heater_node = VisualNode(
        id="node-heater",
        node_type="heater",
        label="Chamber Heater",
        x=125.0,
        y=250.0,
        width=220.0,
        height=120.0,
        semantic_reference="component-1",
        properties={
            "ui_state": "expanded",
        },
    )
    heater_node.add_port(
        VisualPort(
            id="visual-port-heater",
            node_id="node-heater",
            label="Power",
            port_type="power",
            direction="input",
            semantic_reference="port-heater",
            side="left",
            order=0,
        )
    )

    sensor_node = VisualNode(
        id="node-sensor",
        node_type="sensor",
        label="Chamber Thermistor",
        x=500.0,
        y=250.0,
        semantic_reference="component-2",
    )
    sensor_node.add_port(
        VisualPort(
            id="visual-port-sensor",
            node_id="node-sensor",
            label="Temperature",
            port_type="temperature",
            direction="input",
            semantic_reference="port-thermistor",
            side="right",
            order=0,
        )
    )

    visual_model.add_node(
        heater_node
    )
    visual_model.add_node(
        sensor_node
    )

    visual_model.connections[
        "visual-connection-1"
    ] = VisualConnection(
        id="visual-connection-1",
        endpoint_a_id="visual-port-heater",
        endpoint_b_id="visual-port-sensor",
        connection_type="wire",
        geometry={
            "points": [
                [220.0, 310.0],
                [500.0, 310.0],
            ],
        },
    )

    return EditorState(
        visual_model=visual_model,
        semantic_model=semantic_model,
    )


def test_serialize_editor_state_has_file_format_metadata() -> None:
    document = serialize_editor_state(
        build_state()
    )

    assert document["format"] == FORMAT_NAME
    assert document["format_version"] == FORMAT_VERSION
    assert "state" in document


def test_serialize_editor_state_contains_both_models() -> None:
    document = serialize_editor_state(
        build_state()
    )

    state = document["state"]

    assert state["__type__"].endswith(
        ".EditorState"
    )

    fields = state["fields"]

    assert "visual_model" in fields
    assert "semantic_model" in fields


def test_round_trip_preserves_machine() -> None:
    original = build_state()

    restored = deserialize_editor_state(
        serialize_editor_state(
            original
        )
    )

    machine = restored.semantic_model.machines[
        "machine-1"
    ]

    assert machine.name == (
        "Persistence Test Machine"
    )
    assert machine.properties[
        "purpose"
    ] == "round_trip"


def test_round_trip_preserves_components_and_ports() -> None:
    original = build_state()

    restored = deserialize_editor_state(
        serialize_editor_state(
            original
        )
    )

    assert set(
        restored.semantic_model.components
    ) == {
        "component-1",
        "component-2",
    }

    assert (
        restored.semantic_model.components[
            "component-1"
        ].port_ids
        == ["port-heater"]
    )

    assert (
        restored.semantic_model.components[
            "component-2"
        ].port_ids
        == ["port-thermistor"]
    )


def test_round_trip_preserves_semantic_value() -> None:
    restored = deserialize_editor_state(
        serialize_editor_state(
            build_state()
        )
    )

    value = restored.semantic_model.components[
        "component-1"
    ].properties["power"]

    assert isinstance(
        value,
        SemanticValue,
    )
    assert value.status is (
        SemanticValueStatus.MEASURED
    )
    assert value.value == 400


def test_round_trip_preserves_controller_resource_assignment() -> None:
    restored = deserialize_editor_state(
        serialize_editor_state(
            build_state()
        )
    )

    assignment = (
        restored.semantic_model
        .controller_resource_assignments[
            "assignment-heater"
        ]
    )

    assert assignment.source_id == (
        "component-1"
    )
    assert assignment.resource_id == (
        "resource-heater"
    )
    assert assignment.assignment_type == (
        "controls"
    )


def test_round_trip_preserves_connections_and_relationships() -> None:
    restored = deserialize_editor_state(
        serialize_editor_state(
            build_state()
        )
    )

    connection = (
        restored.semantic_model
        .connections["connection-1"]
    )

    relationship = (
        restored.semantic_model
        .relationships["relationship-1"]
    )

    assert isinstance(
        connection,
        SemanticConnection,
    )
    assert connection.endpoint_a_id == (
        "port-heater"
    )
    assert connection.endpoint_b_id == (
        "port-thermistor"
    )

    assert isinstance(
        relationship,
        SemanticRelationship,
    )
    assert relationship.source_id == (
        "component-1"
    )
    assert relationship.target_id == (
        "capability-1"
    )


def test_round_trip_preserves_visual_geometry() -> None:
    restored = deserialize_editor_state(
        serialize_editor_state(
            build_state()
        )
    )

    node = restored.visual_model.nodes[
        "node-heater"
    ]

    connection = restored.visual_model.connections[
        "visual-connection-1"
    ]

    assert node.x == 125.0
    assert node.y == 250.0
    assert node.width == 220.0
    assert node.height == 120.0

    assert connection.geometry[
        "points"
    ] == [
        [220.0, 310.0],
        [500.0, 310.0],
    ]


def test_round_trip_preserves_visual_semantic_reference() -> None:
    restored = deserialize_editor_state(
        serialize_editor_state(
            build_state()
        )
    )

    node = restored.visual_model.nodes[
        "node-heater"
    ]
    port = node.ports[
        "visual-port-heater"
    ]

    assert node.semantic_reference == (
        "component-1"
    )
    assert port.semantic_reference == (
        "port-heater"
    )


def test_save_and_load_round_trip(tmp_path: Path) -> None:
    original = build_state()
    destination = (
        tmp_path / "test-machine.json"
    )

    save_editor_state(
        original,
        destination,
    )

    restored = load_editor_state(
        destination,
    )

    assert (
        restored.semantic_model.machines[
            "machine-1"
        ].name
        == "Persistence Test Machine"
    )

    assert (
        restored.visual_model.nodes[
            "node-heater"
        ].label
        == "Chamber Heater"
    )


def test_save_creates_parent_directory(tmp_path: Path) -> None:
    destination = (
        tmp_path
        / "nested"
        / "projects"
        / "machine.json"
    )

    save_editor_state(
        build_state(),
        destination,
    )

    assert destination.exists()


def test_save_replaces_existing_file(tmp_path: Path) -> None:
    destination = (
        tmp_path / "machine.json"
    )

    save_editor_state(
        build_state(),
        destination,
    )

    first_text = destination.read_text(
        encoding="utf-8"
    )

    save_editor_state(
        build_state(),
        destination,
    )

    second_text = destination.read_text(
        encoding="utf-8"
    )

    assert second_text == first_text


def test_invalid_format_is_rejected() -> None:
    document = serialize_editor_state(
        build_state()
    )

    document["format"] = (
        "not-machine-builder"
    )

    with pytest.raises(
        ValueError,
        match="Unsupported Machine Builder persistence format",
    ):
        deserialize_editor_state(
            document
        )


def test_invalid_version_is_rejected() -> None:
    document = serialize_editor_state(
        build_state()
    )

    document["format_version"] = 999

    with pytest.raises(
        ValueError,
        match="Unsupported Machine Builder persistence version",
    ):
        deserialize_editor_state(
            document
        )


def test_unknown_dataclass_type_is_rejected() -> None:
    document = serialize_editor_state(
        build_state()
    )

    state = document["state"]

    state["fields"]["semantic_model"] = {
        "__type__": "machine_builder.not_real.FakeModel",
        "fields": {},
    }

    with pytest.raises(
        ValueError,
        match="Unsupported persisted dataclass type",
    ):
        deserialize_editor_state(
            document
        )


def test_invalid_json_file_is_rejected(tmp_path: Path) -> None:
    destination = (
        tmp_path / "broken.json"
    )

    destination.write_text(
        "{ definitely not json",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Invalid Machine Builder JSON file",
    ):
        load_editor_state(
            destination
        )


def test_save_does_not_leave_temporary_file(tmp_path: Path) -> None:
    destination = (
        tmp_path / "machine.json"
    )

    save_editor_state(
        build_state(),
        destination,
    )

    temporary = Path(
        str(destination) + ".tmp"
    )

    assert not temporary.exists()