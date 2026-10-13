"""Mutations for controller visual authoring."""

from __future__ import annotations

from dataclasses import dataclass

from .controller import Controller
from .controller_board_fixtures import (
    add_duet_2_maestro_physical_interfaces,
)
from .controller_queries import (
    get_controller,
    machine_id_for_controller,
)
from .editor_state import EditorState
from .semantic_model import (
    Machine,
    Provenance,
    SemanticPort,
)
from .semantic_projection import (
    project_controller_ports,
)
from .visual_model import VisualNode


@dataclass(frozen=True)
class CreateControllerNode:
    """Create a canonical controller and its visual representation."""

    controller: Controller
    node: VisualNode
    machine_id: str = "machine-1"

    def apply(
        self,
        state: EditorState,
    ) -> None:
        if self.node.node_type != "controller":
            raise ValueError(
                "Controller visual nodes must use "
                "node_type='controller'."
            )

        if self.node.semantic_reference is not None:
            raise ValueError(
                "New controller visual node already has "
                "a canonical reference: "
                f"{self.node.semantic_reference}"
            )

        if self.node.id in state.visual_model.nodes:
            raise ValueError(
                "Visual node already exists: "
                f"{self.node.id}"
            )

        if self.controller.id in (
            state.semantic_model.controllers
        ):
            raise ValueError(
                "Controller already exists: "
                f"{self.controller.id}"
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

        state.semantic_model.add_controller(
            self.machine_id,
            self.controller,
        )

        self.node.semantic_reference = (
            self.controller.id
        )
        self.node.label = self.controller.name

        project_controller_ports(
            self.controller,
            state.semantic_model,
            self.node,
        )
        state.visual_model.add_node(
            self.node
        )


@dataclass(frozen=True)
class CreateControllerVisualNode:
    """Link an existing canonical controller to a visual node."""

    controller_id: str
    node: VisualNode

    def apply(
        self,
        state: EditorState,
    ) -> None:
        if self.node.node_type != "controller":
            raise ValueError(
                "Controller visual nodes must use "
                "node_type='controller'."
            )

        if self.node.semantic_reference is not None:
            if (
                self.node.semantic_reference
                != self.controller_id
            ):
                raise ValueError(
                    "Visual node already references a "
                    "different canonical object: "
                    f"{self.node.semantic_reference}"
                )

            raise ValueError(
                "Visual node already references a "
                "canonical object: "
                f"{self.node.semantic_reference}"
            )

        controller = get_controller(
            state,
            self.controller_id,
        )

        machine_id_for_controller(
            state,
            controller.id,
        )

        if self.node.id in state.visual_model.nodes:
            raise ValueError(
                "Visual node already exists: "
                f"{self.node.id}"
            )

        self.node.semantic_reference = (
            controller.id
        )
        self.node.label = controller.name

        project_controller_ports(
            controller,
            state.semantic_model,
            self.node,
        )
        state.visual_model.add_node(
            self.node
        )

@dataclass(frozen=True)
class CreateDuet2MaestroControllerNode:
    """Atomically create a V1.0 reference-board controller and visual node."""

    controller_id: str
    node: VisualNode
    machine_id: str = "machine-1"

    def apply(
        self,
        state: EditorState,
    ) -> None:
        if self.node.node_type != "controller":
            raise ValueError(
                "Controller visual nodes must use "
                "node_type='controller'."
            )

        if self.node.semantic_reference is not None:
            raise ValueError(
                "New controller visual node already has "
                "a canonical reference: "
                f"{self.node.semantic_reference}"
            )

        if self.node.id in state.visual_model.nodes:
            raise ValueError(
                "Visual node already exists: "
                f"{self.node.id}"
            )

        if self.controller_id in state.semantic_model.controllers:
            raise ValueError(
                "Controller already exists: "
                f"{self.controller_id}"
            )

        if not state.semantic_model.machines:
            state.semantic_model.add_machine(
                Machine(
                    id=self.machine_id,
                    name="M3D Promega \u2014 Compound reference specimen (not verified as-built)",
                )
            )

        if self.machine_id not in state.semantic_model.machines:
            raise ValueError(
                f"Unknown machine: {self.machine_id}"
            )

        controller, _ports = add_duet_2_maestro_physical_interfaces(
            model=state.semantic_model,
            machine_id=self.machine_id,
            controller_id=self.controller_id,
            label=self.node.label,
        )

        # The selected definition is the V1.0 reference model. The
        # physical board revision has not been independently verified.
        controller.version = None
        controller.properties["physical_revision_status"] = (
            "not_verified_as_built"
        )

        # Separate connector-level interface endpoint; preserve all four
        # Board-owned J9 contact ports and their existing identities.
        state.semantic_model.add_port(
            SemanticPort(
                id=f"{controller.id}-x-motor-interface",
                component_id=None,
                controller_id=controller.id,
                purpose="J9 / X Motor functional interface",
                direction="unknown",
                connector_id="x-motor",
                pin_id=None,
                properties={
                    "interface_role": "motor_connector_interface",
                    "interface_granularity": "connector_level",
                    "connector_label": "J9 / X Motor",
                    "pcb_reference_designator": "J9",
                    "visual_port_type": "motor",
                    "visual_side": "right",
                    "reference_scope": "functional_interface_only",
                    "physical_wiring_status": "not_verified_as_built",
                    "contact_mapping_status": "not_established",
                    "firmware_assignment_status": "not_established",
                },
                provenance=[
                    Provenance(
                        source=(
                            "Machine Builder #3 Controller/Board crosswalk: "
                            "Duet 2 Maestro J9 / X Motor connector identity"
                        ),
                        evidence_type="published",
                        method="reference-board connector crosswalk",
                        context=(
                            "The Board crosswalk identifies x-motor as J9 / X MOT. "
                            "This is a connector-level functional endpoint, "
                            "separate from individual contact ports."
                        ),
                        date="2026-10-13",
                        notes=(
                            "This evidence does not establish installed wiring, "
                            "cable mating-face positions, motor-terminal mapping, "
                            "coil pairing, or firmware assignment."
                        ),
                    )
                ],
            )
        )

        self.node.semantic_reference = controller.id
        self.node.label = controller.name

        project_controller_ports(
            controller,
            state.semantic_model,
            self.node,
        )
        state.visual_model.add_node(
            self.node
        )
