from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)
from machine_builder.controller_resource_assignment_validation import (
    validate_controller_resource_assignment,
)
from machine_builder.semantic_model import CanonicalMachineModel


def create_controller_resource_assignment(
    model: CanonicalMachineModel,
    assignment_id: str,
    source_id: str,
    resource_id: str,
    assignment_type: str,
    properties: dict | None = None,
) -> ControllerResourceAssignment:
    """Create and validate a controller-resource assignment."""
    assignment = ControllerResourceAssignment(
        id=assignment_id,
        source_id=source_id,
        resource_id=resource_id,
        assignment_type=assignment_type,
        properties=properties or {},
    )

    validate_controller_resource_assignment(
        model,
        assignment,
    )

    return assignment