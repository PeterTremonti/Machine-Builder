"""Helpers for building canonical test components from hardware fixtures."""

from __future__ import annotations

from dataclasses import replace

from .hardware_catalog import (
    build_generic_120vac_400w_heater,
)
from .semantic_model import (
    CanonicalMachineModel,
    MachineComponent,
)


def add_generic_120vac_400w_heater(
    model: CanonicalMachineModel,
    machine_id: str,
    component_id: str = "chamber-heater-1",
    label: str = "Chamber Heater",
) -> MachineComponent:
    """Add one real generic 120 VAC 400 W heater to a machine."""
    hardware, ports = (
        build_generic_120vac_400w_heater()
    )

    if hardware.id not in model.hardware_definitions:
        model.add_hardware_definition(
            hardware
        )

    component = MachineComponent(
        id=component_id,
        role="Chamber Heater",
        label=label,
        hardware_definition_id=hardware.id,
    )

    model.add_component(
        machine_id,
        component,
    )

    for port in ports:
        component_port = replace(
            port,
            id=port.id.replace(
                "generic-120vac-400w-heater",
                component_id,
            ),
            component_id=component.id,
            properties=port.properties.copy(),
            provenance=port.provenance.copy(),
        )

        model.add_port(
            component_port
        )

    return component