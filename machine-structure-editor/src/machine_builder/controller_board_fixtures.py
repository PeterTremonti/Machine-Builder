"""Concrete controller-board fixtures for Machine Builder."""

from __future__ import annotations

from .controller_resource import ControllerResource
from .hardware_catalog import build_duet_2_maestro
from .semantic_model import (
    CanonicalMachineModel,
    Controller,
    SemanticPort,
)
from .semantic_relationship import SemanticRelationship


DUET_2_MAESTRO_CONNECTOR_LAYOUT = (
    ("x-motor", "X motor", 4),
    ("z-a-motor", "Z A motor", 4),
    ("z-b-motor", "Z B motor", 4),
    ("heater", "Heater", 2),
    ("thermistor", "Thermistor", 2),
    ("endstop", "Endstop", 3),
    ("z-probe", "Z probe", 5),
    ("fan", "Fan", 2),
)


def add_duet_2_maestro_physical_interfaces(
    model: CanonicalMachineModel,
    machine_id: str,
    controller_id: str = "duet-2-maestro-v1-0-controller",
    label: str = "Duet 2 Maestro",
) -> tuple[Controller, tuple[SemanticPort, ...]]:
    """Add a representative installed Duet 2 Maestro and its physical interfaces."""
    hardware_definition = build_duet_2_maestro()

    if hardware_definition.id not in model.hardware_definitions:
        model.add_hardware_definition(
            hardware_definition
        )

    controller = Controller(
        id=controller_id,
        name=label,
        controller_type="motion_controller",
        version="v1.0",
        hardware_definition_id=hardware_definition.id,
    )

    model.add_controller(
        machine_id,
        controller,
    )

    ports: list[SemanticPort] = []

    for (
        connector_id,
        connector_name,
        position_count,
    ) in DUET_2_MAESTRO_CONNECTOR_LAYOUT:
        for position in range(1, position_count + 1):
            port = SemanticPort(
                id=(
                    f"{controller_id}"
                    f"-{connector_id}"
                    f"-pin-{position}"
                ),
                component_id=None,
                purpose=(
                    f"{connector_name}"
                    " connector contact"
                ),
                direction="unknown",
                connector_id=connector_id,
                pin_id=str(position),
                properties={
                    "connector_position_count": (
                        position_count
                    )
                },
                provenance=[],
                controller_id=controller_id,
            )

            model.add_port(
                port
            )

            ports.append(port)

    z_stepper_resource = ControllerResource(
        id=f"{controller_id}-z-stepper",
        name="Z stepper driver",
        resource_type="stepper",
        controller_id=controller_id,
    )

    model.add_controller_resource(
        machine_id,
        z_stepper_resource,
    )

    for port in ports:
        if port.connector_id not in {
            "z-a-motor",
            "z-b-motor",
        }:
            continue

        relationship = SemanticRelationship(
            id=(
                f"{z_stepper_resource.id}"
                f"-exposed-through-{port.id}"
            ),
            source_id=z_stepper_resource.id,
            target_id=port.id,
            relationship_type="exposed_through",
        )

        model.add_relationship(
            relationship
        )

    return controller, tuple(ports)