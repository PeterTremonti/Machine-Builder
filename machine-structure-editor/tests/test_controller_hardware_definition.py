import pytest

from machine_builder.controller import Controller
from machine_builder.editor_state import EditorState
from machine_builder.persistence import (
    deserialize_editor_state,
    serialize_editor_state,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    HardwareDefinition,
    Machine,
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


def test_controller_can_reference_hardware_definition() -> None:
    model = make_model()

    hardware = HardwareDefinition(
        id="duet-2-maestro-v1-0",
        family="Duet 2 Maestro",
    )
    model.add_hardware_definition(hardware)

    controller = Controller(
        id="controller-1",
        name="Duet 2 Maestro",
        controller_type="motion_controller",
        version="1.0",
        hardware_definition_id=hardware.id,
    )

    model.add_controller(
        "machine-1",
        controller,
    )

    assert (
        model.controllers[
            "controller-1"
        ].hardware_definition_id
        == "duet-2-maestro-v1-0"
    )


def test_controller_rejects_unknown_hardware_definition() -> None:
    model = make_model()

    controller = Controller(
        id="controller-1",
        name="Duet 2 Maestro",
        controller_type="motion_controller",
        hardware_definition_id="missing-hardware",
    )

    with pytest.raises(
        ValueError,
        match="Unknown hardware definition",
    ):
        model.add_controller(
            "machine-1",
            controller,
        )


def test_controller_hardware_definition_round_trips_through_persistence() -> None:
    model = make_model()

    model.add_hardware_definition(
        HardwareDefinition(
            id="duet-2-maestro-v1-0",
            family="Duet 2 Maestro",
        )
    )

    model.add_controller(
        "machine-1",
        Controller(
            id="controller-1",
            name="Duet 2 Maestro",
            controller_type="motion_controller",
            hardware_definition_id="duet-2-maestro-v1-0",
        ),
    )

    state = EditorState(
        visual_model=VisualModel(),
        semantic_model=model,
    )

    restored = deserialize_editor_state(
        serialize_editor_state(state)
    )

    assert (
        restored.semantic_model.controllers[
            "controller-1"
        ].hardware_definition_id
        == "duet-2-maestro-v1-0"
    )