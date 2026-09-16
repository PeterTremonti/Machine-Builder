from __future__ import annotations

from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)
from machine_builder.controller_fixtures import (
    add_generic_octopus_controller,
)
from machine_builder.hardware_component_fixtures import (
    add_generic_120vac_400w_heater,
)


def add_generic_heater_controller_assignment(
    model,
    machine_id: str,
    component_id: str = "chamber-heater-1",
    controller_id: str = "octopus-v1-1",
) -> ControllerResourceAssignment:
    """Create a representative heater/controller assignment.

    This fixture creates or reuses the controller and heater component,
    then returns a new assignment object without storing it in the model.
    """
    if controller_id not in model.controllers:
        add_generic_octopus_controller(
            model,
            machine_id,
            controller_id=controller_id,
        )

    if component_id not in model.components:
        add_generic_120vac_400w_heater(
            model,
            machine_id,
            component_id=component_id,
        )

    return ControllerResourceAssignment(
        id=f"{component_id}-controller-assignment",
        source_id=component_id,
        resource_id=f"{controller_id}-heater-0",
        assignment_type="controls",
        properties={
            "semantic_role": "heater",
        },
    )


def add_generic_heater_controller_assignment_to_model(
    model,
    machine_id: str,
    component_id: str = "chamber-heater-1",
    controller_id: str = "octopus-v1-1",
) -> ControllerResourceAssignment:
    """Create and store a representative heater/controller assignment."""
    assignment = add_generic_heater_controller_assignment(
        model=model,
        machine_id=machine_id,
        component_id=component_id,
        controller_id=controller_id,
    )

    existing = model.controller_resource_assignments.get(
        assignment.id
    )

    if existing is not None:
        return existing

    model.add_controller_resource_assignment(
        machine_id,
        assignment,
    )

    return assignment