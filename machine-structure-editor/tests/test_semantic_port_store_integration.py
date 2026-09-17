"""Integration tests for semantic port edits through ModelStore."""

from machine_builder.editor_state import (
    EditorState,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
    SemanticPort,
)
from machine_builder.semantic_port_mutations import (
    UpdateSemanticPort,
)
from machine_builder.store import ModelStore
from machine_builder.visual_model import (
    VisualModel,
    VisualNode,
    VisualPort,
)


def make_store() -> ModelStore:
    semantic_model = CanonicalMachineModel()

    semantic_model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    semantic_model.add_component(
        "machine-1",
        MachineComponent(
            id="component-1",
            role="motor",
            label="X Motor",
        ),
    )

    semantic_model.add_port(
        SemanticPort(
            id="port-1",
            component_id="component-1",
            purpose="Signal",
            direction="input",
        )
    )

    visual_model = VisualModel()

    node = VisualNode(
        id="node-1",
        node_type="motor",
        label="X Motor",
        semantic_reference="component-1",
    )

    node.add_port(
        VisualPort(
            id="port-1",
            node_id="node-1",
            label="Signal",
            port_type="signal",
            direction="input",
            semantic_reference="port-1",
        )
    )

    visual_model.add_node(
        node
    )

    return ModelStore(
        model=visual_model,
        semantic_model=semantic_model,
    )


def test_store_commits_port_edit() -> None:
    store = make_store()

    store.commit(
        UpdateSemanticPort(
            port_id="port-1",
            purpose="Motor Command",
            direction="output",
            connector_id="J4",
            pin_id="PA7",
        )
    )

    port = (
        store.semantic_model.ports[
            "port-1"
        ]
    )

    visual_port = (
        store.model.nodes[
            "node-1"
        ].ports["port-1"]
    )

    assert port.purpose == "Motor Command"
    assert port.direction == "output"
    assert port.connector_id == "J4"
    assert port.pin_id == "PA7"

    assert visual_port.label == (
        "Motor Command"
    )

    assert visual_port.direction == (
        "output"
    )


def test_store_undo_restores_port_edit() -> None:
    store = make_store()

    store.commit(
        UpdateSemanticPort(
            port_id="port-1",
            purpose="Motor Command",
            direction="output",
        )
    )

    assert store.undo()

    port = (
        store.semantic_model.ports[
            "port-1"
        ]
    )

    visual_port = (
        store.model.nodes[
            "node-1"
        ].ports["port-1"]
    )

    assert port.purpose == "Signal"
    assert port.direction == "input"

    assert visual_port.label == "Signal"
    assert visual_port.direction == "input"


def test_store_redo_restores_port_edit() -> None:
    store = make_store()

    store.commit(
        UpdateSemanticPort(
            port_id="port-1",
            purpose="Motor Command",
            direction="output",
        )
    )

    assert store.undo()
    assert store.redo()

    port = (
        store.semantic_model.ports[
            "port-1"
        ]
    )

    assert port.purpose == (
        "Motor Command"
    )

    assert port.direction == "output"


def test_port_edit_marks_document_modified() -> None:
    store = make_store()

    assert not store.is_modified

    store.commit(
        UpdateSemanticPort(
            port_id="port-1",
            purpose="Motor Command",
        )
    )

    assert store.is_modified