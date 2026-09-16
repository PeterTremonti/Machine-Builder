"""Tests for complete editor state and store behavior."""

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
from machine_builder.mutations import (
    CreateMachineComponent,
    CreateNode,
    DeleteNodes,
)


def test_store_contains_visual_and_semantic_models() -> None:
    store = ModelStore()

    assert isinstance(
        store.model,
        VisualModel,
    )

    assert isinstance(
        store.semantic_model,
        CanonicalMachineModel,
    )

    assert store.state.visual_model is store.model
    assert (
        store.state.semantic_model
        is store.semantic_model
    )


def test_visual_creation_now_creates_semantic_component() -> None:
    store = ModelStore()

    node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Part Cooling Fan",
    )

    store.commit(
        CreateNode(
            node
        )
    )

    assert "node-1" in store.model.nodes

    assert (
        node.semantic_reference
        == "component-node-1"
    )

    component = (
        store.semantic_model.components[
            "component-node-1"
        ]
    )

    assert component.role == "Part Cooling Fan"
    assert component.label == "Part Cooling Fan"

    assert (
        component.properties[
            "visual_node_type"
        ]
        == "fan"
    )

    assert (
        store.semantic_model.machines[
            "machine-1"
        ].name
        == "Untitled Machine"
    )

    assert (
        store.semantic_model.machines[
            "machine-1"
        ].component_ids
        == ["component-node-1"]
    )


def test_visual_creation_uses_existing_machine() -> None:
    store = ModelStore()

    machine = Machine(
        id="machine-1",
        name="Promega",
    )

    store.semantic_model.add_machine(
        machine
    )

    node = VisualNode(
        id="node-1",
        node_type="motor",
        label="X Motor",
    )

    store.commit(
        CreateNode(
            node
        )
    )

    assert (
        store.semantic_model.machines[
            "machine-1"
        ].name
        == "Promega"
    )

    assert (
        machine.component_ids
        == ["component-node-1"]
    )


def test_visual_mutation_still_works() -> None:
    store = ModelStore()

    node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Fan",
    )

    store.commit(
        CreateNode(
            node
        )
    )

    assert (
        store.model.nodes["node-1"]
        is node
    )


def test_create_machine_component_creates_both_models() -> None:
    store = ModelStore()

    machine = Machine(
        id="machine-1",
        name="Test Machine",
    )

    store.semantic_model.add_machine(
        machine
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
        label="Part Cooling Fan",
    )

    node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Part Cooling Fan",
    )

    store.commit(
        CreateMachineComponent(
            machine_id=machine.id,
            component=component,
            node=node,
        )
    )

    assert (
        store.semantic_model.components[
            component.id
        ]
        is component
    )

    assert (
        store.model.nodes[
            node.id
        ]
        is node
    )

    assert (
        node.semantic_reference
        == component.id
    )


def test_create_machine_component_attaches_component_to_machine() -> None:
    store = ModelStore()

    machine = Machine(
        id="machine-1",
        name="Test Machine",
    )

    store.semantic_model.add_machine(
        machine
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
    )

    node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Fan",
    )

    store.commit(
        CreateMachineComponent(
            machine_id=machine.id,
            component=component,
            node=node,
        )
    )

    assert machine.component_ids == [
        component.id
    ]


def test_create_machine_component_undo_removes_both() -> None:
    store = ModelStore()

    machine = Machine(
        id="machine-1",
        name="Test Machine",
    )

    store.semantic_model.add_machine(
        machine
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
    )

    node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Fan",
    )

    store.commit(
        CreateMachineComponent(
            machine_id=machine.id,
            component=component,
            node=node,
        )
    )

    assert "component-1" in (
        store.semantic_model.components
    )

    assert "node-1" in (
        store.model.nodes
    )

    assert store.undo()

    assert "component-1" not in (
        store.semantic_model.components
    )

    assert "node-1" not in (
        store.model.nodes
    )


def test_create_machine_component_redo_restores_both() -> None:
    store = ModelStore()

    machine = Machine(
        id="machine-1",
        name="Test Machine",
    )

    store.semantic_model.add_machine(
        machine
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
    )

    node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Fan",
    )

    store.commit(
        CreateMachineComponent(
            machine_id=machine.id,
            component=component,
            node=node,
        )
    )

    assert store.undo()
    assert store.redo()

    assert (
        "component-1"
        in store.semantic_model.components
    )

    assert (
        "node-1"
        in store.model.nodes
    )

    assert (
        store.model.nodes[
            "node-1"
        ].semantic_reference
        == "component-1"
    )


def test_create_machine_component_rejects_conflicting_node_reference() -> None:
    store = ModelStore()

    machine = Machine(
        id="machine-1",
        name="Test Machine",
    )

    store.semantic_model.add_machine(
        machine
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
    )

    node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Fan",
        semantic_reference="another-component",
    )

    try:
        store.commit(
            CreateMachineComponent(
                machine_id=machine.id,
                component=component,
                node=node,
            )
        )
    except ValueError as exc:
        assert (
            "different canonical component"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected conflicting semantic reference "
            "to be rejected"
        )


def test_failed_machine_component_creation_rolls_back_everything() -> None:
    store = ModelStore()

    machine = Machine(
        id="machine-1",
        name="Test Machine",
    )

    store.semantic_model.add_machine(
        machine
    )

    existing_node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Existing",
    )

    store.model.add_node(
        existing_node
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
    )

    duplicate_node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Duplicate",
    )

    try:
        store.commit(
            CreateMachineComponent(
                machine_id=machine.id,
                component=component,
                node=duplicate_node,
            )
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Expected duplicate visual node "
            "to be rejected"
        )

    assert (
        "component-1"
        not in store.semantic_model.components
    )

    restored_machine = (
        store.semantic_model.machines[
            "machine-1"
        ]
    )

    assert (
        restored_machine.component_ids
        == []
    )

    restored_node = (
        store.model.nodes[
            "node-1"
        ]
    )

    assert restored_node.id == "node-1"
    assert restored_node.label == "Existing"
    assert restored_node.node_type == "fan"

    assert not store.can_undo
    assert not store.can_redo


def test_failed_mutation_leaves_existing_undo_history_intact() -> None:
    store = ModelStore()

    first_node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Fan",
    )

    store.commit(
        CreateNode(
            first_node
        )
    )

    assert store.can_undo

    machine = Machine(
        id="machine-1",
        name="Test Machine",
    )

    # The first CreateNode already created machine-1, so this operation
    # intentionally replaces the existing object only in local test setup.
    store.semantic_model.machines[
        "machine-1"
    ] = machine

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
    )

    duplicate_node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Duplicate",
    )

    try:
        store.commit(
            CreateMachineComponent(
                machine_id=machine.id,
                component=component,
                node=duplicate_node,
            )
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Expected duplicate visual node "
            "to be rejected"
        )

    assert store.can_undo

    assert store.undo()

    assert (
        "node-1"
        not in store.model.nodes
    )


def test_delete_nodes_removes_canonical_components() -> None:
    store = ModelStore()

    node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Part Cooling Fan",
    )

    store.commit(
        CreateNode(
            node
        )
    )

    assert (
        "component-node-1"
        in store.semantic_model.components
    )

    store.commit(
        DeleteNodes(
            node_ids=("node-1",)
        )
    )

    assert (
        "node-1"
        not in store.model.nodes
    )

    assert (
        "component-node-1"
        not in store.semantic_model.components
    )

    assert (
        store.semantic_model.machines[
            "machine-1"
        ].component_ids
        == []
    )


def test_delete_nodes_undo_restores_both_models() -> None:
    store = ModelStore()

    node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Part Cooling Fan",
    )

    store.commit(
        CreateNode(
            node
        )
    )

    store.commit(
        DeleteNodes(
            node_ids=("node-1",)
        )
    )

    assert store.undo()

    assert (
        "node-1"
        in store.model.nodes
    )

    assert (
        "component-node-1"
        in store.semantic_model.components
    )

    assert (
        store.model.nodes[
            "node-1"
        ].semantic_reference
        == "component-node-1"
    )