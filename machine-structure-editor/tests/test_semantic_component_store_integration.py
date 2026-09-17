"""Integration tests for semantic component editing through ModelStore."""

from machine_builder.editor_state import (
    EditorState,
)
from machine_builder.semantic_component_mutations import (
    SetMachineComponentProperty,
    UpdateMachineComponent,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
)
from machine_builder.store import ModelStore
from machine_builder.visual_model import (
    VisualModel,
    VisualNode,
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
            label="Original Motor",
        ),
    )

    visual_model = VisualModel()

    visual_model.add_node(
        VisualNode(
            id="node-1",
            node_type="motor",
            label="Original Motor",
            semantic_reference="component-1",
        )
    )

    return ModelStore(
        model=visual_model,
        semantic_model=semantic_model,
    )


def test_store_commits_semantic_component_edit() -> None:
    store = make_store()

    store.commit(
        UpdateMachineComponent(
            component_id="component-1",
            label="X Axis Motor",
            role="drive motor",
        )
    )

    component = (
        store.semantic_model.components[
            "component-1"
        ]
    )

    assert component.label == "X Axis Motor"
    assert component.role == "drive motor"

    assert (
        store.model.nodes[
            "node-1"
        ].label
        == "X Axis Motor"
    )


def test_store_undo_restores_component_edit() -> None:
    store = make_store()

    store.commit(
        UpdateMachineComponent(
            component_id="component-1",
            label="X Axis Motor",
        )
    )

    assert (
        store.semantic_model.components[
            "component-1"
        ].label
        == "X Axis Motor"
    )

    assert store.undo()

    assert (
        store.semantic_model.components[
            "component-1"
        ].label
        == "Original Motor"
    )

    assert (
        store.model.nodes[
            "node-1"
        ].label
        == "Original Motor"
    )


def test_store_redo_restores_component_edit() -> None:
    store = make_store()

    store.commit(
        UpdateMachineComponent(
            component_id="component-1",
            label="X Axis Motor",
        )
    )

    assert store.undo()
    assert store.redo()

    assert (
        store.semantic_model.components[
            "component-1"
        ].label
        == "X Axis Motor"
    )

    assert (
        store.model.nodes[
            "node-1"
        ].label
        == "X Axis Motor"
    )


def test_store_can_edit_component_property() -> None:
    store = make_store()

    store.commit(
        SetMachineComponentProperty(
            component_id="component-1",
            property_name="axis",
            value="X",
        )
    )

    assert (
        store.semantic_model.components[
            "component-1"
        ].properties["axis"]
        == "X"
    )

    assert store.undo()

    assert (
        "axis"
        not in store.semantic_model.components[
            "component-1"
        ].properties
    )


def test_semantic_edit_marks_document_modified() -> None:
    store = make_store()

    assert not store.is_modified

    store.commit(
        UpdateMachineComponent(
            component_id="component-1",
            label="Edited Motor",
        )
    )

    assert store.is_modified