import pytest

from machine_builder.controller import Controller
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
            name="Test Controller",
            controller_type="test",
        ),
    )

    return model


def test_controller_resource_can_be_added_to_machine() -> None:
    model = build_model()

    resource = ControllerResource(
        id="resource-1",
        name="Heater Output 0",
        resource_type="heater_output",
        controller_id="controller-1",
    )

    model.add_controller_resource(
        "machine-1",
        resource,
    )

    assert model.get_controller_resource("resource-1") is resource


def test_controller_resource_can_be_added_without_controller() -> None:
    model = build_model()

    resource = ControllerResource(
        id="resource-1",
        name="Generic Output",
        resource_type="generic_output",
    )

    model.add_controller_resource(
        "machine-1",
        resource,
    )

    assert model.get_controller_resource("resource-1") is resource


def test_duplicate_controller_resource_is_rejected() -> None:
    model = build_model()

    resource = ControllerResource(
        id="resource-1",
        name="Heater Output 0",
        resource_type="heater_output",
        controller_id="controller-1",
    )

    model.add_controller_resource("machine-1", resource)

    with pytest.raises(ValueError):
        model.add_controller_resource("machine-1", resource)


def test_unknown_machine_is_rejected() -> None:
    model = build_model()

    resource = ControllerResource(
        id="resource-1",
        name="Heater Output 0",
        resource_type="heater_output",
        controller_id="controller-1",
    )

    with pytest.raises(ValueError):
        model.add_controller_resource(
            "unknown-machine",
            resource,
        )


def test_unknown_controller_is_rejected() -> None:
    model = build_model()

    resource = ControllerResource(
        id="resource-1",
        name="Heater Output 0",
        resource_type="heater_output",
        controller_id="unknown-controller",
    )

    with pytest.raises(ValueError):
        model.add_controller_resource(
            "machine-1",
            resource,
        )


def test_controller_resource_can_be_retrieved() -> None:
    model = build_model()

    resource = ControllerResource(
        id="resource-1",
        name="Heater Output 0",
        resource_type="heater_output",
        controller_id="controller-1",
    )

    model.add_controller_resource("machine-1", resource)

    retrieved = model.get_controller_resource("resource-1")

    assert retrieved is not None
    assert retrieved.id == "resource-1"
    assert retrieved.name == "Heater Output 0"


def test_controller_resource_can_be_removed() -> None:
    model = build_model()

    resource = ControllerResource(
        id="resource-1",
        name="Heater Output 0",
        resource_type="heater_output",
        controller_id="controller-1",
    )

    model.add_controller_resource("machine-1", resource)

    removed = model.remove_controller_resource("resource-1")

    assert removed is resource

    with pytest.raises(KeyError):
        model.get_controller_resource("resource-1")


def test_removing_controller_removes_its_resources() -> None:
    model = build_model()

    resource = ControllerResource(
        id="resource-1",
        name="Heater Output 0",
        resource_type="heater_output",
        controller_id="controller-1",
    )

    model.add_controller_resource("machine-1", resource)

    model.remove_controller("controller-1")

    with pytest.raises(KeyError):
        model.get_controller("controller-1")

    with pytest.raises(KeyError):
        model.get_controller_resource("resource-1")