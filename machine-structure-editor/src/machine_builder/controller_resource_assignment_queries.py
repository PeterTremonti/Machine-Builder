"""Queries for controller-resource assignments."""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from .controller_resource_assignment import (
    ControllerResourceAssignment,
)

if TYPE_CHECKING:
    from .semantic_model import CanonicalMachineModel


def assignments_from_source(
    assignments: Iterable[ControllerResourceAssignment],
    source_id: str,
) -> list[ControllerResourceAssignment]:
    """Return assignments originating from a canonical source."""
    return [
        assignment
        for assignment in assignments
        if assignment.source_id == source_id
    ]


def assignments_to_resource(
    assignments: Iterable[ControllerResourceAssignment],
    resource_id: str,
) -> list[ControllerResourceAssignment]:
    """Return assignments targeting a controller resource."""
    return [
        assignment
        for assignment in assignments
        if assignment.resource_id == resource_id
    ]


def assignments_of_type(
    assignments: Iterable[ControllerResourceAssignment],
    assignment_type: str,
) -> list[ControllerResourceAssignment]:
    """Return assignments of a particular semantic type."""
    return [
        assignment
        for assignment in assignments
        if assignment.assignment_type == assignment_type
    ]


def assignments_between(
    assignments: Iterable[ControllerResourceAssignment],
    source_id: str,
    resource_id: str,
) -> list[ControllerResourceAssignment]:
    """Return assignments connecting one source to one resource."""
    return [
        assignment
        for assignment in assignments
        if (
            assignment.source_id == source_id
            and assignment.resource_id == resource_id
        )
    ]


def assignments_for_machine(
    model: CanonicalMachineModel,
    machine_id: str,
) -> list[ControllerResourceAssignment]:
    """Return assignments explicitly attached to a machine."""
    machine = model.machines.get(
        machine_id
    )

    if machine is None:
        raise KeyError(
            f"Unknown machine: {machine_id}"
        )

    return [
        model.controller_resource_assignments[
            assignment_id
        ]
        for assignment_id
        in machine.controller_resource_assignment_ids
        if assignment_id
        in model.controller_resource_assignments
    ]


def assignments_for_controller(
    model: CanonicalMachineModel,
    controller_id: str,
) -> list[ControllerResourceAssignment]:
    """Return assignments targeting resources owned by a controller."""
    if controller_id not in model.controllers:
        raise KeyError(
            f"Unknown controller: {controller_id}"
        )

    controller_resource_ids = {
        resource.id
        for resource
        in model.controller_resources.values()
        if resource.controller_id == controller_id
    }

    return [
        assignment
        for assignment
        in model.controller_resource_assignments.values()
        if assignment.resource_id
        in controller_resource_ids
    ]


def assignments_for_source(
    model: CanonicalMachineModel,
    source_id: str,
) -> list[ControllerResourceAssignment]:
    """Return assignments originating from a canonical object in the model."""
    if not model._has_canonical_object(
        source_id
    ):
        raise KeyError(
            f"Unknown canonical assignment source: {source_id}"
        )

    return assignments_from_source(
        model.controller_resource_assignments.values(),
        source_id,
    )


def assignments_for_resource(
    model: CanonicalMachineModel,
    resource_id: str,
) -> list[ControllerResourceAssignment]:
    """Return assignments targeting a canonical controller resource."""
    if resource_id not in model.controller_resources:
        raise KeyError(
            f"Unknown controller resource: {resource_id}"
        )

    return assignments_to_resource(
        model.controller_resource_assignments.values(),
        resource_id,
    )


def assignments_for_resource_type(
    model: CanonicalMachineModel,
    resource_type: str,
) -> list[ControllerResourceAssignment]:
    """Return assignments targeting resources of a given type."""
    resource_ids = {
        resource.id
        for resource
        in model.controller_resources.values()
        if resource.resource_type == resource_type
    }

    return [
        assignment
        for assignment
        in model.controller_resource_assignments.values()
        if assignment.resource_id
        in resource_ids
    ]