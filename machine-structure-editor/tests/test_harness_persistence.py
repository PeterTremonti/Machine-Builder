import pytest

from machine_builder.editor_state import EditorState
from machine_builder.persistence import (
    FORMAT_VERSION,
    deserialize_editor_state,
    serialize_editor_state,
)
from machine_builder.semantic_connection import SemanticConnection
from machine_builder.semantic_harness import Harness
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
    Provenance,
    SemanticPort,
)
from machine_builder.visual_model import VisualModel


def build_state() -> EditorState:
    model = CanonicalMachineModel()
    model.add_machine(Machine(id="machine-1", name="Test machine"))

    for suffix in ("a", "b", "c"):
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
            properties={
                "wire_color": "blue",
                "harness_id": "legacy textual label",
                "notes": "existing wire metadata",
            },
            provenance=[Provenance(source="original wiring record")],
        )
    )
    model.add_connection(
        SemanticConnection(
            id="wire-bc",
            endpoint_a_id="port-b",
            endpoint_b_id="port-c",
            properties={"wire_color": "white"},
        )
    )

    return EditorState(
        visual_model=VisualModel(),
        semantic_model=model,
    )


def build_nested_harness_state() -> EditorState:
    state = build_state()
    model = state.semantic_model

    model.add_harness(
        Harness(
            id="harness-branch",
            name="J9 branch",
            member_connection_ids=["wire-bc"],
            properties={"color": "white"},
            provenance=[Provenance(source="assembly drawing")],
        )
    )
    model.add_harness(
        Harness(
            id="harness-main",
            name="J9 loom",
            member_connection_ids=["wire-ab"],
            child_harness_ids=["harness-branch"],
            properties={"label": "J9"},
            provenance=[Provenance(source="wiring inspection")],
        )
    )
    return state


def test_nested_harnesses_and_connections_round_trip():
    original = build_nested_harness_state()

    document = serialize_editor_state(original)
    restored = deserialize_editor_state(document)
    model = restored.semantic_model

    assert model.harnesses["harness-main"].name == "J9 loom"
    assert model.harnesses["harness-main"].member_connection_ids == [
        "wire-ab"
    ]
    assert model.harnesses["harness-main"].child_harness_ids == [
        "harness-branch"
    ]
    assert model.harnesses["harness-main"].properties == {"label": "J9"}
    assert model.harnesses["harness-main"].provenance == [
        Provenance(source="wiring inspection")
    ]

    assert model.harnesses["harness-branch"].member_connection_ids == [
        "wire-bc"
    ]
    assert model.harnesses["harness-branch"].properties == {"color": "white"}
    assert model.harnesses["harness-branch"].provenance == [
        Provenance(source="assembly drawing")
    ]

    assert model.get_harness_connection_ids("harness-main") == [
        "wire-ab",
        "wire-bc",
    ]
    assert model.get_harness_conductor_count("harness-main") == 2
    model.validate_harnesses()


def test_round_trip_preserves_legacy_harness_id_and_wire_semantics():
    original = build_nested_harness_state()
    original_connection = original.semantic_model.connections["wire-ab"]

    restored = deserialize_editor_state(serialize_editor_state(original))
    connection = restored.semantic_model.connections["wire-ab"]

    assert connection.id == original_connection.id
    assert connection.endpoint_a_id == "port-a"
    assert connection.endpoint_b_id == "port-b"
    assert connection.connection_type == original_connection.connection_type
    assert connection.properties == {
        "wire_color": "blue",
        "harness_id": "legacy textual label",
        "notes": "existing wire metadata",
    }
    assert connection.provenance == [
        Provenance(source="original wiring record")
    ]
    assert "legacy textual label" != "harness-main"


def test_version_one_document_without_harnesses_field_loads_with_empty_default():
    state = build_state()
    document = serialize_editor_state(state)

    assert document["format_version"] == FORMAT_VERSION == 1

    semantic_model_fields = (
        document["state"]["fields"]["semantic_model"]["fields"]
    )
    semantic_model_fields.pop("harnesses")

    restored = deserialize_editor_state(document)

    assert restored.semantic_model.harnesses == {}
    assert set(restored.semantic_model.connections) == {"wire-ab", "wire-bc"}
    assert (
        restored.semantic_model.connections["wire-ab"].properties["harness_id"]
        == "legacy textual label"
    )


def test_persistence_rejects_dangling_direct_connection_membership():
    state = build_state()
    state.semantic_model.harnesses["bad-harness"] = Harness(
        id="bad-harness",
        name="Invalid harness",
        member_connection_ids=["missing-wire"],
    )

    document = serialize_editor_state(state)

    with pytest.raises(
        ValueError,
        match="Invalid persisted harness membership.*unknown connection",
    ):
        deserialize_editor_state(document)


def test_persistence_rejects_dangling_child_harness_reference():
    state = build_state()
    state.semantic_model.harnesses["bad-harness"] = Harness(
        id="bad-harness",
        name="Invalid harness",
        child_harness_ids=["missing-child"],
    )

    document = serialize_editor_state(state)

    with pytest.raises(
        ValueError,
        match="Invalid persisted harness membership.*unknown child harness",
    ):
        deserialize_editor_state(document)
