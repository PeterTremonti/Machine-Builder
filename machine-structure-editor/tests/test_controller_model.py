"""Tests for controller integration into the canonical model."""

import pytest

from machine_builder.controller import Controller
from machine_builder.controller_resource import (
    ControllerResource,
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


def test_controller_can_be_added_to_machine() -> None:
    model = build_model()

    controller = Controller(
        id="controller-1",
        name="Main Controller",
        controller_type="motion_controller",
    )

    model.add_controller(
        "machine-1",
        controller,
    )

    assert (
        model.controllers[
            "controller-1"
        ]
        is controller
    )

    assert (
        model.machines[
            "machine-1"
        ].controller_ids
        == ["controller-1"]
    )


def test_controller_can_be_retrieved() -> None:
    model = build_model()

    controller = Controller(
        id="controller-1",
        name="Main Controller",
        controller_type="motion_controller",
    )

    model.add_controller(
        "machine-1",
        controller,
    )

    assert (
        model.get_controller(
            "controller-1"
        )
        is controller
    )


def test_controller_can_be_removed() -> None:
    model = build_model()

    controller = Controller(
        id="controller-1",
        name="Main Controller",
        controller_type="motion_controller",
    )

    model.add_controller(
        "machine-1",
        controller,
    )

    removed = model.remove_controller(
        "controller-1"
    )

    assert removed is controller

    assert (
        "controller-1"
        not in model.controllers
    )

    assert (
        model.machines[
            "machine-1"
        ].controller_ids
        == []
    )


def test_controller_with_unknown_machine_is_rejected() -> None:
    model = CanonicalMachineModel()

    with pytest.raises(
        ValueError,
        match="Unknown machine",
    ):
        model.add_controller(
            "missing-machine",
            Controller(
                id="controller-1",
                name="Main Controller",
                controller_type="motion_controller",
            ),
        )


def test_duplicate_controller_is_rejected() -> None:
    model = build_model()

    model.add_controller(
        "machine-1",
        Controller(
            id="controller-1",
            name="Main Controller",
            controller_type="motion_controller",
        ),
    )

    with pytest.raises(
        ValueError,
        match="Controller already exists",
    ):
        model.add_controller(
            "machine-1",
            Controller(
                id="controller-1",
                name="Different Controller",
                controller_type="motion_controller",
            ),
        )


def test_unknown_controller_is_rejected_when_retrieved() -> None:
    model = build_model()

    with pytest.raises(
        KeyError,
        match="Unknown controller",
    ):
        model.get_controller(
            "missing-controller"
        )


def test_unknown_controller_is_rejected_when_removed() -> None:
    model = build_model()

    with pytest.raises(
        KeyError,
        match="Unknown controller",
    ):
        model.remove_controller(
            "missing-controller"
        )


def test_controller_resource_requires_known_controller() -> None:
    model = build_model()

    with pytest.raises(
        ValueError,
        match="Unknown controller",
    ):
        model.add_controller_resource(
            "machine-1",
            ControllerResource(
                id="resource-1",
                name="Heater Output 0",
                resource_type="heater_output",
                controller_id="missing-controller",
            ),
        )


def test_controller_resource_can_reference_controller() -> None:
    model = build_model()

    model.add_controller(
        "machine-1",
        Controller(
            id="controller-1",
            name="Main Controller",
            controller_type="motion_controller",
        ),
    )

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

    assert (
        model.get_controller_resource(
            "resource-1"
        ).controller_id
        == "controller-1"
    )


def test_removing_controller_removes_its_resources() -> None:
    model = build_model()

    model.add_controller(
        "machine-1",
        Controller(
            id="controller-1",
            name="Main Controller",
            controller_type="motion_controller",
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

    model.remove_controller(
        "controller-1"
    )

    assert model.controllers == {}
    assert model.controller_resources == {}
    assert (
        model.machines[
            "machine-1"
        ].controller_resource_ids
        == []
    )