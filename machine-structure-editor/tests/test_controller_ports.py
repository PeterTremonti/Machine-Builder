import pytest

from machine_builder.controller import Controller
from machine_builder.editor_state import EditorState
from machine_builder.persistence import (
    deserialize_editor_state,
    serialize_editor_state,
)
from machine_builder.semantic_connection import SemanticConnection
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
    SemanticPort,
)
from machine_builder.visual_model import VisualModel


def make_model() -> CanonicalMachineModel:
    model = CanonicalMachineModel()
    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )
    return model


def add_controller(
    model: CanonicalMachineModel,
) -> Controller:
    controller = Controller(
        id="controller-1",
        name="Duet 2 Maestro",
        controller_type="motion_controller",
    )
    model.add_controller(
        "machine-1",
        controller,
    )
    return controller


def test_controller_can_own_semantic_port() -> None:
    model = make_model()
    controller = add_controller(model)

    port = SemanticPort(
        id="controller-1-bedheat",
        component_id=None,
        purpose="Heater output",
        direction="output",
        connector_id="bed-heater-connector",
        pin_id="1",
        controller_id=controller.id,
    )

    model.add_port(port)

    assert model.ports[port.id] is port
    assert controller.port_ids == [
        "controller-1-bedheat"
    ]


def test_semantic_port_requires_exactly_one_owner() -> None:
    model = make_model()
    controller = add_controller(model)

    with pytest.raises(
        ValueError,
        match="exactly one owner",
    ):
        model.add_port(
            SemanticPort(
                id="port-no-owner",
                component_id=None,
                purpose="unknown",
            )
        )

    with pytest.raises(
        ValueError,
        match="exactly one owner",
    ):
        model.add_port(
            SemanticPort(
                id="port-two-owners",
                component_id="component-1",
                purpose="unknown",
                controller_id=controller.id,
            )
        )


def test_controller_owned_port_can_be_connection_endpoint() -> None:
    model = make_model()
    controller = add_controller(model)

    model.add_component(
        "machine-1",
        MachineComponent(
            id="component-1",
            role="Test Load",
        ),
    )

    controller_port = SemanticPort(
        id="controller-1-output",
        component_id=None,
        purpose="Power",
        direction="output",
        controller_id=controller.id,
    )

    component_port = SemanticPort(
        id="component-1-input",
        component_id="component-1",
        purpose="Power",
        direction="input",
    )

    model.add_port(controller_port)
    model.add_port(component_port)

    connection = SemanticConnection(
        id="connection-1",
        endpoint_a_id=controller_port.id,
        endpoint_b_id=component_port.id,
        connection_type="electrical",
    )

    model.add_connection(connection)

    assert model.connections[
        "connection-1"
    ] is connection


def test_controller_owned_port_round_trips_through_persistence() -> None:
    model = make_model()
    controller = add_controller(model)

    model.add_port(
        SemanticPort(
            id="controller-1-port",
            component_id=None,
            purpose="Endstop",
            direction="input",
            connector_id="x-endstop",
            pin_id="signal",
            controller_id=controller.id,
        )
    )

    state = EditorState(
        visual_model=VisualModel(),
        semantic_model=model,
    )

    restored = deserialize_editor_state(
        serialize_editor_state(state)
    )

    restored_controller = (
        restored.semantic_model.controllers[
            controller.id
        ]
    )
    restored_port = (
        restored.semantic_model.ports[
            "controller-1-port"
        ]
    )

    assert restored_controller.port_ids == [
        "controller-1-port"
    ]
    assert restored_port.component_id is None
    assert restored_port.controller_id == controller.id
    assert restored_port.connector_id == "x-endstop"
    assert restored_port.pin_id == "signal"