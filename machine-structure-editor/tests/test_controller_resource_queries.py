import pytest

from machine_builder.controller import Controller
from machine_builder.controller_resource import ControllerResource
from machine_builder.controller_resource_queries import (
    controller_for_resource,
    get_controller_resource,
    machine_id_for_controller_resource,
    resources_for_controller,
    resources_for_machine,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
)


def make_model() -> CanonicalMachineModel:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Machine One",
        )
    )

    model.add_machine(
        Machine(
            id="machine-2",
            name="Machine Two",
        )
    )

    model.add_controller(
        "machine-1",
        Controller(
            id="controller-1",
            name="Controller One",
            controller_type="test",
        ),
    )

    model.add_controller(
        "machine-2",
        Controller(
            id="controller-2",
            name="Controller Two",
            controller_type="test",
        ),
    )

    model.add_controller_resource(
        "machine-1",
        ControllerResource(
            id="resource-1",
            name="Heater",
            resource_type="heater",
            controller_id="controller-1",
        ),
    )

    model.add_controller_resource(
        "machine-1",
        ControllerResource(
            id="resource-2",
            name="Fan",
            resource_type="fan",
            controller_id=None,
        ),
    )

    model.add_controller_resource(
        "machine-2",
        ControllerResource(
            id="resource-3",
            name="Motor",
            resource_type="motor",
            controller_id="controller-2",
        ),
    )

    return model


def test_get_controller_resource():
    model = make_model()

    resource = get_controller_resource(
        model,
        "resource-1",
    )

    assert resource.name == "Heater"


def test_get_controller_resource_rejects_unknown():
    model = make_model()

    with pytest.raises(KeyError):
        get_controller_resource(
            model,
            "missing",
        )


def test_machine_id_for_controller_resource():
    model = make_model()

    assert (
        machine_id_for_controller_resource(
            model,
            "resource-1",
        )
        == "machine-1"
    )


def test_machine_id_for_unassigned_controller_resource():
    model = make_model()

    assert (
        machine_id_for_controller_resource(
            model,
            "resource-2",
        )
        == "machine-1"
    )


def test_machine_id_for_unknown_resource():
    model = make_model()

    with pytest.raises(KeyError):
        machine_id_for_controller_resource(
            model,
            "missing",
        )


def test_controller_for_resource():
    model = make_model()

    controller = controller_for_resource(
        model,
        "resource-1",
    )

    assert controller is not None
    assert controller.id == "controller-1"


def test_controller_for_unassigned_resource():
    model = make_model()

    assert (
        controller_for_resource(
            model,
            "resource-2",
        )
        is None
    )


def test_resources_for_controller():
    model = make_model()

    resources = resources_for_controller(
        model,
        "controller-1",
    )

    assert [
        resource.id
        for resource in resources
    ] == ["resource-1"]


def test_resources_for_machine():
    model = make_model()

    resources = resources_for_machine(
        model,
        "machine-1",
    )

    assert {
        resource.id
        for resource in resources
    } == {
        "resource-1",
        "resource-2",
    }


def test_resources_for_unknown_machine():
    model = make_model()

    with pytest.raises(KeyError):
        resources_for_machine(
            model,
            "missing",
        )