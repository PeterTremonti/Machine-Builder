import pytest

from machine_builder.controller import Controller
from machine_builder.semantic_model import CanonicalMachineModel, Machine


def build_model() -> CanonicalMachineModel:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    return model


def test_controller_is_associated_with_machine_when_added() -> None:
    model = build_model()

    controller = Controller(
        id="controller-1",
        name="Test Controller",
        controller_type="test",
    )

    model.add_controller(
        "machine-1",
        controller,
    )

    machine = model.machines["machine-1"]

    assert controller.id in machine.controller_ids


def test_machine_can_have_multiple_controllers() -> None:
    model = build_model()

    first = Controller(
        id="controller-1",
        name="Primary Controller",
        controller_type="test",
    )

    second = Controller(
        id="controller-2",
        name="Secondary Controller",
        controller_type="test",
    )

    model.add_controller("machine-1", first)
    model.add_controller("machine-1", second)

    machine = model.machines["machine-1"]

    assert machine.controller_ids == [
        "controller-1",
        "controller-2",
    ]


def test_duplicate_controller_is_rejected() -> None:
    model = build_model()

    controller = Controller(
        id="controller-1",
        name="Test Controller",
        controller_type="test",
    )

    model.add_controller(
        "machine-1",
        controller,
    )

    with pytest.raises(ValueError):
        model.add_controller(
            "machine-1",
            controller,
        )


def test_controller_cannot_be_added_to_unknown_machine() -> None:
    model = build_model()

    controller = Controller(
        id="controller-1",
        name="Test Controller",
        controller_type="test",
    )

    with pytest.raises(ValueError):
        model.add_controller(
            "unknown-machine",
            controller,
        )


def test_removing_controller_removes_machine_association() -> None:
    model = build_model()

    controller = Controller(
        id="controller-1",
        name="Test Controller",
        controller_type="test",
    )

    model.add_controller(
        "machine-1",
        controller,
    )

    model.remove_controller("controller-1")

    machine = model.machines["machine-1"]

    assert "controller-1" not in machine.controller_ids


def test_controller_can_be_retrieved_after_machine_association() -> None:
    model = build_model()

    controller = Controller(
        id="controller-1",
        name="Test Controller",
        controller_type="test",
    )

    model.add_controller(
        "machine-1",
        controller,
    )

    retrieved = model.get_controller("controller-1")

    assert retrieved is controller
    assert retrieved.controller_type == "test"