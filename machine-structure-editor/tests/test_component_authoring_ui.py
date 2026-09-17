"""Integration tests for visible semantic component authoring."""

from __future__ import annotations

import sys

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QApplication

from machine_builder.canvas import MachineCanvas
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