"""Tests for controller palette authoring."""

from PySide6.QtCore import QPointF

from machine_builder.canvas_palette import (
    CanvasPaletteMixin,
)
from machine_builder.store import ModelStore


class FakeStatusBar:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def showMessage(
        self,
        message: str,
    ) -> None:
        self.messages.append(
            message
        )


class PaletteTestCanvas(
    CanvasPaletteMixin
):
    def __init__(self) -> None:
        self.store = ModelStore()
        self._node_counter = 0
        self._last_edit_position = QPointF(
            100.0,
            100.0,
        )
        self._status_bar = FakeStatusBar()

    def statusBar(
        self,
    ) -> FakeStatusBar:
        return self._status_bar


def test_controller_palette_creation_creates_canonical_controller() -> None:
    canvas = PaletteTestCanvas()

    canvas.create_node_from_template(
        node_type="controller",
        scene_position=QPointF(
            120.0,
            240.0,
        ),
    )

    assert (
        "controller-1"
        in canvas.store.semantic_model.controllers
    )

    controller = (
        canvas.store.semantic_model.controllers[
            "controller-1"
        ]
    )

    assert controller.name == "Controller"
    assert controller.controller_type == "controller"


def test_controller_palette_creation_links_visual_node() -> None:
    canvas = PaletteTestCanvas()

    canvas.create_node_from_template(
        node_type="controller",
        scene_position=QPointF(
            120.0,
            240.0,
        ),
    )

    node = (
        canvas.store.model.nodes[
            "node-1"
        ]
    )

    assert node.node_type == "controller"
    assert (
        node.semantic_reference
        == "controller-1"
    )
    assert node.label == "Controller"
    assert node.x == 120.0
    assert node.y == 240.0


def test_controller_palette_creation_does_not_create_fake_ports() -> None:
    canvas = PaletteTestCanvas()

    canvas.create_node_from_template(
        node_type="controller",
        scene_position=QPointF(
            120.0,
            240.0,
        ),
    )

    node = (
        canvas.store.model.nodes[
            "node-1"
        ]
    )

    assert node.ports == {}


def test_controller_palette_creation_attaches_controller_to_machine() -> None:
    canvas = PaletteTestCanvas()

    canvas.create_node_from_template(
        node_type="controller",
        scene_position=QPointF(
            120.0,
            240.0,
        ),
    )

    machine = (
        canvas.store.semantic_model.machines[
            "machine-1"
        ]
    )

    assert machine.controller_ids == [
        "controller-1"
    ]


def test_controller_palette_creation_is_undoable_and_redoable() -> None:
    canvas = PaletteTestCanvas()

    canvas.create_node_from_template(
        node_type="controller",
        scene_position=QPointF(
            120.0,
            240.0,
        ),
    )

    assert canvas.store.undo()

    assert (
        "controller-1"
        not in canvas.store.semantic_model.controllers
    )
    assert (
        "node-1"
        not in canvas.store.model.nodes
    )

    assert canvas.store.redo()

    assert (
        "controller-1"
        in canvas.store.semantic_model.controllers
    )
    assert (
        canvas.store.model.nodes[
            "node-1"
        ].semantic_reference
        == "controller-1"
    )


def test_non_controller_palette_creation_creates_canonical_component() -> None:
    canvas = PaletteTestCanvas()

    canvas.create_node_from_template(
        node_type="motor",
        scene_position=QPointF(
            200.0,
            300.0,
        ),
    )

    assert (
        canvas.store.semantic_model.controllers
        == {}
    )

    assert (
        "component-node-1"
        in canvas.store.semantic_model.components
    )

    component = (
        canvas.store.semantic_model.components[
            "component-node-1"
        ]
    )

    assert component.label == "Motor"
    assert component.role == "Motor"
    assert component.properties[
        "visual_node_type"
    ] == "motor"

    node = (
        canvas.store.model.nodes[
            "node-1"
        ]
    )

    assert node.node_type == "motor"
    assert (
        node.semantic_reference
        == "component-node-1"
    )
    assert len(node.ports) == 2