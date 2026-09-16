import pytest

from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)
from machine_builder.controller_resource_assignment_mutations import (
    CreateControllerResourceAssignment,
    DeleteControllerResourceAssignment,
)


def build_assignment(
    assignment_id: str = "assignment-1",
) -> ControllerResourceAssignment:
    return ControllerResourceAssignment(
        id=assignment_id,
        source_id="component-1",
        resource_id="resource-1",
        assignment_type="controls",
    )


def build_assignments() -> dict[
    str,
    ControllerResourceAssignment,
]:
    return {}


def test_create_assignment_adds_assignment_to_collection() -> None:
    assignments = build_assignments()
    assignment = build_assignment()

    mutation = CreateControllerResourceAssignment(
        assignment=assignment,
    )

    mutation.apply(assignments)

    assert assignments["assignment-1"] is assignment


def test_create_assignment_rejects_duplicate() -> None:
    assignments = build_assignments()
    assignment = build_assignment()

    assignments[assignment.id] = assignment

    mutation = CreateControllerResourceAssignment(
        assignment=assignment,
    )

    with pytest.raises(ValueError):
        mutation.apply(assignments)


def test_create_assignment_preserves_object_identity() -> None:
    assignments = build_assignments()
    assignment = build_assignment()

    CreateControllerResourceAssignment(
        assignment=assignment,
    ).apply(assignments)

    assert assignments["assignment-1"] is assignment


def test_delete_assignment_removes_assignment() -> None:
    assignments = build_assignments()
    assignment = build_assignment()

    assignments[assignment.id] = assignment

    removed = DeleteControllerResourceAssignment(
        assignment_id="assignment-1",
    ).apply(assignments)

    assert removed is assignment
    assert "assignment-1" not in assignments


def test_delete_assignment_rejects_unknown_assignment() -> None:
    assignments = build_assignments()

    mutation = DeleteControllerResourceAssignment(
        assignment_id="unknown-assignment",
    )

    with pytest.raises(KeyError):
        mutation.apply(assignments)


def test_multiple_assignments_can_be_created() -> None:
    assignments = build_assignments()

    first = build_assignment("assignment-1")
    second = build_assignment("assignment-2")

    CreateControllerResourceAssignment(
        assignment=first,
    ).apply(assignments)

    CreateControllerResourceAssignment(
        assignment=second,
    ).apply(assignments)

    assert set(assignments) == {
        "assignment-1",
        "assignment-2",
    }


def test_deleting_one_assignment_does_not_delete_another() -> None:
    assignments = build_assignments()

    first = build_assignment("assignment-1")
    second = build_assignment("assignment-2")

    assignments[first.id] = first
    assignments[second.id] = second

    DeleteControllerResourceAssignment(
        assignment_id="assignment-1",
    ).apply(assignments)

    assert "assignment-1" not in assignments
    assert assignments["assignment-2"] is second


def test_assignment_mutations_are_independent_of_visual_state() -> None:
    assignments = build_assignments()
    assignment = build_assignment()

    CreateControllerResourceAssignment(
        assignment=assignment,
    ).apply(assignments)

    DeleteControllerResourceAssignment(
        assignment_id="assignment-1",
    ).apply(assignments)

    assert assignments == {}