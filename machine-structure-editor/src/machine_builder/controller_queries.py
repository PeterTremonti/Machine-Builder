from __future__ import annotations

from machine_builder.controller_resource import ControllerResource
from machine_builder.semantic_model import CanonicalMachineModel


def controllers_for_machine(
    model: CanonicalMachineModel,
    machine_id: str,
):
    """Return the controllers associated with a machine."""
    machine = model.machines.get(machine_id)

    if machine is None:
        raise KeyError(
            f"Unknown machine: {machine_id}"
        )

    return [
        model.controllers[controller_id]
        for controller_id in machine.controller_ids
        if controller_id in model.controllers
    ]


def controller_resources_for_controller(
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


def controller_resources_for_machine(
    model: CanonicalMachineModel,
    machine_id: str,
) -> list[ControllerResource]:
    """Return all controller resources used by controllers on a machine."""
    controllers = controllers_for_machine(
        model,
        machine_id,
    )

    controller_ids = {
        controller.id
        for controller in controllers
    }

    return [
        resource
        for resource in model.controller_resources.values()
        if resource.controller_id in controller_ids
    ]


def controller_resources_of_type(
    model: CanonicalMachineModel,
    resource_type: str,
) -> list[ControllerResource]:
    """Return controller resources of a given resource type."""
    return [
        resource
        for resource in model.controller_resources.values()
        if resource.resource_type == resource_type
    ]