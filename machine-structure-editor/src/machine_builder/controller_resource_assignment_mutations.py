from dataclasses import dataclass
from collections.abc import MutableMapping

from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)


@dataclass
class CreateControllerResourceAssignment:
    assignment: ControllerResourceAssignment

    def apply(
        self,
        assignments: MutableMapping[
            str,
            ControllerResourceAssignment,
        ],
    ) -> None:
        if self.assignment.id in assignments:
            raise ValueError(
                "Controller resource assignment already exists: "
                f"{self.assignment.id}"
            )

        assignments[self.assignment.id] = self.assignment


@dataclass
class DeleteControllerResourceAssignment:
    assignment_id: str

    def apply(
        self,
        assignments: MutableMapping[
            str,
            ControllerResourceAssignment,
        ],
    ) -> ControllerResourceAssignment:
        assignment = assignments.get(
            self.assignment_id
        )

        if assignment is None:
            raise KeyError(
                "Unknown controller resource assignment: "
                f"{self.assignment_id}"
            )

        del assignments[self.assignment_id]

        return assignment