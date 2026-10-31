import pytest

from machine_builder.editor_state import EditorState
from machine_builder.harness_mutations import (
    AddConnectionToHarness,
    AttachChildHarness,
    CreateHarness,
    DeleteHarness,
    DetachChildHarness,
    RemoveConnectionFromHarness,
    UpdateHarness,
)
from machine_builder.semantic_connection import SemanticConnection
from machine_builder.semantic_harness import Harness
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
    SemanticPort,
)
from machine_builder.store import ModelStore
from machine_builder.visual_model import VisualModel


def build_state() -> EditorState:
    model = CanonicalMachineModel()
    model.add_machine(Machine(id="machine-1", name="Test machine"))

    for suffix in ("a", "b"):
        component_id = f"component-{suffix}"
        model.add_component(
            "machine-1",
            MachineComponent(id=component_id, role=f"Part {suffix}"),
        )
        model.add_port(
            SemanticPort(
                id=f"port-{suffix}",
                component_id=component_id,
                purpose="test",
            )
        )

    model.add_connection(
        SemanticConnection(
            id="wire-ab",
            endpoint_a_id="port-a",
            endpoint_b_id="port-b",
            properties={"wire_color": "blue", "harness_id": "legacy text"},
        )
    )

    return EditorState(
        visual_model=VisualModel(),
        semantic_model=model,
    )


def test_create_and_update_harness_mutations():
    state = build_state()
    original = Harness(
        id="harness-1",
        name="Original",
        properties={"label": "J9"},
    )

    CreateHarness(original).apply(state)

    assert state.semantic_model.harnesses["harness-1"] == original
    assert state.semantic_model.harnesses["harness-1"] is not original

    UpdateHarness(
        harness_id="harness-1",
        name="Updated J9",
        properties={"label": "J9 loom", "color": "black"},
    ).apply(state)

    harness = state.semantic_model.harnesses["harness-1"]
    assert harness.name == "Updated J9"
    assert harness.properties == {"label": "J9 loom", "color": "black"}


def test_direct_membership_mutations_do_not_modify_connection():
    state = build_state()
    CreateHarness(Harness(id="harness-1", name="J9")).apply(state)

    AddConnectionToHarness("harness-1", "wire-ab").apply(state)

    assert state.semantic_model.harnesses[
        "harness-1"
    ].member_connection_ids == ["wire-ab"]
    connection = state.semantic_model.connections["wire-ab"]
    assert connection.endpoint_a_id == "port-a"
    assert connection.endpoint_b_id == "port-b"
    assert connection.properties == {
        "wire_color": "blue",
        "harness_id": "legacy text",
    }

    RemoveConnectionFromHarness("harness-1", "wire-ab").apply(state)

    assert state.semantic_model.harnesses[
        "harness-1"
    ].member_connection_ids == []
    assert "wire-ab" in state.semantic_model.connections
    state.semantic_model.validate_harnesses()


def test_attach_and_detach_child_harness_mutations():
    state = build_state()
    CreateHarness(Harness(id="parent", name="Parent")).apply(state)
    CreateHarness(
        Harness(
            id="child",
            name="Child",
            member_connection_ids=["wire-ab"],
        )
    ).apply(state)

    AttachChildHarness("parent", "child").apply(state)

    assert state.semantic_model.harnesses[
        "parent"
    ].child_harness_ids == ["child"]

    DetachChildHarness("parent", "child").apply(state)

    assert state.semantic_model.harnesses["parent"].child_harness_ids == []
    assert state.semantic_model.harnesses[
        "child"
    ].member_connection_ids == ["wire-ab"]
    state.semantic_model.validate_harnesses()


def test_delete_harness_requires_no_direct_members_or_children():
    state = build_state()
    CreateHarness(
        Harness(
            id="parent",
            name="Parent",
            child_harness_ids=["child"],
        )
    )
    # Create the child first because each creation validates references.
    CreateHarness(Harness(id="child", name="Child")).apply(state)
    CreateHarness(
        Harness(
            id="parent",
            name="Parent",
            child_harness_ids=["child"],
        )
    ).apply(state)

    with pytest.raises(ValueError, match="child harnesses"):
        DeleteHarness("parent").apply(state)

    with pytest.raises(ValueError, match="attached to a parent"):
        DeleteHarness("child").apply(state)

    DetachChildHarness("parent", "child").apply(state)
    DeleteHarness("child").apply(state)
    DeleteHarness("parent").apply(state)

    assert state.semantic_model.harnesses == {}


def test_delete_harness_with_direct_members_is_rejected():
    state = build_state()
    CreateHarness(
        Harness(
            id="harness-1",
            name="J9",
            member_connection_ids=["wire-ab"],
        )
    ).apply(state)

    with pytest.raises(ValueError, match="direct connection members"):
        DeleteHarness("harness-1").apply(state)

    assert "wire-ab" in state.semantic_model.connections
    assert state.semantic_model.harnesses[
        "harness-1"
    ].member_connection_ids == ["wire-ab"]


def test_store_undo_redo_restores_harness_and_membership():
    state = build_state()
    store = ModelStore(
        model=state.visual_model,
        semantic_model=state.semantic_model,
    )

    store.commit(
        CreateHarness(Harness(id="harness-1", name="J9"))
    )
    assert "harness-1" in store.semantic_model.harnesses

    assert store.undo()
    assert "harness-1" not in store.semantic_model.harnesses

    assert store.redo()
    assert "harness-1" in store.semantic_model.harnesses

    store.commit(
        AddConnectionToHarness("harness-1", "wire-ab")
    )
    assert store.semantic_model.harnesses[
        "harness-1"
    ].member_connection_ids == ["wire-ab"]

    assert store.undo()
    assert store.semantic_model.harnesses[
        "harness-1"
    ].member_connection_ids == []

    assert store.redo()
    assert store.semantic_model.harnesses[
        "harness-1"
    ].member_connection_ids == ["wire-ab"]
    store.semantic_model.validate_harnesses()


def test_failed_store_mutation_rolls_back_state():
    state = build_state()
    store = ModelStore(
        model=state.visual_model,
        semantic_model=state.semantic_model,
    )
    store.commit(
        CreateHarness(Harness(id="harness-1", name="J9"))
    )

    with pytest.raises(ValueError, match="Unknown child harness"):
        store.commit(
            AttachChildHarness("harness-1", "missing-child")
        )

    assert store.semantic_model.harnesses[
        "harness-1"
    ].child_harness_ids == []
    store.semantic_model.validate_harnesses()
