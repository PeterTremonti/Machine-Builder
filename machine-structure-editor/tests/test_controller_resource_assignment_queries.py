from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)
from machine_builder.controller_resource_assignment_queries import (
    assignments_between,
    assignments_from_source,
    assignments_of_type,
    assignments_to_resource,
)


def build_assignments() -> list[ControllerResourceAssignment]:
    return [
        ControllerResourceAssignment(
            id="assignment-1",
            source_id="component-1",
            resource_id="resource-1",
            assignment_type="controls",
        ),
        ControllerResourceAssignment(
            id="assignment-2",
            source_id="component-1",
            resource_id="resource-2",
            assignment_type="controls",
        ),
        ControllerResourceAssignment(
            id="assignment-3",
            source_id="function-1",
            resource_id="resource-1",
            assignment_type="implemented_by",
        ),
        ControllerResourceAssignment(
            id="assignment-4",
            source_id="component-2",
            resource_id="resource-3",
            assignment_type="controls",
        ),
    ]


def test_assignments_from_source() -> None:
    assignments = assignments_from_source(
        build_assignments(),
        "component-1",
    )

    assert [assignment.id for assignment in assignments] == [
        "assignment-1",
        "assignment-2",
    ]


def test_assignments_from_unknown_source_are_empty() -> None:
    assignments = assignments_from_source(
        build_assignments(),
        "unknown-component",
    )

    assert assignments == []


def test_assignments_to_resource() -> None:
    assignments = assignments_to_resource(
        build_assignments(),
        "resource-1",
    )

    assert [assignment.id for assignment in assignments] == [
        "assignment-1",
        "assignment-3",
    ]


def test_assignments_to_unknown_resource_are_empty() -> None:
    assignments = assignments_to_resource(
        build_assignments(),
        "unknown-resource",
    )

    assert assignments == []


def test_assignments_of_type() -> None:
    assignments = assignments_of_type(
        build_assignments(),
        "controls",
    )

    assert [assignment.id for assignment in assignments] == [
        "assignment-1",
        "assignment-2",
        "assignment-4",
    ]


def test_assignments_of_unknown_type_are_empty() -> None:
    assignments = assignments_of_type(
        build_assignments(),
        "requires",
    )

    assert assignments == []


def test_assignments_between_source_and_resource() -> None:
    assignments = assignments_between(
        build_assignments(),
        "component-1",
        "resource-2",
    )

    assert [assignment.id for assignment in assignments] == [
        "assignment-2",
    ]


def test_assignments_between_unrelated_objects_are_empty() -> None:
    assignments = assignments_between(
        build_assignments(),
        "component-1",
        "resource-3",
    )

    assert assignments == []