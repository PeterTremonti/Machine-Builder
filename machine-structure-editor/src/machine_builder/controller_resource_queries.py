"""Queries for canonical controller-resource information."""

from __future__ import annotations

from .controller_resource import ControllerResource
from .semantic_model import CanonicalMachineModel


def get_controller_resource(
    model: CanonicalMachineModel,
    resource_id: str,
) -> ControllerResource:
    """Return one controller resource."""
    return model.get_controller_resource(resource_id)


def machine_id_for_controller_resource(
    model: CanonicalMachineModel,
    resource_id: str,
) -> str | None:
    """Return the machine that owns a controller resource."""
    if resource_id not in model.controller_resources:
        raise KeyError(
            "Unknown controller resource: "
            f"{resource_id}"
        )

    return model._machine_for_canonical_object(
        resource_id
    )


def controller_for_resource(
    model: CanonicalMachineModel,
    resource_id: str,
):
    """Return the controller associated with a resource, if any."""
    resource = model.get_controller_resource(
        resource_id
    )

    if resource.controller_id is None:
        return None

    return model.get_controller(
        resource.controller_id
    )


def resources_for_controller(
    model: CanonicalMachineModel,
    controller_id: str,
) -> list[ControllerResource]:
    """Return all resources belonging to a controller."""
    if controller_id not in model.controllers:
        raise KeyError(
            f"Unknown controller: {controller_id}"
        )

    return [
        resource
        for resource in model.controller_resources.values()
        if resource.controller_id == controller_id
    ]


def resources_for_machine(
    model: CanonicalMachineModel,
    machine_id: str,
) -> list[ControllerResource]:
    """Return all controller resources owned by a machine."""
    machine = model.machines.get(machine_id)

    if machine is None:
        raise KeyError(
            f"Unknown machine: {machine_id}"
        )

    return [
        model.controller_resources[resource_id]
        for resource_id in machine.controller_resource_ids
        if resource_id in model.controller_resources
    ]