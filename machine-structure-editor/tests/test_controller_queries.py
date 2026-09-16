import pytest

from machine_builder.controller import Controller
from machine_builder.controller_queries import (
    controller_resources_for_controller,
    controller_resources_for_machine,
    controller_resources_of_type,
    controllers_for_machine,
)
from machine_builder.controller_resource import ControllerResource
from machine_builder.semantic_model import CanonicalMachineModel, Machine


def build_model() -> CanonicalMachineModel:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    model.add_controller(
        "machine-1",
        Controller(
            id="controller-1",
            name="Primary Controller",
            controller_type="test",
        ),
    )

    model.add_controller(
        "machine-1",
        Controller(
            id="controller-2",
            name="Secondary Controller",
            controller_type="test",
        ),
    )

    model.add_controller_resource(
        "machine-1",
        ControllerResource(
            id="resource-1",
            name="Heater Output 0",
            resource_type="heater_output",
            controller_id="controller-1",
        ),
    )

    model.add_controller_resource(
        "machine-1",
        ControllerResource(
            id="resource-2",
            name="Fan Output 0",
            resource_type="fan_output",
            controller_id="controller-1",
        ),
    )

    model.add_controller_resource(
        "machine-1",
        ControllerResource(
            id="resource-3",
            name="Stepper X",
            resource_type="stepper_output",
            controller_id="controller-2",
        ),
    )

    return model


def test_controllers_for_machine() -> None:
    model = build_model()

    controllers = controllers_for_machine(
        model,
        "machine-1",
    )

    assert [controller.id for controller in controllers] == [
        "controller-1",
        "controller-2",
    ]


def test_controllers_for_unknown_machine_is_rejected() -> None:
    model = build_model()

    with pytest.raises(KeyError):
        controllers_for_machine(
            model,
            "unknown-machine",
        )


def test_controller_resources_for_controller() -> None:
    model = build_model()

    resources = controller_resources_for_controller(
        model,
        "controller-1",
    )

    assert [resource.id for resource in resources] == [
        "resource-1",
        "resource-2",
    ]


def test_controller_resources_for_unknown_controller_is_rejected() -> None:
    model = build_model()

    with pytest.raises(KeyError):
        controller_resources_for_controller(
            model,
            "unknown-controller",
        )


def test_controller_resources_for_machine() -> None:
    model = build_model()

    resources = controller_resources_for_machine(
        model,
        "machine-1",
    )

    assert [resource.id for resource in resources] == [
        "resource-1",
        "resource-2",
        "resource-3",
    ]


def test_controller_resources_of_type() -> None:
    model = build_model()

    resources = controller_resources_of_type(
        model,
        "heater_output",
    )

    assert [resource.id for resource in resources] == [
        "resource-1",
    ]


def test_controller_resources_of_unknown_type_are_empty() -> None:
    model = build_model()

    resources = controller_resources_of_type(
        model,
        "probe_input",
    )

    assert resources == []