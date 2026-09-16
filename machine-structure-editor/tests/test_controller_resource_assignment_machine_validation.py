import pytest

from machine_builder.controller import Controller
from machine_builder.controller_resource import ControllerResource
from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
)


def build_model() -> CanonicalMachineModel:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Machine 1",
        )
    )

    model.add_machine(
        Machine(
            id="machine-2",
            name="Machine 2",
        )
    )

    model.add_component(
        "machine-1",
        MachineComponent(
            id="component-1",
            role="Heater",
        ),
    )

    model.add_component(
        "machine-2",
        MachineComponent(
            id="component-2",
            role="Heater",
        ),
    )

    model.add_controller(
        "machine-1",
        Controller(
            id="controller-1",
            name="Controller 1",
            controller_type="test",
        ),
    )

    model.add_controller(
        "machine-2",
        Controller(
            id="controller-2",
            name="Controller 2",
            controller_type="test",
        ),
    )

    model.add_controller_resource(
        "machine-1",
        ControllerResource(
            id="resource-1",
            name="Heater Output 1",
            resource_type="heater_output",
            controller_id="controller-1",
        ),
    )

    model.add_controller_resource(
        "machine-2",
        ControllerResource(
            id="resource-2",
            name="Heater Output 2",
            resource_type="heater_output",
            controller_id="controller-2",
        ),
    )

    return model


def test_assignment_accepts_source_and_resource_on_same_machine() -> None:
    model = build_model()

    assignment = ControllerResourceAssignment(
        id="assignment-1",
        source_id="component-1",
        resource_id="resource-1",
        assignment_type="controls",
    )

    model.add_controller_resource_assignment(
        "machine-1",
        assignment,
    )

    assert (
        model.get_controller_resource_assignment(
            "assignment-1"
        )
        is assignment
    )


def test_assignment_rejects_source_from_different_machine() -> None:
    model = build_model()

    assignment = ControllerResourceAssignment(
        id="assignment-1",
        source_id="component-2",
        resource_id="resource-1",
        assignment_type="controls",
    )

    with pytest.raises(
        ValueError,
        match="different machine",
    ):
        model.add_controller_resource_assignment(
            "machine-1",
            assignment,
        )


def test_assignment_rejects_resource_from_different_machine() -> None:
    model = build_model()

    assignment = ControllerResourceAssignment(
        id="assignment-1",
        source_id="component-1",
        resource_id="resource-2",
        assignment_type="controls",
    )

    with pytest.raises(
        ValueError,
        match="different machine",
    ):
        model.add_controller_resource_assignment(
            "machine-1",
            assignment,
        )


def test_assignment_can_be_added_to_second_machine() -> None:
    model = build_model()

    assignment = ControllerResourceAssignment(
        id="assignment-2",
        source_id="component-2",
        resource_id="resource-2",
        assignment_type="controls",
    )

    model.add_controller_resource_assignment(
        "machine-2",
        assignment,
    )

    assert (
        model.machines[
            "machine-2"
        ].controller_resource_assignment_ids
        == ["assignment-2"]
    )


def test_machine_lookup_resolves_component_owner() -> None:
    model = build_model()

    assert (
        model._machine_for_canonical_object(
            "component-1"
        )
        == "machine-1"
    )

    assert (
        model._machine_for_canonical_object(
            "component-2"
        )
        == "machine-2"
    )


def test_machine_lookup_resolves_controller_resource_owner() -> None:
    model = build_model()

    assert (
        model._machine_for_canonical_object(
            "resource-1"
        )
        == "machine-1"
    )

    assert (
        model._machine_for_canonical_object(
            "resource-2"
        )
        == "machine-2"
    )


def test_assignment_machine_mismatch_does_not_store_assignment() -> None:
    model = build_model()

    assignment = ControllerResourceAssignment(
        id="assignment-1",
        source_id="component-2",
        resource_id="resource-1",
        assignment_type="controls",
    )

    with pytest.raises(ValueError):
        model.add_controller_resource_assignment(
            "machine-1",
            assignment,
        )

    assert model.controller_resource_assignments == {}
    assert (
        model.machines[
            "machine-1"
        ].controller_resource_assignment_ids
        == []
    )


def test_unknown_canonical_object_has_no_machine_owner() -> None:
    model = build_model()

    assert (
        model._machine_for_canonical_object(
            "unknown-object"
        )
        is None
    )