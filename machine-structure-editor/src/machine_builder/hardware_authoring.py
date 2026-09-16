"""Helpers for authoring hardware-backed machine components."""

from __future__ import annotations

from dataclasses import replace

from .semantic_model import (
    CanonicalMachineModel,
    HardwareDefinition,
    MachineComponent,
    SemanticPort,
)


def add_hardware_component(
    model: CanonicalMachineModel,
    machine_id: str,
    component_id: str,
    role: str,
    label: str,
    hardware: HardwareDefinition,
    ports: tuple[SemanticPort, ...],
) -> MachineComponent:
    """Add a hardware-backed component and its instance ports."""
    if hardware.id not in model.hardware_definitions:
        model.add_hardware_definition(
            hardware
        )

    component = MachineComponent(
        id=component_id,
        role=role,
        label=label,
        hardware_definition_id=hardware.id,
    )

    model.add_component(
        machine_id,
        component,
    )

    for port in ports:
        component_port_id = _instance_port_id(
            port,
            component_id,
            hardware.id,
        )

        component_port = replace(
            port,
            id=component_port_id,
            component_id=component.id,
            properties=port.properties.copy(),
            provenance=port.provenance.copy(),
        )

        model.add_port(
            component_port
        )

    return component


def _instance_port_id(
    port: SemanticPort,
    component_id: str,
    hardware_id: str,
) -> str:
    """Create a unique canonical port ID for this component instance."""
    if port.id.startswith(
        f"{hardware_id}-"
    ):
        suffix = port.id[
            len(hardware_id) + 1:
        ]
        return (
            f"{component_id}-{suffix}"
        )

    return (
        f"{component_id}-{port.purpose.lower()}"
    )