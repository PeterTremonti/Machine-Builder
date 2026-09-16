import pytest

from machine_builder.controller import Controller
from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)
from machine_builder.controller_resource_assignment_validation import (
    validate_controller_resource_assignment,
)
from machine_builder.controller_resource import ControllerResource
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
    source_id: str = "component-1",
    resource_id: str = "resource-1",
) -> ControllerResourceAssignment:
    return ControllerResourceAssignment(
        id="assignment-1",
        source_id=source_id,
        resource_id=resource_id,
        assignment_type="controls",
    )


def test_valid_component_assignment_passes() -> None:
    model = build_model()

    validate_controller_resource_assignment(
        model,
        build_assignment(),
    )


def test_valid_function_assignment_passes() -> None:
    model = build_model()

    validate_controller_resource_assignment(
        model,
        build_assignment(
            source_id="function-1",
        ),
    )


def test_valid_capability_assignment_passes() -> None:
    model = build_model()

    validate_controller_resource_assignment(
        model,
        build_assignment(
            source_id="capability-1",
        ),
    )


def test_valid_controller_assignment_passes() -> None:
    model = build_model()

    validate_controller_resource_assignment(
        model,
        build_assignment(
            source_id="controller-1",
        ),
    )


def test_unknown_source_is_rejected() -> None:
    model = build_model()

    with pytest.raises(ValueError):
        validate_controller_resource_assignment(
            model,
            build_assignment(
                source_id="unknown-source",
            ),
        )


def test_unknown_resource_is_rejected() -> None:
    model = build_model()

    with pytest.raises(ValueError):
        validate_controller_resource_assignment(
            model,
            build_assignment(
                resource_id="unknown-resource",
            ),
        )


def test_machine_is_valid_assignment_source() -> None:
    model = build_model()

    validate_controller_resource_assignment(
        model,
        build_assignment(
            source_id="machine-1",
        ),
    )


def test_controller_resource_is_valid_assignment_source() -> None:
    model = build_model()

    validate_controller_resource_assignment(
        model,
        build_assignment(
            source_id="resource-1",
        ),
    )