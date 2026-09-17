"""Queries for canonical controller authoring and inspection."""

from __future__ import annotations

from .editor_state import EditorState
from .controller import Controller


def get_controller(
    state: EditorState,
    controller_id: str,
) -> Controller:
    """Return a canonical controller."""
    controller = (
        state.semantic_model.controllers.get(
            controller_id
        )
    )

    if controller is None:
        raise KeyError(
            "Unknown controller: "
            f"{controller_id}"
        )

    return controller


def machine_id_for_controller(
    state: EditorState,
    controller_id: str,
) -> str:
    """Return the machine that owns a controller."""
    get_controller(
        state,
        controller_id,
    )

    for (
        machine_id,
        machine,
    ) in state.semantic_model.machines.items():
        if controller_id in machine.controller_ids:
            return machine_id

    raise ValueError(
        "Controller is not attached to a machine: "
        f"{controller_id}"
    )


def controllers_for_machine(
    state: EditorState,
    machine_id: str,
) -> tuple[Controller, ...]:
    """Return controllers attached to a machine."""
    machine = (
        state.semantic_model.machines.get(
            machine_id
        )
    )

    if machine is None:
        raise KeyError(
            "Unknown machine: "
            f"{machine_id}"
        )

    return tuple(
        state.semantic_model.controllers[
            controller_id
        ]
        for controller_id
        in machine.controller_ids
        if controller_id
        in state.semantic_model.controllers
    )


def controller_for_resource(
    state: EditorState,
    resource_id: str,
) -> Controller | None:
    """Return the controller owning a resource, if known."""
    resource = (
        state.semantic_model.controller_resources.get(
            resource_id
        )
    )

    if resource is None:
        raise KeyError(
            "Unknown controller resource: "
            f"{resource_id}"
        )

    if resource.controller_id is None:
        return None

    return get_controller(
        state,
        resource.controller_id,
    )