"""Tests for controller palette authoring."""

from PySide6.QtCore import QPointF

from machine_builder.canvas_palette import (
    CanvasPaletteMixin,
)
from machine_builder.persistence import load_editor_state
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


def test_generic_palette_templates_create_registered_components() -> None:
    canvas = PaletteTestCanvas()

    templates = (
        ("motor", "Motor"),
        ("sensor", "Sensor"),
        ("temperature_sensor", "Temperature Sensor"),
        ("component", "Component"),
        ("temperature_controller", "Temperature Controller"),
    )

    for index, (node_type, expected_label) in enumerate(
        templates,
        start=1,
    ):
        canvas.create_node_from_template(
            node_type=node_type,
            scene_position=QPointF(
                100.0 + index * 20.0,
                160.0 + index * 20.0,
            ),
        )

        node_id = f"node-{index}"
        component_id = f"component-{node_id}"
        node = canvas.store.model.nodes[node_id]
        component = canvas.store.semantic_model.components[
            component_id
        ]

        assert component.id == component_id
        assert component.id != node.id
        assert component.role == expected_label
        assert component.label == expected_label
        assert component.hardware_definition_id is None
        assert component.properties == {
            "visual_node_type": node_type,
        }
        assert component.port_ids == []

        assert node.node_type == node_type
        assert node.semantic_reference == component.id

        machine = canvas.store.semantic_model.machines[
            "machine-1"
        ]
        assert component.id in machine.component_ids

    assert canvas.store.semantic_model.controllers == {}
    assert canvas.store.semantic_model.hardware_definitions == {}
    assert len(canvas.store.semantic_model.components) == len(templates)


def test_generic_palette_creation_is_undoable_and_redoable() -> None:
    canvas = PaletteTestCanvas()

    canvas.create_node_from_template(
        node_type="motor",
        scene_position=QPointF(
            220.0,
            320.0,
        ),
    )

    assert "component-node-1" in canvas.store.semantic_model.components
    assert "node-1" in canvas.store.model.nodes

    assert canvas.store.undo()

    assert "component-node-1" not in canvas.store.semantic_model.components
    assert "node-1" not in canvas.store.model.nodes

    assert canvas.store.redo()

    assert "component-node-1" in canvas.store.semantic_model.components
    assert (
        canvas.store.model.nodes["node-1"].semantic_reference
        == "component-node-1"
    )


def test_generic_palette_component_round_trips_with_identity_and_ports(
    tmp_path,
) -> None:
    canvas = PaletteTestCanvas()

    canvas.create_node_from_template(
        node_type="motor",
        scene_position=QPointF(
            240.0,
            340.0,
        ),
    )

    component_id = "component-node-1"
    node_id = "node-1"
    original_node = canvas.store.model.nodes[node_id]
    provisional_port_ids = set(original_node.ports)

    path = tmp_path / "generic-component.machine.json"
    canvas.store.save(path)

    restored = load_editor_state(path)

    component = restored.semantic_model.components[component_id]
    node = restored.visual_model.nodes[node_id]

    assert component.id == component_id
    assert component.hardware_definition_id is None
    assert component.properties == {
        "visual_node_type": "motor",
    }
    assert component.id in restored.semantic_model.machines[
        "machine-1"
    ].component_ids

    assert node.semantic_reference == component.id
    assert set(node.ports) == provisional_port_ids
    assert all(
        node.ports[port_id].semantic_reference is None
        for port_id in provisional_port_ids
    )
    assert restored.semantic_model.controllers == {}
