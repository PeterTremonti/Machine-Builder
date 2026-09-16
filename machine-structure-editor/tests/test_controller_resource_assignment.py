import pytest

from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)


def test_assignment_can_be_created() -> None:
    assignment = ControllerResourceAssignment(
        id="assignment-1",
        source_id="component-1",
        resource_id="resource-1",
        assignment_type="controls",
    )

    assert assignment.id == "assignment-1"
    assert assignment.source_id == "component-1"
    assert assignment.resource_id == "resource-1"
    assert assignment.assignment_type == "controls"


def test_assignment_has_optional_properties() -> None:
    assignment = ControllerResourceAssignment(
        id="assignment-1",
        source_id="function-1",
        resource_id="resource-1",
        assignment_type="implemented_by",
        properties={
            "channel": 0,
        },
    )

    assert assignment.properties["channel"] == 0


def test_assignment_rejects_empty_id() -> None:
    with pytest.raises(ValueError):
        ControllerResourceAssignment(
            id="",
            source_id="component-1",
            resource_id="resource-1",
            assignment_type="controls",
        )


def test_assignment_rejects_empty_source_id() -> None:
    with pytest.raises(ValueError):
        ControllerResourceAssignment(
            id="assignment-1",
            source_id="",
            resource_id="resource-1",
            assignment_type="controls",
        )


def test_assignment_rejects_empty_resource_id() -> None:
    with pytest.raises(ValueError):
        ControllerResourceAssignment(
            id="assignment-1",
            source_id="component-1",
            resource_id="",
            assignment_type="controls",
        )


def test_assignment_rejects_empty_assignment_type() -> None:
    with pytest.raises(ValueError):
        ControllerResourceAssignment(
            id="assignment-1",
            source_id="component-1",
            resource_id="resource-1",
            assignment_type="",
        )


def test_assignment_rejects_whitespace_only_values() -> None:
    with pytest.raises(ValueError):
        ControllerResourceAssignment(
            id="   ",
            source_id="component-1",
            resource_id="resource-1",
            assignment_type="controls",
        )


def test_assignment_properties_are_independent_between_instances() -> None:
    first = ControllerResourceAssignment(
        id="assignment-1",
        source_id="component-1",
        resource_id="resource-1",
        assignment_type="controls",
    )

    second = ControllerResourceAssignment(
        id="assignment-2",
        source_id="component-2",
        resource_id="resource-2",
        assignment_type="controls",
    )

    first.properties["test"] = True

    assert "test" not in second.properties