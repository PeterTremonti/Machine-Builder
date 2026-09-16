import pytest

from machine_builder.controller import Controller
from machine_builder.controller_resource import ControllerResource
from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)
from machine_builder.semantic_capability import Capability
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Function,
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

    model.add_function(
        "machine-1",
        Function(
            id="function-1",
            name="Control Temperature",
        ),
    )

    model.add_capability(
        "machine-1",
        Capability(
            id="capability-1",
            name="Temperature Control",
        ),
    )

    model.add_controller(
        "machine-1",
        Controller(
            id="controller-1",
            name="Test Controller",
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

    return model


def build_assignment(
    assignment_id: str = "assignment-1",
    source_id: str = "component-1",
    resource_id: str = "resource-1",
) -> ControllerResourceAssignment:
    return ControllerResourceAssignment(
        id=assignment_id,
        source_id=source_id,
        resource_id=resource_id,
        assignment_type="controls",
    )


def test_assignment_can_be_added_to_machine() -> None:
    model = build_model()
    assignment = build_assignment()

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


def test_machine_tracks_assignment() -> None:
    model = build_model()

    model.add_controller_resource_assignment(
        "machine-1",
        build_assignment(),
    )

    assert model.machines[
        "machine-1"
    ].controller_resource_assignment_ids == [
        "assignment-1",
    ]


def test_duplicate_assignment_is_rejected() -> None:
    model = build_model()
    assignment = build_assignment()

    model.add_controller_resource_assignment(
        "machine-1",
        assignment,
    )

    with pytest.raises(ValueError):
        model.add_controller_resource_assignment(
            "machine-1",
            assignment,
        )


def test_unknown_machine_is_rejected() -> None:
    model = build_model()

    with pytest.raises(ValueError):
        model.add_controller_resource_assignment(
            "unknown-machine",
            build_assignment(),
        )


def test_unknown_resource_is_rejected() -> None:
    model = build_model()

    with pytest.raises(ValueError):
        model.add_controller_resource_assignment(
            "machine-1",
            build_assignment(
                resource_id="unknown-resource",
            ),
        )


def test_unknown_source_is_rejected() -> None:
    model = build_model()

    with pytest.raises(ValueError):
        model.add_controller_resource_assignment(
            "machine-1",
            build_assignment(
                source_id="unknown-source",
            ),
        )


def test_function_can_be_assignment_source() -> None:
    model = build_model()
    assignment = build_assignment(
        source_id="function-1",
    )

    model.add_controller_resource_assignment(
        "machine-1",
        assignment,
    )

    assert (
        model.get_controller_resource_assignment(
            assignment.id
        )
        is assignment
    )


def test_capability_can_be_assignment_source() -> None:
    model = build_model()
    assignment = build_assignment(
        source_id="capability-1",
    )

    model.add_controller_resource_assignment(
        "machine-1",
        assignment,
    )

    assert (
        model.get_controller_resource_assignment(
            assignment.id
        )
        is assignment
    )


def test_controller_can_be_assignment_source() -> None:
    model = build_model()
    assignment = build_assignment(
        source_id="controller-1",
    )

    model.add_controller_resource_assignment(
        "machine-1",
        assignment,
    )

    assert (
        model.get_controller_resource_assignment(
            assignment.id
        )
        is assignment
    )


def test_machine_can_be_assignment_source() -> None:
    model = build_model()
    assignment = build_assignment(
        source_id="machine-1",
    )

    model.add_controller_resource_assignment(
        "machine-1",
        assignment,
    )

    assert (
        model.get_controller_resource_assignment(
            assignment.id
        )
        is assignment
    )


def test_assignment_can_be_removed() -> None:
    model = build_model()
    assignment = build_assignment()

    model.add_controller_resource_assignment(
        "machine-1",
        assignment,
    )

    removed = model.remove_controller_resource_assignment(
        "assignment-1",
    )

    assert removed is assignment
    assert (
        model.machines[
            "machine-1"
        ].controller_resource_assignment_ids
        == []
    )

    with pytest.raises(KeyError):
        model.get_controller_resource_assignment(
            "assignment-1"
        )


def test_removing_resource_removes_assignments_to_resource() -> None:
    model = build_model()

    model.add_controller_resource_assignment(
        "machine-1",
        build_assignment(),
    )

    model.remove_controller_resource(
        "resource-1",
    )

    with pytest.raises(KeyError):
        model.get_controller_resource_assignment(
            "assignment-1"
        )


def test_removing_component_removes_component_assignments() -> None:
    model = build_model()

    model.add_controller_resource_assignment(
        "machine-1",
        build_assignment(),
    )

    model.remove_component(
        "component-1",
    )

    with pytest.raises(KeyError):
        model.get_controller_resource_assignment(
            "assignment-1"
        )


def test_removing_function_removes_function_assignments() -> None:
    model = build_model()

    model.add_controller_resource_assignment(
        "machine-1",
        build_assignment(
            source_id="function-1",
        ),
    )

    model.remove_function(
        "function-1",
    )

    with pytest.raises(KeyError):
        model.get_controller_resource_assignment(
            "assignment-1"
        )


def test_removing_capability_removes_capability_assignments() -> None:
    model = build_model()

    model.add_controller_resource_assignment(
        "machine-1",
        build_assignment(
            source_id="capability-1",
        ),
    )

    model.remove_capability(
        "capability-1",
    )

    with pytest.raises(KeyError):
        model.get_controller_resource_assignment(
            "assignment-1"
        )


def test_removing_controller_removes_controller_assignments() -> None:
    model = build_model()

    model.add_controller_resource_assignment(
        "machine-1",
        build_assignment(
            source_id="controller-1",
        ),
    )

    model.remove_controller(
        "controller-1",
    )

    with pytest.raises(KeyError):
        model.get_controller_resource_assignment(
            "assignment-1"
        )


def test_assignment_is_part_of_canonical_object_graph() -> None:
    model = build_model()
    assignment = build_assignment()

    model.add_controller_resource_assignment(
        "machine-1",
        assignment,
    )

    assert (
        assignment.id
        in model.controller_resource_assignments
    )