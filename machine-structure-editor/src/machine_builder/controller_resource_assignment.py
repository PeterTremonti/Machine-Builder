from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .semantic_model import Provenance


@dataclass
class ControllerResourceAssignment:
    """
    Semantic mapping between a machine object and a controller resource.

    The assignment records that a particular controller resource is used
    for a particular machine-semantic purpose. The target machine object
    may be a component, function, capability, or other canonical object.
    """

    id: str
    source_id: str
    resource_id: str
    assignment_type: str
    properties: dict[str, Any] = field(default_factory=dict)
    provenance: list["Provenance"] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Assignment id must not be empty.")

        if not self.source_id.strip():
            raise ValueError(
                "Assignment source_id must not be empty."
            )

        if not self.resource_id.strip():
            raise ValueError(
                "Assignment resource_id must not be empty."
            )

        if not self.assignment_type.strip():
            raise ValueError(
                "Assignment type must not be empty."
            )