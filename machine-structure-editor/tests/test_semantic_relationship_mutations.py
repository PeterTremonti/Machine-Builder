"""Tests for semantic relationship mutations."""

import pytest

from machine_builder.editor_state import EditorState
from machine_builder.semantic_capability import Capability
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Function,
    Machine,
    MachineComponent,
)
from machine_builder.semantic_relationship import (
    SemanticRelationship,
)
from machine_builder.semantic_relationship_mutations import (
    CreateSemanticRelationship,
    DeleteSemanticRelationship,
)
from machine_builder.store import ModelStore
from machine_builder.visual_model import VisualModel


def build_state() -> EditorState:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    model.add_component(
        "machine-1",
        MachineComponent(
            id="component-1",
            role="Heater",
        ),
    )

    model.add_function(
        "machine-1",
        Function(
            id="function-1",
            name="Control Temperature",
        ),
    )

    model.add_capability(
        "machine-1",
        Capability(
            id="capability-1",
            name="Temperature Control",
        ),
    )

    return EditorState(
        visual_model=VisualModel(),
        semantic_model=model,
    )


def build_store() -> ModelStore:
    store = ModelStore()

    store.semantic_model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    store.semantic_model.add_component(
        "machine-1",
        MachineComponent(
            id="component-1",
            role="Heater",
        ),
    )

    store.semantic_model.add_function(
        "machine-1",
        Function(
            id="function-1",
            name="Control Temperature",
        ),
    )

    store.semantic_model.add_capability(
        "machine-1",
        Capability(
            id="capability-1",
            name="Temperature Control",
        ),
    )

    return store


def test_create_relationship_mutation_adds_relationship() -> None:
    state = build_state()

    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="component-1",
        target_id="function-1",
        relationship_type="realizes",
    )

    CreateSemanticRelationship(
        relationship
    ).apply(
        state
    )

    assert (
        state.semantic_model.relationships[
            "relationship-1"
        ]
        is relationship
    )


def test_create_relationship_can_connect_function_and_capability() -> None:
    state = build_state()

    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="function-1",
        target_id="capability-1",
        relationship_type="realizes",
    )

    CreateSemanticRelationship(
        relationship
    ).apply(
        state
    )

    assert (
        state.semantic_model.get_relationship(
            "relationship-1"
        ).source_id
        == "function-1"
    )

    assert (
        state.semantic_model.get_relationship(
            "relationship-1"
        ).target_id
        == "capability-1"
    )


def test_create_relationship_rejects_unknown_source() -> None:
    state = build_state()

    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="missing-object",
        target_id="function-1",
        relationship_type="supports",
    )

    with pytest.raises(
        ValueError,
        match="Unknown relationship source",
    ):
        CreateSemanticRelationship(
            relationship
        ).apply(
            state
        )


def test_create_relationship_rejects_unknown_target() -> None:
    state = build_state()

    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="component-1",
        target_id="missing-object",
        relationship_type="supports",
    )

    with pytest.raises(
        ValueError,
        match="Unknown relationship target",
    ):
        CreateSemanticRelationship(
            relationship
        ).apply(
            state
        )


def test_create_relationship_rejects_duplicate_relationship() -> None:
    state = build_state()

    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="component-1",
        target_id="function-1",
        relationship_type="realizes",
    )

    CreateSemanticRelationship(
        relationship
    ).apply(
        state
    )

    with pytest.raises(
        ValueError,
        match="Relationship already exists",
    ):
        CreateSemanticRelationship(
            SemanticRelationship(
                id="relationship-1",
                source_id="component-1",
                target_id="function-1",
                relationship_type="realizes",
            )
        ).apply(
            state
        )


def test_delete_relationship_mutation_removes_relationship() -> None:
    state = build_state()

    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="component-1",
        target_id="function-1",
        relationship_type="realizes",
    )

    CreateSemanticRelationship(
        relationship
    ).apply(
        state
    )

    DeleteSemanticRelationship(
        "relationship-1"
    ).apply(
        state
    )

    assert (
        "relationship-1"
        not in state.semantic_model.relationships
    )


def test_delete_relationship_rejects_unknown_relationship() -> None:
    state = build_state()

    with pytest.raises(
        KeyError,
        match="Unknown relationship",
    ):
        DeleteSemanticRelationship(
            "missing-relationship"
        ).apply(
            state
        )


def test_relationship_mutations_do_not_modify_visual_model() -> None:
    state = build_state()

    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="component-1",
        target_id="capability-1",
        relationship_type="supports",
    )

    CreateSemanticRelationship(
        relationship
    ).apply(
        state
    )

    assert state.visual_model.nodes == {}
    assert state.visual_model.connections == {}


def test_create_relationship_can_be_committed() -> None:
    store = build_store()

    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="component-1",
        target_id="function-1",
        relationship_type="realizes",
    )

    store.commit(
        CreateSemanticRelationship(
            relationship
        )
    )

    assert (
        store.semantic_model.relationships[
            "relationship-1"
        ]
        is relationship
    )


def test_create_relationship_can_be_undone() -> None:
    store = build_store()

    store.commit(
        CreateSemanticRelationship(
            SemanticRelationship(
                id="relationship-1",
                source_id="component-1",
                target_id="function-1",
                relationship_type="realizes",
            )
        )
    )

    assert (
        "relationship-1"
        in store.semantic_model.relationships
    )

    assert store.undo()

    assert (
        "relationship-1"
        not in store.semantic_model.relationships
    )


def test_create_relationship_can_be_redone() -> None:
    store = build_store()

    store.commit(
        CreateSemanticRelationship(
            SemanticRelationship(
                id="relationship-1",
                source_id="component-1",
                target_id="function-1",
                relationship_type="realizes",
            )
        )
    )

    assert store.undo()
    assert store.redo()

    assert (
        "relationship-1"
        in store.semantic_model.relationships
    )


def test_delete_relationship_can_be_committed_and_undone() -> None:
    store = build_store()

    store.commit(
        CreateSemanticRelationship(
            SemanticRelationship(
                id="relationship-1",
                source_id="function-1",
                target_id="capability-1",
                relationship_type="realizes",
            )
        )
    )

    store.commit(
        DeleteSemanticRelationship(
            "relationship-1"
        )
    )

    assert (
        "relationship-1"
        not in store.semantic_model.relationships
    )

    assert store.undo()

    assert (
        "relationship-1"
        in store.semantic_model.relationships
    )


def test_delete_relationship_can_be_redone() -> None:
    store = build_store()

    store.commit(
        CreateSemanticRelationship(
            SemanticRelationship(
                id="relationship-1",
                source_id="function-1",
                target_id="capability-1",
                relationship_type="realizes",
            )
        )
    )

    store.commit(
        DeleteSemanticRelationship(
            "relationship-1"
        )
    )

    assert store.undo()
    assert store.redo()

    assert (
        "relationship-1"
        not in store.semantic_model.relationships
    )


def test_failed_relationship_commit_does_not_create_history_entry() -> None:
    store = build_store()

    first = SemanticRelationship(
        id="relationship-1",
        source_id="component-1",
        target_id="function-1",
        relationship_type="realizes",
    )

    store.commit(
        CreateSemanticRelationship(
            first
        )
    )

    with pytest.raises(
        ValueError,
        match="Relationship already exists",
    ):
        store.commit(
            CreateSemanticRelationship(
                SemanticRelationship(
                    id="relationship-1",
                    source_id="component-1",
                    target_id="function-1",
                    relationship_type="realizes",
                )
            )
        )

    assert (
        "relationship-1"
        in store.semantic_model.relationships
    )

    assert store.undo()

    assert (
        "relationship-1"
        not in store.semantic_model.relationships
    )

    assert not store.can_undo