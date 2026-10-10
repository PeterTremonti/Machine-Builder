"""Tests for controller palette authoring."""

from PySide6.QtCore import QPointF, Qt
import machine_builder.canvas_palette as canvas_palette_module

from machine_builder.canvas_palette import (
    CanvasPaletteMixin,
)
from machine_builder.controller_board_fixtures import (
    DUET_2_MAESTRO_CONNECTOR_LAYOUT,
)
from machine_builder.hardware_catalog import build_duet_2_maestro
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

def test_maestro_palette_option_is_explicit_reference_board(
    monkeypatch,
) -> None:
    class FakeSignal:
        def connect(self, callback) -> None:
            self.callback = callback

    class FakePaletteItem:
        def __init__(self, label: str) -> None:
            self.label = label
            self.data = {}
            self.tooltip = ""

        def setData(self, role, value) -> None:
            self.data[role] = value

        def setToolTip(self, value: str) -> None:
            self.tooltip = value

    class FakePalette:
        def __init__(self) -> None:
            self.items = []
            self.itemDoubleClicked = FakeSignal()

        def setMinimumWidth(self, value: int) -> None:
            self.minimum_width = value

        def setDragEnabled(self, value: bool) -> None:
            self.drag_enabled = value

        def addItem(self, item) -> None:
            self.items.append(item)

    monkeypatch.setattr(
        canvas_palette_module,
        "QListWidgetItem",
        FakePaletteItem,
    )

    canvas = PaletteTestCanvas()
    canvas.palette = FakePalette()
    canvas._build_palette()

    named_items = [
        item
        for item in canvas.palette.items
        if item.data.get(Qt.ItemDataRole.UserRole)
        == "duet_2_maestro_v1_0"
    ]
    generic_items = [
        item
        for item in canvas.palette.items
        if item.data.get(Qt.ItemDataRole.UserRole)
        == "controller"
    ]

    assert len(named_items) == 1
    assert named_items[0].label == "Duet 2 Maestro v1.0"
    assert "does not verify" in named_items[0].tooltip
    assert "physical board revision" in named_items[0].tooltip

    assert len(generic_items) == 1
    assert generic_items[0].label == "Controller"


def test_maestro_palette_creation_is_atomic_undoable_and_redoable() -> None:
    canvas = PaletteTestCanvas()

    canvas.create_node_from_template(
        node_type="duet_2_maestro_v1_0",
        scene_position=QPointF(
            120.0,
            240.0,
        ),
    )

    semantic_model = canvas.store.semantic_model
    controller = semantic_model.controllers["controller-1"]
    definition = semantic_model.hardware_definitions[
        "duet-2-maestro-v1-0"
    ]
    node = canvas.store.model.nodes["node-1"]

    expected_definition = build_duet_2_maestro()
    expected_port_count = sum(
        position_count
        for _connector_id, _connector_name, position_count
        in DUET_2_MAESTRO_CONNECTOR_LAYOUT
    )
    installed_ports = [
        semantic_model.ports[port_id]
        for port_id in controller.port_ids
    ]

    assert definition.id == "duet-2-maestro-v1-0"
    assert definition.provenance == expected_definition.provenance
    assert controller.hardware_definition_id == definition.id
    assert controller.name == "Duet 2 Maestro v1.0"
    assert controller.controller_type == "motion_controller"
    assert controller.version is None
    assert controller.properties["physical_revision_status"] == (
        "not_verified_as_built"
    )

    assert semantic_model.machines["machine-1"].name == (
        "M3D Promega \u2014 Compound reference specimen "
        "(not verified as-built)"
    )
    assert semantic_model.machines["machine-1"].controller_ids == [
        controller.id
    ]

    assert len(controller.port_ids) == expected_port_count
    assert len(installed_ports) == expected_port_count
    assert len({port.id for port in installed_ports}) == expected_port_count
    assert all(
        port.controller_id == controller.id
        and port.component_id is None
        and port.pin_id is not None
        for port in installed_ports
    )
    assert {
        port.connector_id
        for port in installed_ports
    } == {
        connector_id
        for connector_id, _connector_name, _position_count
        in DUET_2_MAESTRO_CONNECTOR_LAYOUT
    }
    assert definition.provenance

    j4_ports = [
        port
        for port in installed_ports
        if port.connector_id == "j4"
    ]
    assert len(j4_ports) == 4
    assert {port.pin_id for port in j4_ports} == {
        "1",
        "2",
        "3",
        "4",
    }

    assert node.node_type == "controller"
    assert node.label == "Duet 2 Maestro v1.0"
    assert node.semantic_reference == controller.id
    assert len(node.ports) == expected_port_count
    assert {
        port.semantic_reference
        for port in node.ports.values()
    } == set(controller.port_ids)
    assert set(node.ports).isdisjoint(set(controller.port_ids))

    created_controller_ids = set(semantic_model.controllers)
    created_port_ids = set(semantic_model.ports)
    created_definition_ids = set(semantic_model.hardware_definitions)
    created_node_ids = set(canvas.store.model.nodes)

    assert canvas.store.undo()
    assert canvas.store.semantic_model.controllers == {}
    assert canvas.store.semantic_model.ports == {}
    assert canvas.store.semantic_model.hardware_definitions == {}
    assert canvas.store.semantic_model.machines == {}
    assert canvas.store.model.nodes == {}

    for mapping_name in ("controller_resources", "relationships"):
        mapping = getattr(canvas.store.semantic_model, mapping_name, None)
        if mapping is not None:
            assert mapping == {}

    assert canvas.store.redo()
    assert set(canvas.store.semantic_model.controllers) == created_controller_ids
    assert set(canvas.store.semantic_model.ports) == created_port_ids
    assert set(canvas.store.semantic_model.hardware_definitions) == created_definition_ids
    assert set(canvas.store.model.nodes) == created_node_ids

    restored_controller = canvas.store.semantic_model.controllers[
        "controller-1"
    ]
    restored_node = canvas.store.model.nodes["node-1"]
    assert restored_controller.hardware_definition_id == (
        "duet-2-maestro-v1-0"
    )
    assert len(restored_controller.port_ids) == expected_port_count
    assert {
        port.semantic_reference
        for port in restored_node.ports.values()
    } == set(restored_controller.port_ids)
