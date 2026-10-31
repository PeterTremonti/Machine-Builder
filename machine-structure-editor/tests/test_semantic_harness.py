import pytest

from machine_builder.semantic_harness import Harness


def test_harness_defaults_to_empty_members_and_metadata():
    harness = Harness(id="harness-main", name="Main harness")

    assert harness.id == "harness-main"
    assert harness.name == "Main harness"
    assert harness.member_connection_ids == []
    assert harness.child_harness_ids == []
    assert harness.properties == {}
    assert harness.provenance == []


def test_harness_preserves_supplied_members_metadata_and_provenance():
    from machine_builder.semantic_model import Provenance

    provenance = [Provenance(source="assembly drawing")]
    properties = {"label": "J9 loom", "color": "black"}
    harness = Harness(
        id="harness-j9",
        name="J9 loom",
        member_connection_ids=["wire-x", "wire-y"],
        child_harness_ids=["harness-branch"],
        properties=properties,
        provenance=provenance,
    )

    assert harness.member_connection_ids == ["wire-x", "wire-y"]
    assert harness.child_harness_ids == ["harness-branch"]
    assert harness.properties == properties
    assert harness.provenance == provenance


@pytest.mark.parametrize("identifier", ["", " ", None, 7])
def test_harness_rejects_invalid_id(identifier):
    with pytest.raises(ValueError, match="ID"):
        Harness(id=identifier, name="Harness")


@pytest.mark.parametrize("name", ["", " ", None, 7])
def test_harness_rejects_invalid_name(name):
    with pytest.raises(ValueError, match="name"):
        Harness(id="harness-1", name=name)


@pytest.mark.parametrize(
    ("field_name", "kwargs"),
    [
        (
            "member_connection_ids",
            {"member_connection_ids": ["wire-1", "wire-1"]},
        ),
        (
            "child_harness_ids",
            {"child_harness_ids": ["child-1", "child-1"]},
        ),
    ],
)
def test_harness_rejects_repeated_local_membership(field_name, kwargs):
    with pytest.raises(ValueError, match="repeated"):
        Harness(id="harness-1", name="Harness", **kwargs)


@pytest.mark.parametrize(
    ("field_name", "kwargs"),
    [
        (
            "member_connection_ids",
            {"member_connection_ids": "wire-1"},
        ),
        (
            "child_harness_ids",
            {"child_harness_ids": ("child-1",)},
        ),
    ],
)
def test_harness_requires_membership_collections_to_be_lists(
    field_name, kwargs
):
    with pytest.raises(ValueError, match="must be a list"):
        Harness(id="harness-1", name="Harness", **kwargs)


@pytest.mark.parametrize(
    ("field_name", "kwargs"),
    [
        (
            "member_connection_ids",
            {"member_connection_ids": ["wire-1", " "]},
        ),
        (
            "child_harness_ids",
            {"child_harness_ids": ["child-1", None]},
        ),
    ],
)
def test_harness_rejects_empty_or_non_string_member_ids(
    field_name, kwargs
):
    with pytest.raises(ValueError, match="non-empty strings"):
        Harness(id="harness-1", name="Harness", **kwargs)


def _model_with_three_connections():
    from machine_builder.semantic_connection import SemanticConnection
    from machine_builder.semantic_model import (
        CanonicalMachineModel,
        Machine,
        MachineComponent,
        SemanticPort,
    )

    model = CanonicalMachineModel()
    model.add_machine(Machine(id="machine-1", name="Test machine"))

    for letter in ("a", "b", "c"):
        component_id = f"component-{letter}"
        model.add_component(
            "machine-1",
            MachineComponent(id=component_id, role=f"Test part {letter}"),
        )
        model.add_port(
            SemanticPort(
                id=f"port-{letter}",
                component_id=component_id,
                purpose="test",
            )
        )

    connections = (
        SemanticConnection(
            id="wire-ab",
            endpoint_a_id="port-a",
            endpoint_b_id="port-b",
            properties={"harness_id": "legacy free text"},
        ),
        SemanticConnection(
            id="wire-ac",
            endpoint_a_id="port-a",
            endpoint_b_id="port-c",
            properties={"wire_color": "blue"},
        ),
        SemanticConnection(
            id="wire-bc",
            endpoint_a_id="port-b",
            endpoint_b_id="port-c",
            properties={"wire_color": "white"},
        ),
    )
    for connection in connections:
        model.add_connection(connection)

    return model


def test_nested_harness_counts_leaf_connections_and_preserves_legacy_data():
    model = _model_with_three_connections()

    child = Harness(
        id="harness-child",
        name="Child",
        member_connection_ids=["wire-bc"],
    )
    model.add_harness(child)

    parent = Harness(
        id="harness-root",
        name="Root",
        member_connection_ids=["wire-ab"],
        child_harness_ids=["harness-child"],
    )
    model.add_harness(parent)

    assert model.get_harness_connection_ids("harness-root") == [
        "wire-ab",
        "wire-bc",
    ]
    assert model.get_harness_conductor_count("harness-root") == 2
    assert model.connections["wire-ab"].endpoint_a_id == "port-a"
    assert model.connections["wire-ab"].endpoint_b_id == "port-b"
    assert (
        model.connections["wire-ab"].properties["harness_id"]
        == "legacy free text"
    )
    assert model.harnesses["harness-root"].child_harness_ids == [
        "harness-child"
    ]
    model.validate_harnesses()


def test_harness_rejects_unknown_direct_connection_without_partial_add():
    model = _model_with_three_connections()

    with pytest.raises(ValueError, match="unknown connection"):
        model.add_harness(
            Harness(
                id="bad-harness",
                name="Bad",
                member_connection_ids=["missing-wire"],
            )
        )

    assert "bad-harness" not in model.harnesses
    model.validate_harnesses()


def test_harness_rejects_unknown_child_without_partial_add():
    model = _model_with_three_connections()

    with pytest.raises(ValueError, match="unknown child harness"):
        model.add_harness(
            Harness(
                id="bad-parent",
                name="Bad parent",
                child_harness_ids=["missing-child"],
            )
        )

    assert "bad-parent" not in model.harnesses
    model.validate_harnesses()


def test_harness_rejects_connection_owned_directly_by_two_harnesses():
    model = _model_with_three_connections()
    model.add_harness(
        Harness(
            id="harness-one",
            name="One",
            member_connection_ids=["wire-ab"],
        )
    )

    with pytest.raises(ValueError, match="belongs directly"):
        model.add_harness(
            Harness(
                id="harness-two",
                name="Two",
                member_connection_ids=["wire-ab"],
            )
        )

    assert "harness-two" not in model.harnesses
    model.validate_harnesses()


def test_harness_rejects_child_with_two_parents():
    model = _model_with_three_connections()
    model.add_harness(Harness(id="child", name="Child"))
    model.add_harness(
        Harness(id="parent-one", name="Parent one", child_harness_ids=["child"])
    )

    with pytest.raises(ValueError, match="conflicting parents"):
        model.add_harness(
            Harness(id="parent-two", name="Parent two", child_harness_ids=["child"])
        )

    assert "parent-two" not in model.harnesses
    model.validate_harnesses()


def test_harness_rejects_nested_cycle_and_rolls_back_child_link():
    model = _model_with_three_connections()
    model.add_harness(Harness(id="harness-a", name="A"))
    model.add_harness(Harness(id="harness-b", name="B"))
    model.add_child_harness("harness-a", "harness-b")

    with pytest.raises(ValueError, match="cycle"):
        model.add_child_harness("harness-b", "harness-a")

    assert model.harnesses["harness-b"].child_harness_ids == []
    model.validate_harnesses()


def test_normal_connection_removal_cleans_only_that_harness_membership():
    model = _model_with_three_connections()
    model.add_harness(
        Harness(
            id="child",
            name="Child",
            member_connection_ids=["wire-bc"],
        )
    )
    model.add_harness(
        Harness(
            id="root",
            name="Root",
            member_connection_ids=["wire-ab"],
            child_harness_ids=["child"],
        )
    )

    removed = model.remove_connection("wire-ab")

    assert removed.id == "wire-ab"
    assert "wire-ab" not in model.connections
    assert model.harnesses["root"].member_connection_ids == []
    assert model.harnesses["root"].child_harness_ids == ["child"]
    assert model.harnesses["child"].member_connection_ids == ["wire-bc"]
    assert model.get_harness_connection_ids("root") == ["wire-bc"]
    model.validate_harnesses()


def test_component_removal_cleans_incident_members_and_preserves_hierarchy():
    model = _model_with_three_connections()

    model.add_harness(
        Harness(
            id="grandchild",
            name="Grandchild",
            member_connection_ids=["wire-bc"],
        )
    )
    model.add_harness(
        Harness(
            id="branch",
            name="Branch",
            member_connection_ids=["wire-ac"],
            child_harness_ids=["grandchild"],
        )
    )
    model.add_harness(
        Harness(
            id="root",
            name="Root",
            member_connection_ids=["wire-ab"],
            child_harness_ids=["branch"],
        )
    )

    removed = model.remove_component("component-a")

    assert removed.id == "component-a"
    assert set(model.connections) == {"wire-bc"}
    assert model.harnesses["root"].member_connection_ids == []
    assert model.harnesses["branch"].member_connection_ids == []
    assert model.harnesses["grandchild"].member_connection_ids == ["wire-bc"]
    assert model.harnesses["root"].child_harness_ids == ["branch"]
    assert model.harnesses["branch"].child_harness_ids == ["grandchild"]
    assert model.get_harness_connection_ids("root") == ["wire-bc"]
    assert model.get_harness_conductor_count("root") == 1
    model.validate_harnesses()
