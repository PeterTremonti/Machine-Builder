"""Explicit editor-model mutations.

User-visible editing operations are represented as mutations instead of
allowing UI code to directly manipulate either model.

The editor state contains both:
    * the visual model
    * the canonical semantic model

V0.2 semantic authoring mutations update both sides as one atomic
user action.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .editor_state import EditorState
from .hardware_catalog import (
    build_generic_4010_24v_fan,
)
from .semantic_model import (
    Machine,
    MachineComponent,
    SemanticPort,
)
from .semantic_projection import (
    project_component_ports,
)
from .visual_model import (
    VisualConnection,
    VisualNode,
)


class Mutation(Protocol):
    """Protocol implemented by all editor mutations."""

    def apply(
        self,
        state: EditorState,
    ) -> None:
        """Apply this mutation to the complete editor state."""
        ...


def _create_canonical_fan_data(
    component_id: str,
) -> tuple[
    object,
    tuple[SemanticPort, SemanticPort],
]:
    """Create canonical hardware and ports for the real test fan."""
    hardware, ports = (
        build_generic_4010_24v_fan()
    )

    corrected_ports = tuple(
        SemanticPort(
            id=port.id,
            component_id=component_id,
            purpose=port.purpose,
            direction=port.direction,
            connector_id=port.connector_id,
            pin_id=port.pin_id,
            properties=port.properties.copy(),
            provenance=port.provenance.copy(),
        )
        for port in ports
    )

    return (
        hardware,
        corrected_ports,
    )


@dataclass(frozen=True)
class CreateNode:
    """Create a visual node and its canonical machine component."""

    node: VisualNode
    machine_id: str = "machine-1"

    def apply(
        self,
        state: EditorState,
    ) -> None:
        if (
            self.node.semantic_reference
            is not None
        ):
            raise ValueError(
                "New visual node already has a canonical "
                "semantic reference: "
                f"{self.node.semantic_reference}"
            )

        if not state.semantic_model.machines:
            state.semantic_model.add_machine(
                Machine(
                    id=self.machine_id,
                    name="Untitled Machine",
                )
            )

        if self.machine_id not in (
            state.semantic_model.machines
        ):
            raise ValueError(
                f"Unknown machine: {self.machine_id}"
            )

        component_id = (
            f"component-{self.node.id}"
        )

        component = MachineComponent(
            id=component_id,
            role=(
                self.node.label
                or self.node.node_type
            ),
            label=self.node.label,
            properties={
                "visual_node_type": self.node.node_type,
            },
        )

        if (
            self.node.node_type
            == "part_cooling_fan"
        ):
            (
                hardware,
                semantic_ports,
            ) = _create_canonical_fan_data(
                component_id
            )

            if (
                hardware.id
                in state.semantic_model.hardware_definitions
            ):
                existing_hardware = (
                    state.semantic_model
                    .hardware_definitions[
                        hardware.id
                    ]
                )

                if existing_hardware != hardware:
                    raise ValueError(
                        "Hardware definition ID already exists "
                        "with different data: "
                        f"{hardware.id}"
                    )
            else:
                state.semantic_model.add_hardware_definition(
                    hardware
                )

            component.hardware_definition_id = (
                hardware.id
            )

            state.semantic_model.add_component(
                self.machine_id,
                component,
            )

            for port in semantic_ports:
                state.semantic_model.add_port(
                    port
                )

            self.node.semantic_reference = (
                component.id
            )

            # The canonical ports are authoritative. The projection
            # decides how those ports should appear visually.
            project_component_ports(
                component,
                state.semantic_model,
                self.node,
            )

            state.visual_model.add_node(
                self.node
            )

            return

        state.semantic_model.add_component(
            self.machine_id,
            component,
        )

        self.node.semantic_reference = (
            component.id
        )

        state.visual_model.add_node(
            self.node
        )


@dataclass(frozen=True)
class CreateMachineComponent:
    """Create a canonical component and its visual representation."""

    machine_id: str
    component: MachineComponent
    node: VisualNode

    def apply(
        self,
        state: EditorState,
    ) -> None:
        if (
            self.node.semantic_reference is not None
            and self.node.semantic_reference
            != self.component.id
        ):
            raise ValueError(
                "Visual node already references a different "
                "canonical component: "
                f"{self.node.semantic_reference}"
            )

        self.node.semantic_reference = (
            self.component.id
        )

        state.semantic_model.add_component(
            self.machine_id,
            self.component,
        )

        state.visual_model.add_node(
            self.node
        )


@dataclass(frozen=True)
class MoveNodes:
    """Move one or more visual nodes as one atomic user action."""

    positions: dict[
        str,
        tuple[float, float],
    ]

    def apply(
        self,
        state: EditorState,
    ) -> None:
        for node_id, (
            x,
            y,
        ) in self.positions.items():
            node = state.visual_model.nodes.get(
                node_id
            )

            if node is None:
                raise KeyError(
                    f"Unknown visual node: {node_id}"
                )

            node.x = x
            node.y = y


@dataclass(frozen=True)
class DeleteNodes:
    """Delete visual nodes and their canonical components."""

    node_ids: tuple[str, ...]

    def apply(
        self,
        state: EditorState,
    ) -> None:
        for node_id in self.node_ids:
            node = state.visual_model.nodes.get(
                node_id
            )

            if node is None:
                raise KeyError(
                    f"Unknown visual node: {node_id}"
                )

            component_id = (
                node.semantic_reference
            )

            state.visual_model.remove_node(
                node_id
            )

            if component_id is not None:
                if component_id in (
                    state.semantic_model.components
                ):
                    state.semantic_model.remove_component(
                        component_id
                    )


@dataclass(frozen=True)
class CreateConnection:
    """Create a physical visual connection between two visual ports."""

    connection_id: str
    endpoint_a_id: str
    endpoint_b_id: str
    connection_type: str = "unknown"

    def apply(
        self,
        state: EditorState,
    ) -> None:
        connection = VisualConnection(
            id=self.connection_id,
            endpoint_a_id=self.endpoint_a_id,
            endpoint_b_id=self.endpoint_b_id,
            connection_type=self.connection_type,
        )

        state.visual_model.add_connection(
            connection
        )


@dataclass(frozen=True)
class DeleteConnection:
    """Delete an existing visual connection."""

    connection_id: str

    def apply(
        self,
        state: EditorState,
    ) -> None:
        state.visual_model.remove_connection(
            self.connection_id
        )