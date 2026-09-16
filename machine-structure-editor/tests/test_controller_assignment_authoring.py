from machine_builder.controller import Controller
from machine_builder.controller_resource import ControllerResource
from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)
from machine_builder.controller_assignment_authoring import (
    create_controller_resource_assignment,
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
            name="Heater Output",
            resource_type="heater_output",
            controller_id="controller-1",
        ),
    )

    return model


def test_assignment_authoring_returns_assignment() -> None:
    model = build_model()

    assignment = create_controller_resource_assignment(
        model=model,
        assignment_id="assignment-1",
        source_id="component-1",
        resource_id="resource-1",
        assignment_type="controls",
    )

    assert isinstance(
        assignment,
        ControllerResourceAssignment,
    )


def test_assignment_authoring_preserves_values() -> None:
    model = build_model()

    assignment = create_controller_resource_assignment(
        model=model,
        assignment_id="assignment-1",
        source_id="component-1",
        resource_id="resource-1",
        assignment_type="controls",
        properties={
            "semantic_role": "heater",
        },
    )

    assert assignment.id == "assignment-1"
    assert assignment.source_id == "component-1"
    assert assignment.resource_id == "resource-1"
    assert assignment.assignment_type == "controls"
    assert assignment.properties == {
        "semantic_role": "heater",
    }


def test_assignment_authoring_validates_source() -> None:
    model = build_model()

    try:
        create_controller_resource_assignment(
            model=model,
            assignment_id="assignment-1",
            source_id="unknown-source",
            resource_id="resource-1",
            assignment_type="controls",
        )
    except ValueError as exc:
        assert "Unknown canonical assignment source" in str(exc)
    else:
        raise AssertionError(
            "Expected unknown assignment source to be rejected."
        )


def test_assignment_authoring_validates_resource() -> None:
    model = build_model()

    try:
        create_controller_resource_assignment(
            model=model,
            assignment_id="assignment-1",
            source_id="component-1",
            resource_id="unknown-resource",
            assignment_type="controls",
        )
    except ValueError as exc:
        assert "Unknown controller resource" in str(exc)
    else:
        raise AssertionError(
            "Expected unknown controller resource to be rejected."
        )


def test_assignment_authoring_does_not_add_assignment_to_model() -> None:
    model = build_model()

    assignment = create_controller_resource_assignment(
        model=model,
        assignment_id="assignment-1",
        source_id="component-1",
        resource_id="resource-1",
        assignment_type="controls",
    )

    assert model.controller_resource_assignments == {}
    assert assignment.id not in (
        model.controller_resource_assignments
    )


def test_assignment_authoring_does_not_modify_other_model_data() -> None:
    model = build_model()

    before_components = dict(
        model.components
    )
    before_controllers = dict(
        model.controllers
    )
    before_resources = dict(
        model.controller_resources
    )

    create_controller_resource_assignment(
        model=model,
        assignment_id="assignment-1",
        source_id="component-1",
        resource_id="resource-1",
        assignment_type="controls",
    )

    assert model.components == before_components
    assert model.controllers == before_controllers
    assert (
        model.controller_resources
        == before_resources
    )


def test_assignment_authoring_returns_distinct_objects() -> None:
    model = build_model()

    first = create_controller_resource_assignment(
        model=model,
        assignment_id="assignment-1",
        source_id="component-1",
        resource_id="resource-1",
        assignment_type="controls",
    )

    second = create_controller_resource_assignment(
        model=model,
        assignment_id="assignment-2",
        source_id="component-1",
        resource_id="resource-1",
        assignment_type="controls",
    )

    assert first is not second
    assert first.id != second.id


def test_assignment_authoring_supports_custom_properties() -> None:
    model = build_model()

    assignment = create_controller_resource_assignment(
        model=model,
        assignment_id="assignment-1",
        source_id="component-1",
        resource_id="resource-1",
        assignment_type="controls",
        properties={
            "semantic_role": "heater",
            "priority": 1,
        },
    )

    assert assignment.properties[
        "semantic_role"
    ] == "heater"
    assert assignment.properties[
        "priority"
    ] == 1