import pytest

from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)
from machine_builder.controller_resource_assignment_store import (
    ControllerResourceAssignmentStore,
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


def test_store_starts_empty() -> None:
    store = ControllerResourceAssignmentStore()

    assert len(store) == 0
    assert store.all() == []


def test_store_adds_assignment() -> None:
    store = ControllerResourceAssignmentStore()
    assignment = build_assignment()

    store.add(assignment)

    assert len(store) == 1
    assert store.get("assignment-1") is assignment


def test_store_rejects_duplicate_assignment() -> None:
    store = ControllerResourceAssignmentStore()
    assignment = build_assignment()

    store.add(assignment)

    with pytest.raises(ValueError):
        store.add(assignment)


def test_store_get_rejects_unknown_assignment() -> None:
    store = ControllerResourceAssignmentStore()

    with pytest.raises(KeyError):
        store.get("unknown-assignment")


def test_store_removes_assignment() -> None:
    store = ControllerResourceAssignmentStore()
    assignment = build_assignment()

    store.add(assignment)

    removed = store.remove("assignment-1")

    assert removed is assignment
    assert len(store) == 0


def test_store_remove_rejects_unknown_assignment() -> None:
    store = ControllerResourceAssignmentStore()

    with pytest.raises(KeyError):
        store.remove("unknown-assignment")


def test_store_returns_all_assignments_in_insertion_order() -> None:
    store = ControllerResourceAssignmentStore()

    first = build_assignment("assignment-1")
    second = build_assignment("assignment-2")
    third = build_assignment("assignment-3")

    store.add(first)
    store.add(second)
    store.add(third)

    assert store.all() == [
        first,
        second,
        third,
    ]


def test_store_all_returns_independent_list() -> None:
    store = ControllerResourceAssignmentStore()

    assignment = build_assignment()

    store.add(assignment)

    assignments = store.all()
    assignments.clear()

    assert len(store) == 1
    assert store.get("assignment-1") is assignment