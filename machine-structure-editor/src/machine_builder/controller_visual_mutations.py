"""Mutations for controller visual authoring."""

from __future__ import annotations

from dataclasses import dataclass

from .controller import Controller
from .controller_queries import (
    get_controller,
    machine_id_for_controller,
)
from .editor_state import EditorState
from .semantic_model import Machine
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

        state.visual_model.add_node(
            self.node
        )