"""Canonical semantic model foundation for the Machine Structure Editor.

This module contains the beginning of the canonical Machine Builder model.

The canonical model represents what the machine means. It is intentionally
independent of Qt and independent of the visual editor's geometry.

Visual objects such as VisualNode and VisualPort reference canonical objects
but do not replace them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Provenance:
    """Evidence describing where a canonical fact came from."""

    source: str
    evidence_type: str = "authored"
    method: str | None = None
    context: str | None = None
    date: str | None = None
    notes: str | None = None


@dataclass
class HardwareDefinition:
    """Description of a physical hardware definition.

    A hardware definition describes a kind of physical hardware separately
    from the machine-specific component that uses it.

    Manufacturer may be absent or generic. A missing hardware definition is
    represented by the component having no hardware_definition_id.
    """

    id: str
    family: str
    manufacturer: str | None = None
    variant: str | None = None

    properties: dict[str, Any] = field(
        default_factory=dict
    )

    provenance: list[Provenance] = field(
        default_factory=list
    )


@dataclass
class SemanticPort:
    """A canonical interface belonging to a machine component."""

    id: str
    component_id: str
    purpose: str

    direction: str = "unknown"

    connector_id: str | None = None
    pin_id: str | None = None

    properties: dict[str, Any] = field(
        default_factory=dict
    )

    provenance: list[Provenance] = field(
        default_factory=list
    )


@dataclass
class MachineComponent:
    """A machine-specific semantic component.

    The component has its own identity within a particular machine even when
    it uses a hardware definition shared with other machines.
    """

    id: str
    role: str
    label: str = ""

    hardware_definition_id: str | None = None

    port_ids: list[str] = field(
        default_factory=list
    )

    properties: dict[str, Any] = field(
        default_factory=dict
    )

    provenance: list[Provenance] = field(
        default_factory=list
    )


@dataclass
class Machine:
    """A canonical machine being described."""

    id: str
    name: str

    component_ids: list[str] = field(
        default_factory=list
    )

    properties: dict[str, Any] = field(
        default_factory=dict
    )

    provenance: list[Provenance] = field(
        default_factory=list
    )


@dataclass
class CanonicalMachineModel:
    """Container for canonical semantic machine information."""

    machines: dict[str, Machine] = field(
        default_factory=dict
    )

    components: dict[str, MachineComponent] = field(
        default_factory=dict
    )

    hardware_definitions: dict[str, HardwareDefinition] = field(
        default_factory=dict
    )

    ports: dict[str, SemanticPort] = field(
        default_factory=dict
    )

    def add_machine(
        self,
        machine: Machine,
    ) -> None:
        """Add a machine to the canonical model."""
        if machine.id in self.machines:
            raise ValueError(
                f"Machine already exists: {machine.id}"
            )

        self.machines[
            machine.id
        ] = machine

    def add_component(
        self,
        machine_id: str,
        component: MachineComponent,
    ) -> None:
        """Add a machine component and attach it to a machine."""
        if component.id in self.components:
            raise ValueError(
                f"Machine component already exists: {component.id}"
            )

        if machine_id not in self.machines:
            raise ValueError(
                f"Unknown machine: {machine_id}"
            )

        if component.hardware_definition_id is not None:
            if (
                component.hardware_definition_id
                not in self.hardware_definitions
            ):
                raise ValueError(
                    "Unknown hardware definition: "
                    f"{component.hardware_definition_id}"
                )

        self.components[
            component.id
        ] = component

        self.machines[
            machine_id
        ].component_ids.append(
            component.id
        )

    def remove_component(
        self,
        component_id: str,
    ) -> MachineComponent:
        """Remove a machine component and its canonical ports."""
        component = self.components.get(
            component_id
        )

        if component is None:
            raise KeyError(
                f"Unknown machine component: {component_id}"
            )

        for port_id in tuple(
            component.port_ids
        ):
            self.ports.pop(
                port_id,
                None,
            )

        for machine in self.machines.values():
            if component_id in machine.component_ids:
                machine.component_ids.remove(
                    component_id
                )
                break

        del self.components[
            component_id
        ]

        return component

    def add_hardware_definition(
        self,
        hardware_definition: HardwareDefinition,
    ) -> None:
        """Add a reusable physical hardware definition."""
        if hardware_definition.id in self.hardware_definitions:
            raise ValueError(
                "Hardware definition already exists: "
                f"{hardware_definition.id}"
            )

        self.hardware_definitions[
            hardware_definition.id
        ] = hardware_definition

    def add_port(
        self,
        port: SemanticPort,
    ) -> None:
        """Add a canonical port to its machine component."""
        if port.id in self.ports:
            raise ValueError(
                f"Port already exists: {port.id}"
            )

        component = self.components.get(
            port.component_id
        )

        if component is None:
            raise ValueError(
                "Unknown component: "
                f"{port.component_id}"
            )

        if port.id in component.port_ids:
            raise ValueError(
                f"Port is already attached to component: "
                f"{port.component_id}"
            )

        self.ports[
            port.id
        ] = port

        component.port_ids.append(
            port.id
        )

    def get_component(
        self,
        component_id: str,
    ) -> MachineComponent:
        """Return a canonical machine component."""
        component = self.components.get(
            component_id
        )

        if component is None:
            raise KeyError(
                f"Unknown machine component: {component_id}"
            )

        return component

    def get_port(
        self,
        port_id: str,
    ) -> SemanticPort:
        """Return a canonical port."""
        port = self.ports.get(
            port_id
        )

        if port is None:
            raise KeyError(
                f"Unknown port: {port_id}"
            )

        return port