from machine_builder.controller_fixtures import (
    add_generic_octopus_controller,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
)


def build_model() -> CanonicalMachineModel:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    return model


def test_generic_octopus_controller_is_added() -> None:
    model = build_model()

    controller = add_generic_octopus_controller(
        model,
        "machine-1",
    )

    assert controller.id == "octopus-v1-1"
    assert controller.name == "BTT Octopus V1.1"
    assert controller.controller_type == "motion_controller"
    assert controller.version == "V1.1"


def test_generic_octopus_controller_is_associated_with_machine() -> None:
    model = build_model()

    add_generic_octopus_controller(
        model,
        "machine-1",
    )

    machine = model.machines["machine-1"]

    assert machine.controller_ids == [
        "octopus-v1-1",
    ]


def test_generic_octopus_controller_creates_expected_resources() -> None:
    model = build_model()

    add_generic_octopus_controller(
        model,
        "machine-1",
    )

    resources = list(
        model.controller_resources.values()
    )

    assert len(resources) == 7

    assert {
        resource.resource_type
        for resource in resources
    } == {
        "stepper_output",
        "heater_output",
        "temperature_input",
        "fan_output",
    }


def test_generic_octopus_contains_stepper_resources() -> None:
    model = build_model()

    add_generic_octopus_controller(
        model,
        "machine-1",
    )

    stepper_resources = [
        resource
        for resource in model.controller_resources.values()
        if resource.resource_type == "stepper_output"
    ]

    assert [
        resource.name
        for resource in stepper_resources
    ] == [
        "Stepper X",
        "Stepper Y",
        "Stepper Z",
        "Stepper E",
    ]


def test_generic_octopus_contains_heater_temperature_and_fan_resources() -> None:
    model = build_model()

    add_generic_octopus_controller(
        model,
        "machine-1",
    )

    assert (
        "octopus-v1-1-heater-0"
        in model.controller_resources
    )

    assert (
        "octopus-v1-1-thermistor-0"
        in model.controller_resources
    )

    assert (
        "octopus-v1-1-fan-0"
        in model.controller_resources
    )


def test_generic_octopus_resources_reference_controller() -> None:
    model = build_model()

    add_generic_octopus_controller(
        model,
        "machine-1",
    )

    assert all(
        resource.controller_id == "octopus-v1-1"
        for resource in model.controller_resources.values()
    )
