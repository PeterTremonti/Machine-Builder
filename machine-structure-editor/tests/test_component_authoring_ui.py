"""Integration tests for visible semantic component authoring."""

from __future__ import annotations

import sys

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication, QDialog, QPushButton

import machine_builder.canvas_editing as canvas_editing
from machine_builder.canvas import MachineCanvas
from machine_builder.persistence import load_editor_state
from machine_builder.port_details import PortDetailsResult
from machine_builder.semantic_component_mutations import (
    UpdateMachineComponent,
)
from machine_builder.semantic_model import (
    Machine,
    MachineComponent,
    SemanticPort,
)
from machine_builder.semantic_port_mutations import (
    UpdateSemanticPort,
)
from machine_builder.visual_model import VisualPort


def _application() -> QApplication:
    application = QApplication.instance()

    if application is None:
        application = QApplication(sys.argv)

    return application


def make_canvas() -> MachineCanvas:
    _application()

    canvas = MachineCanvas()

    canvas.store.semantic_model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    canvas.store.semantic_model.add_component(
        "machine-1",
        MachineComponent(
            id="component-1",
            role="motor",
            label="Original Motor",
        ),
    )

    canvas.store.semantic_model.add_port(
        SemanticPort(
            id="port-1",
            component_id="component-1",
            purpose="Signal",
            direction="input",
        )
    )

    canvas.create_node_from_template(
        node_type="motor",
        scene_position=QPointF(
            100.0,
            100.0,
        ),
    )

    node = next(
        iter(
            canvas.store.model.nodes.values()
        )
    )

    node.semantic_reference = (
        "component-1"
    )

    node.add_port(
        VisualPort(
            id="port-1",
            node_id=node.id,
            label="Signal",
            port_type="signal",
            direction="input",
            semantic_reference="port-1",
            side="right",
            order=2,
        )
    )

    canvas._model_changed(
        canvas.store.model
    )

    return canvas


def test_port_properties_can_be_committed() -> None:
    canvas = make_canvas()

    canvas.store.commit(
        UpdateSemanticPort(
            port_id="port-1",
            properties={
                "voltage": "24",
                "protocol": "PWM",
            },
        )
    )

    port = (
        canvas.store.semantic_model.ports[
            "port-1"
        ]
    )

    assert port.properties == {
        "voltage": "24",
        "protocol": "PWM",
    }


def test_port_properties_are_undoable() -> None:
    canvas = make_canvas()

    canvas.store.commit(
        UpdateSemanticPort(
            port_id="port-1",
            properties={
                "voltage": "24",
            },
        )
    )

    assert canvas.store.undo()

    assert (
        canvas.store.semantic_model.ports[
            "port-1"
        ].properties
        == {}
    )


def test_port_properties_are_redoable() -> None:
    canvas = make_canvas()

    canvas.store.commit(
        UpdateSemanticPort(
            port_id="port-1",
            properties={
                "voltage": "24",
            },
        )
    )

    assert canvas.store.undo()
    assert canvas.store.redo()

    assert (
        canvas.store.semantic_model.ports[
            "port-1"
        ].properties
        == {
            "voltage": "24",
        }
    )


def test_port_edit_updates_visual_port() -> None:
    canvas = make_canvas()

    canvas.store.commit(
        UpdateSemanticPort(
            port_id="port-1",
            purpose="Motor Command",
            direction="output",
        )
    )

    node = next(
        iter(
            canvas.store.model.nodes.values()
        )
    )

    visual_port = node.ports[
        "port-1"
    ]

    assert visual_port.label == (
        "Motor Command"
    )

    assert visual_port.direction == (
        "output"
    )


def test_component_editing_changes_canonical_component() -> None:
    canvas = make_canvas()

    canvas.store.commit(
        UpdateMachineComponent(
            component_id="component-1",
            role="drive motor",
            label="Drive Motor",
        )
    )

    component = (
        canvas.store.semantic_model.components[
            "component-1"
        ]
    )

    assert component.role == (
        "drive motor"
    )

    assert component.label == (
        "Drive Motor"
    )


def test_component_editing_updates_visual_label() -> None:
    canvas = make_canvas()

    canvas.store.commit(
        UpdateMachineComponent(
            component_id="component-1",
            label="Drive Motor",
        )
    )

    node = next(
        iter(
            canvas.store.model.nodes.values()
        )
    )

    assert node.label == "Drive Motor"


def test_component_editing_is_undoable() -> None:
    canvas = make_canvas()

    canvas.store.commit(
        UpdateMachineComponent(
            component_id="component-1",
            role="drive motor",
            label="Drive Motor",
        )
    )

    assert canvas.store.undo()

    component = (
        canvas.store.semantic_model.components[
            "component-1"
        ]
    )

    assert component.role == "motor"
    assert component.label == "Original Motor"


def test_component_properties_are_editable() -> None:
    canvas = make_canvas()

    canvas.store.commit(
        UpdateMachineComponent(
            component_id="component-1",
            properties={
                "axis": "X",
                "voltage": "24",
            },
        )
    )

    component = (
        canvas.store.semantic_model.components[
            "component-1"
        ]
    )

    assert component.properties == {
        "axis": "X",
        "voltage": "24",
    }


def test_component_properties_are_undoable() -> None:
    canvas = make_canvas()

    canvas.store.commit(
        UpdateMachineComponent(
            component_id="component-1",
            properties={
                "axis": "X",
            },
        )
    )

    assert canvas.store.undo()

    component = (
        canvas.store.semantic_model.components[
            "component-1"
        ]
    )

    assert component.properties == {}


def test_component_properties_support_unknown_fields() -> None:
    canvas = make_canvas()

    canvas.store.commit(
        UpdateMachineComponent(
            component_id="component-1",
            properties={
                "manufacturer_model": "XYZ-123",
                "datasheet": "unknown",
            },
        )
    )

    component = (
        canvas.store.semantic_model.components[
            "component-1"
        ]
    )

    assert (
        component.properties[
            "manufacturer_model"
        ]
        == "XYZ-123"
    )

    assert (
        component.properties[
            "datasheet"
        ]
        == "unknown"
    )


def test_canvas_port_graphics_has_port_edit_callback() -> None:
    canvas = make_canvas()

    node = next(
        iter(
            canvas._node_items.values()
        )
    )

    port = node._port_items.get(
        "port-1"
    )

    assert port is not None


def test_port_edit_updates_canonical_port() -> None:
    canvas = make_canvas()

    canvas.store.commit(
        UpdateSemanticPort(
            port_id="port-1",
            purpose="Motor Command",
            direction="output",
            connector_id="J4",
            pin_id="PA7",
        )
    )

    port = (
        canvas.store.semantic_model.ports[
            "port-1"
        ]
    )

    assert port.purpose == (
        "Motor Command"
    )

    assert port.direction == "output"
    assert port.connector_id == "J4"
    assert port.pin_id == "PA7"


def test_port_edit_is_undoable() -> None:
    canvas = make_canvas()

    canvas.store.commit(
        UpdateSemanticPort(
            port_id="port-1",
            purpose="Motor Command",
            direction="output",
        )
    )

    assert canvas.store.undo()

    port = (
        canvas.store.semantic_model.ports[
            "port-1"
        ]
    )

    assert port.purpose == "Signal"
    assert port.direction == "input"


def test_add_port_button_commits_component_owned_semantic_port(
    monkeypatch,
) -> None:
    canvas = make_canvas()

    node_item = next(iter(canvas._node_items.values()))
    node_item.setSelected(True)

    assert node_item in canvas.scene.selectedItems()

    result = PortDetailsResult(
        purpose="PT1000 Sensor",
        direction="input",
        connector_id=None,
        pin_id=None,
        properties={},
    )

    class AcceptedPortDetailsDialog:
        DialogCode = QDialog.DialogCode

        def __init__(
            self,
            port,
            component_label,
            parent=None,
        ) -> None:
            assert port.component_id == "component-1"
            assert port.controller_id is None
            assert port.connector_id is None
            assert port.pin_id is None
            assert component_label == "Original Motor"

        def exec(self) -> int:
            return self.DialogCode.Accepted

        def result_data(self) -> PortDetailsResult:
            return result

    monkeypatch.setattr(
        canvas_editing,
        "PortDetailsDialog",
        AcceptedPortDetailsDialog,
    )

    add_port_button = next(
        button
        for button in canvas.findChildren(QPushButton)
        if button.text() == "Add Port..."
    )

    add_port_button.click()

    component = canvas.store.semantic_model.components[
        "component-1"
    ]
    created_port = next(
        port
        for port in canvas.store.semantic_model.ports.values()
        if port.purpose == "PT1000 Sensor"
    )

    assert created_port.component_id == component.id
    assert created_port.controller_id is None
    assert created_port.connector_id is None
    assert created_port.pin_id is None
    assert created_port.id in component.port_ids

    visual_node = next(
        node
        for node in canvas.store.model.nodes.values()
        if node.semantic_reference == component.id
    )
    assert any(
        visual_port.semantic_reference == created_port.id
        for visual_port in visual_node.ports.values()
    )


def test_palette_created_component_can_add_port_and_round_trip(
    monkeypatch,
    tmp_path,
) -> None:
    _application()
    canvas = MachineCanvas()

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

    assert len(provisional_port_ids) == 2
    assert all(
        original_node.ports[port_id].semantic_reference is None
        for port_id in provisional_port_ids
    )

    node_item = canvas._node_items[node_id]
    node_item.setSelected(True)

    result = PortDetailsResult(
        purpose="PT1000 Sensor",
        direction="input",
        connector_id=None,
        pin_id=None,
        properties={},
    )

    class AcceptedPortDetailsDialog:
        DialogCode = QDialog.DialogCode

        def __init__(
            self,
            port,
            component_label,
            parent=None,
        ) -> None:
            assert port.component_id == component_id
            assert port.controller_id is None
            assert component_label == "Motor"

        def exec(self) -> int:
            return self.DialogCode.Accepted

        def result_data(self) -> PortDetailsResult:
            return result

    monkeypatch.setattr(
        canvas_editing,
        "PortDetailsDialog",
        AcceptedPortDetailsDialog,
    )

    add_port_button = next(
        button
        for button in canvas.findChildren(QPushButton)
        if button.text() == "Add Port..."
    )
    add_port_button.click()

    component = canvas.store.semantic_model.components[component_id]
    created_port = next(
        port
        for port in canvas.store.semantic_model.ports.values()
        if port.purpose == "PT1000 Sensor"
    )
    visual_node = canvas.store.model.nodes[node_id]

    assert created_port.component_id == component.id
    assert created_port.controller_id is None
    assert created_port.connector_id is None
    assert created_port.pin_id is None
    assert created_port.id in component.port_ids

    assert provisional_port_ids.issubset(visual_node.ports)
    assert all(
        visual_node.ports[port_id].semantic_reference is None
        for port_id in provisional_port_ids
    )
    assert sum(
        port.semantic_reference == created_port.id
        for port in visual_node.ports.values()
    ) == 1

    path = tmp_path / "palette-component-with-port.machine.json"
    canvas.store.save(path)

    restored = load_editor_state(path)
    restored_component = restored.semantic_model.components[component_id]
    restored_node = restored.visual_model.nodes[node_id]

    assert restored_component.id == component.id
    assert restored_component.hardware_definition_id is None
    assert restored_component.properties == {
        "visual_node_type": "motor",
    }
    assert restored_component.id in restored.semantic_model.machines[
        "machine-1"
    ].component_ids

    restored_port = restored.semantic_model.ports[created_port.id]
    assert restored_port.component_id == restored_component.id
    assert restored_port.id in restored_component.port_ids
    assert restored_node.semantic_reference == restored_component.id

    assert provisional_port_ids.issubset(restored_node.ports)
    assert all(
        restored_node.ports[port_id].semantic_reference is None
        for port_id in provisional_port_ids
    )
    assert sum(
        port.semantic_reference == restored_port.id
        for port in restored_node.ports.values()
    ) == 1
    assert restored.semantic_model.controllers == {}
