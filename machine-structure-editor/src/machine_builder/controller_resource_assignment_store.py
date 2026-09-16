from __future__ import annotations

from dataclasses import dataclass, field

from machine_builder.controller_resource_assignment import (
    ControllerResourceAssignment,
)


@dataclass
class ControllerResourceAssignmentStore:
    assignments: dict[
        str,
        ControllerResourceAssignment,
    ] = field(default_factory=dict)

    def add(
        self,
        assignment: ControllerResourceAssignment,
    ) -> None:
        if assignment.id in self.assignments:
            raise ValueError(
                "Controller resource assignment already exists: "
                f"{assignment.id}"
            )

        self.assignments[assignment.id] = assignment

    def get(
        self,
        assignment_id: str,
    ) -> ControllerResourceAssignment:
        assignment = self.assignments.get(
            assignment_id
        )

        if assignment is None:
            raise KeyError(
                "Unknown controller resource assignment: "
                f"{assignment_id}"
            )

        return assignment

    def remove(
        self,
        assignment_id: str,
    ) -> ControllerResourceAssignment:
        assignment = self.get(
            assignment_id
        )

        del self.assignments[assignment_id]

        return assignment

    def all(
        self,
    ) -> list[ControllerResourceAssignment]:
        return list(
            self.assignments.values()
        )

    def __len__(self) -> int:
        return len(self.assignments)