from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)
from machine_builder.semantic_model import CanonicalMachineModel


def validate_controller_resource_assignment(
    model: CanonicalMachineModel,
    assignment: ControllerResourceAssignment,
) -> None:
    """Validate that an assignment references existing canonical objects."""
    if assignment.resource_id not in model.controller_resources:
        raise ValueError(
            "Unknown controller resource: "
            f"{assignment.resource_id}"
        )

    if not _has_canonical_source(
        model,
        assignment.source_id,
    ):
        raise ValueError(
            "Unknown canonical assignment source: "
            f"{assignment.source_id}"
        )


def _has_canonical_source(
    model: CanonicalMachineModel,
    source_id: str,
) -> bool:
    return (
        source_id in model.components
        or source_id in model.functions
        or source_id in model.capabilities
        or source_id in model.controllers
        or source_id in model.controller_resources
        or source_id in model.machines
    )