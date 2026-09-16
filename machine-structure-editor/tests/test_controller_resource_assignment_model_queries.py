import pytest

from machine_builder.controller import Controller
from machine_builder.controller_resource import ControllerResource
from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)
from machine_builder.controller_resource_assignment_queries import (
    assignments_for_controller,
    assignments_for_machine,
    assignments_for_resource,
    assignments_for_resource_type,
    assignments_for_source,
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
            name="Test Machine",
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
        "machine-1",
        MachineComponent(
            id="component-2",
            role="Fan",
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
        "machine-1",
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
            name="Heater Output",
            resource_type="heater_output",
            controller_id="controller-1",
        ),
    )

    model.add_controller_resource(
        "machine-1",
        ControllerResource(
            id="resource-2",
            name="Fan Output",
            resource_type="fan_output",
            controller_id="controller-1",
        ),
    )

    model.add_controller_resource(
        "machine-1",
        ControllerResource(
            id="resource-3",
            name="Second Heater Output",
            resource_type="heater_output",
            controller_id="controller-2",
        ),
    )

    model.add_controller_resource_assignment(
        "machine-1",
        ControllerResourceAssignment(
            id="assignment-1",
            source_id="component-1",
            resource_id="resource-1",
            assignment_type="controls",
        ),
    )

    model.add_controller_resource_assignment(
        "machine-1",
        ControllerResourceAssignment(
            id="assignment-2",
            source_id="component-2",
            resource_id="resource-2",
            assignment_type="controls",
        ),
    )

    model.add_controller_resource_assignment(
        "machine-1",
        ControllerResourceAssignment(
            id="assignment-3",
            source_id="component-1",
            resource_id="resource-3",
            assignment_type="backup_controls",
        ),
    )

    return model


def test_assignments_for_machine_returns_machine_assignments() -> None:
    model = build_model()

    assignments = assignments_for_machine(
        model,
        "machine-1",
    )

    assert [
        assignment.id
        for assignment in assignments
    ] == [
        "assignment-1",
        "assignment-2",
        "assignment-3",
    ]


def test_assignments_for_machine_rejects_unknown_machine() -> None:
    model = build_model()

    with pytest.raises(KeyError):
        assignments_for_machine(
            model,
            "unknown-machine",
        )


def test_assignments_for_controller_returns_matching_assignments() -> None:
    model = build_model()

    assignments = assignments_for_controller(
        model,
        "controller-1",
    )

    assert {
        assignment.id
        for assignment in assignments
    } == {
        "assignment-1",
        "assignment-2",
    }


def test_assignments_for_controller_excludes_other_controller() -> None:
    model = build_model()

    assignments = assignments_for_controller(
        model,
        "controller-2",
    )

    assert [
        assignment.id
        for assignment in assignments
    ] == [
        "assignment-3",
    ]


def test_assignments_for_controller_rejects_unknown_controller() -> None:
    model = build_model()

    with pytest.raises(KeyError):
        assignments_for_controller(
            model,
            "unknown-controller",
        )


def test_assignments_for_source_returns_matching_assignments() -> None:
    model = build_model()

    assignments = assignments_for_source(
        model,
        "component-1",
    )

    assert {
        assignment.id
        for assignment in assignments
    } == {
        "assignment-1",
        "assignment-3",
    }


def test_assignments_for_source_rejects_unknown_source() -> None:
    model = build_model()

    with pytest.raises(KeyError):
        assignments_for_source(
            model,
            "unknown-source",
        )


def test_assignments_for_resource_returns_matching_assignment() -> None:
    model = build_model()

    assignments = assignments_for_resource(
        model,
        "resource-1",
    )

    assert [
        assignment.id
        for assignment in assignments
    ] == [
        "assignment-1",
    ]


def test_assignments_for_resource_rejects_unknown_resource() -> None:
    model = build_model()

    with pytest.raises(KeyError):
        assignments_for_resource(
            model,
            "unknown-resource",
        )


def test_assignments_for_resource_type_returns_matching_assignments() -> None:
    model = build_model()

    assignments = assignments_for_resource_type(
        model,
        "heater_output",
    )

    assert {
        assignment.id
        for assignment in assignments
    } == {
        "assignment-1",
        "assignment-3",
    }


def test_assignments_for_resource_type_excludes_other_types() -> None:
    model = build_model()

    assignments = assignments_for_resource_type(
        model,
        "fan_output",
    )

    assert [
        assignment.id
        for assignment in assignments
    ] == [
        "assignment-2",
    ]