"""Canonical semantic model foundation for the Machine Structure Editor.

This module contains the canonical Machine Builder model.
The canonical model represents what the machine means. It is independent
of Qt and independent of the visual editor's geometry.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .controller import Controller
from .controller_resource import ControllerResource
from .semantic_capability import Capability


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
    """Description of a physical hardware definition."""

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
class Function:
    """An identifiable machine behavior or service."""

    id: str
    name: str
    description: str = ""

    properties: dict[str, Any] = field(
        default_factory=dict
    )
    provenance: list[Provenance] = field(
        default_factory=list
    )


@dataclass
class MachineComponent:
    """A machine-specific semantic component."""

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

    function_ids: list[str] = field(
        default_factory=list
    )

    capability_ids: list[str] = field(
        default_factory=list
    )

    controller_ids: list[str] = field(
        default_factory=list
    )

    controller_resource_ids: list[str] = field(
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

    hardware_definitions: dict[
        str,
        HardwareDefinition,
    ] = field(
        default_factory=dict
    )

    ports: dict[str, SemanticPort] = field(
        default_factory=dict
    )

    functions: dict[str, Function] = field(
        default_factory=dict
    )

    capabilities: dict[str, Capability] = field(
        default_factory=dict
    )

    controllers: dict[str, Controller] = field(
        default_factory=dict
    )

    controller_resources: dict[
        str,
        ControllerResource,
    ] = field(
        default_factory=dict
    )

    connections: dict[str, Any] = field(
        default_factory=dict
    )

    relationships: dict[str, Any] = field(
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
        """Remove a machine component and its related semantic data."""
        component = self.components.get(
            component_id
        )

        if component is None:
            raise KeyError(
                f"Unknown machine component: {component_id}"
            )

        component_port_ids = set(
            component.port_ids
        )

        connection_ids = [
            connection_id
            for connection_id, connection
            in self.connections.items()
            if (
                connection.endpoint_a_id
                in component_port_ids
                or connection.endpoint_b_id
                in component_port_ids
            )
        ]

        for connection_id in connection_ids:
            del self.connections[
                connection_id
            ]

        relationship_ids = [
            relationship_id
            for relationship_id, relationship
            in self.relationships.items()
            if (
                relationship.source_id == component_id
                or relationship.target_id == component_id
                or relationship.source_id in component_port_ids
                or relationship.target_id in component_port_ids
            )
        ]

        for relationship_id in relationship_ids:
            del self.relationships[
                relationship_id
            ]

        for port_id in component.port_ids:
            self.ports.pop(
                port_id,
                None
            )

        for machine in self.machines.values():
            if component_id in machine.component_ids:
                machine.component_ids.remove(
                    component_id
                )

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
                "Port is already attached to component: "
                f"{port.component_id}"
            )

        self.ports[
            port.id
        ] = port

        component.port_ids.append(
            port.id
        )

    def add_function(
        self,
        machine_id: str,
        function: Function,
    ) -> None:
        """Add a Function and attach it to a machine."""
        if function.id in self.functions:
            raise ValueError(
                f"Function already exists: {function.id}"
            )

        machine = self.machines.get(
            machine_id
        )

        if machine is None:
            raise ValueError(
                f"Unknown machine: {machine_id}"
            )

        self.functions[
            function.id
        ] = function

        machine.function_ids.append(
            function.id
        )

    def remove_function(
        self,
        function_id: str,
    ) -> Function:
        """Remove a Function from the canonical model."""
        function = self.functions.get(
            function_id
        )

        if function is None:
            raise KeyError(
                f"Unknown function: {function_id}"
            )

        relationship_ids = [
            relationship_id
            for relationship_id, relationship
            in self.relationships.items()
            if (
                relationship.source_id == function_id
                or relationship.target_id == function_id
            )
        ]

        for relationship_id in relationship_ids:
            del self.relationships[
                relationship_id
            ]

        for machine in self.machines.values():
            if function_id in machine.function_ids:
                machine.function_ids.remove(
                    function_id
                )

        del self.functions[
            function_id
        ]

        return function

    def add_capability(
        self,
        machine_id: str,
        capability: Capability,
    ) -> None:
        """Add a Capability and attach it to a machine."""
        if capability.id in self.capabilities:
            raise ValueError(
                f"Capability already exists: {capability.id}"
            )

        machine = self.machines.get(
            machine_id
        )

        if machine is None:
            raise ValueError(
                f"Unknown machine: {machine_id}"
            )

        self.capabilities[
            capability.id
        ] = capability

        machine.capability_ids.append(
            capability.id
        )

    def remove_capability(
        self,
        capability_id: str,
    ) -> Capability:
        """Remove a Capability from the canonical model."""
        capability = self.capabilities.get(
            capability_id
        )

        if capability is None:
            raise KeyError(
                f"Unknown capability: {capability_id}"
            )

        relationship_ids = [
            relationship_id
            for relationship_id, relationship
            in self.relationships.items()
            if (
                relationship.source_id == capability_id
                or relationship.target_id == capability_id
            )
        ]

        for relationship_id in relationship_ids:
            del self.relationships[
                relationship_id
            ]

        for machine in self.machines.values():
            if capability_id in machine.capability_ids:
                machine.capability_ids.remove(
                    capability_id
                )

        del self.capabilities[
            capability_id
        ]

        return capability

    def add_controller(
        self,
        machine_id: str,
        controller: Controller,
    ) -> None:
        """Add a controller and attach it to a machine."""
        if controller.id in self.controllers:
            raise ValueError(
                f"Controller already exists: {controller.id}"
            )

        machine = self.machines.get(
            machine_id
        )

        if machine is None:
            raise ValueError(
                f"Unknown machine: {machine_id}"
            )

        self.controllers[
            controller.id
        ] = controller

        machine.controller_ids.append(
            controller.id
        )

    def get_controller(
        self,
        controller_id: str,
    ) -> Controller:
        """Return a canonical controller."""
        controller = self.controllers.get(
            controller_id
        )

        if controller is None:
            raise KeyError(
                f"Unknown controller: {controller_id}"
            )

        return controller

    def remove_controller(
        self,
        controller_id: str,
    ) -> Controller:
        """Remove a controller and its machine association."""
        controller = self.controllers.get(
            controller_id
        )

        if controller is None:
            raise KeyError(
                f"Unknown controller: {controller_id}"
            )

        resource_ids = [
            resource_id
            for resource_id, resource
            in self.controller_resources.items()
            if resource.controller_id == controller_id
        ]

        for resource_id in resource_ids:
            self.remove_controller_resource(
                resource_id
            )

        for machine in self.machines.values():
            if controller_id in machine.controller_ids:
                machine.controller_ids.remove(
                    controller_id
                )

        del self.controllers[
            controller_id
        ]

        return controller

    def add_controller_resource(
        self,
        machine_id: str,
        resource: ControllerResource,
    ) -> None:
        """Add a controller resource and attach it to a machine."""
        if resource.id in self.controller_resources:
            raise ValueError(
                "Controller resource already exists: "
                f"{resource.id}"
            )

        machine = self.machines.get(
            machine_id
        )

        if machine is None:
            raise ValueError(
                f"Unknown machine: {machine_id}"
            )

        if resource.controller_id is not None:
            if resource.controller_id not in self.controllers:
                raise ValueError(
                    "Unknown controller: "
                    f"{resource.controller_id}"
                )

        self.controller_resources[
            resource.id
        ] = resource

        machine.controller_resource_ids.append(
            resource.id
        )

    def get_controller_resource(
        self,
        resource_id: str,
    ) -> ControllerResource:
        """Return a canonical controller resource."""
        resource = self.controller_resources.get(
            resource_id
        )

        if resource is None:
            raise KeyError(
                "Unknown controller resource: "
                f"{resource_id}"
            )

        return resource

    def remove_controller_resource(
        self,
        resource_id: str,
    ) -> ControllerResource:
        """Remove a controller resource from the canonical model."""
        resource = self.controller_resources.get(
            resource_id
        )

        if resource is None:
            raise KeyError(
                "Unknown controller resource: "
                f"{resource_id}"
            )

        for machine in self.machines.values():
            if resource_id in machine.controller_resource_ids:
                machine.controller_resource_ids.remove(
                    resource_id
                )

        del self.controller_resources[
            resource_id
        ]

        return resource

    def _has_canonical_object(
        self,
        object_id: str,
    ) -> bool:
        """Return whether an ID belongs to a canonical model object."""
        return (
            object_id in self.machines
            or object_id in self.components
            or object_id in self.hardware_definitions
            or object_id in self.ports
            or object_id in self.functions
            or object_id in self.capabilities
            or object_id in self.controllers
            or object_id in self.controller_resources
        )

    def add_relationship(
        self,
        relationship: Any,
    ) -> None:
        """Add a semantic relationship between canonical objects."""
        if relationship.id in self.relationships:
            raise ValueError(
                "Relationship already exists: "
                f"{relationship.id}"
            )

        if (
            not self._has_canonical_object(
                relationship.source_id
            )
        ):
            raise ValueError(
                "Unknown relationship source: "
                f"{relationship.source_id}"
            )

        if (
            not self._has_canonical_object(
                relationship.target_id
            )
        ):
            raise ValueError(
                "Unknown relationship target: "
                f"{relationship.target_id}"
            )

        for existing in self.relationships.values():
            if (
                existing.source_id
                == relationship.source_id
                and existing.target_id
                == relationship.target_id
                and existing.relationship_type
                == relationship.relationship_type
            ):
                raise ValueError(
                    "That semantic relationship already exists."
                )

        self.relationships[
            relationship.id
        ] = relationship

    def get_relationship(
        self,
        relationship_id: str,
    ) -> Any:
        """Return a canonical semantic relationship."""
        relationship = self.relationships.get(
            relationship_id
        )

        if relationship is None:
            raise KeyError(
                f"Unknown relationship: {relationship_id}"
            )

        return relationship

    def remove_relationship(
        self,
        relationship_id: str,
    ) -> Any:
        """Remove a semantic relationship."""
        relationship = self.relationships.get(
            relationship_id
        )

        if relationship is None:
            raise KeyError(
                f"Unknown relationship: {relationship_id}"
            )

        del self.relationships[
            relationship_id
        ]

        return relationship

    def add_connection(
        self,
        connection: Any,
    ) -> None:
        """Add a canonical physical connection between two ports."""
        if connection.id in self.connections:
            raise ValueError(
                f"Connection already exists: {connection.id}"
            )

        if (
            connection.endpoint_a_id
            == connection.endpoint_b_id
        ):
            raise ValueError(
                "A connection cannot connect a port to itself."
            )

        if (
            connection.endpoint_a_id
            not in self.ports
        ):
            raise ValueError(
                "Unknown connection endpoint: "
                f"{connection.endpoint_a_id}"
            )

        if (
            connection.endpoint_b_id
            not in self.ports
        ):
            raise ValueError(
                "Unknown connection endpoint: "
                f"{connection.endpoint_b_id}"
            )

        for existing in self.connections.values():
            if existing.connects_same_ports(
                connection.endpoint_a_id,
                connection.endpoint_b_id,
            ):
                raise ValueError(
                    "That canonical connection already exists."
                )

        self.connections[
            connection.id
        ] = connection

    def remove_connection(
        self,
        connection_id: str,
    ) -> Any:
        """Remove a canonical physical connection."""
        connection = self.connections.get(
            connection_id
        )

        if connection is None:
            raise KeyError(
                f"Unknown connection: {connection_id}"
            )

        del self.connections[
            connection_id
        ]

        return connection

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

    def get_function(
        self,
        function_id: str,
    ) -> Function:
        """Return a canonical Function."""
        function = self.functions.get(
            function_id
        )

        if function is None:
            raise KeyError(
                f"Unknown function: {function_id}"
            )

        return function

    def get_capability(
        self,
        capability_id: str,
    ) -> Capability:
        """Return a canonical Capability."""
        capability = self.capabilities.get(
            capability_id
        )

        if capability is None:
            raise KeyError(
                f"Unknown capability: {capability_id}"
            )

        return capability