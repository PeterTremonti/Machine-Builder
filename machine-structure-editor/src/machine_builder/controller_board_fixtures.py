"""Fixtures for documented controller-board physical interfaces."""

from __future__ import annotations

from .controller import Controller
from .hardware_catalog import build_duet_2_maestro
from .semantic_model import (
    CanonicalMachineModel,
    SemanticPort,
)


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
    """Add an installed Maestro controller and representative physical interfaces.

    This fixture intentionally models only externally accessible physical
    connector positions. It does not introduce a Connector entity or map
    Controller Resources to physical interfaces yet.
    """
    hardware = build_duet_2_maestro()

    if hardware.id not in model.hardware_definitions:
        model.add_hardware_definition(hardware)

    controller = Controller(
        id=controller_id,
        name=label,
        controller_type="motion_controller",
        version="v1.0",
        hardware_definition_id=hardware.id,
    )

    model.add_controller(
        machine_id,
        controller,
    )

    ports: list[SemanticPort] = []

    for connector_id, connector_name, position_count in (
        DUET_2_MAESTRO_CONNECTOR_LAYOUT
    ):
        for position in range(1, position_count + 1):
            port = SemanticPort(
                id=(
                    f"{controller_id}-"
                    f"{connector_id}-pin-{position}"
                ),
                component_id=None,
                purpose=f"{connector_name} connector contact",
                direction="unknown",
                connector_id=connector_id,
                pin_id=str(position),
                properties={
                    "connector_position_count": position_count,
                },
                provenance=[],
                controller_id=controller_id,
            )
            model.add_port(port)
            ports.append(port)

    return controller, tuple(ports)