"""Tests for semantic relationships involving real hardware components."""

from machine_builder.hardware_component_fixtures import (
    add_generic_120vac_400w_heater,
)
from machine_builder.mutations import CreateNode
from machine_builder.semantic_capability import Capability
from machine_builder.semantic_model import Function
from machine_builder.semantic_relationship import (
    SemanticRelationship,
)
from machine_builder.semantic_relationship_queries import (
    relationships_from,
    relationships_to,
)
from machine_builder.store import ModelStore
from machine_builder.visual_model import (
    VisualNode,
    VisualPort,
)


def build_fan_node() -> VisualNode:
    node = VisualNode(
        id="fan-1",
        node_type="part_cooling_fan",
        label="Part Cooling Fan",
    )

    node.ports[
        "fan-1-power"
    ] = VisualPort(
        id="fan-1-power",
        node_id=node.id,
        label="Power",
        port_type="power",
        direction="input",
        side="left",
        order=0,
    )

    node.ports[
        "fan-1-ground"
    ] = VisualPort(
        id="fan-1-ground",
        node_id=node.id,
        label="Ground",
        port_type="electrical",
        direction="input",
        side="left",
        order=1,
    )

    return node


def build_heater_node() -> VisualNode:
    node = VisualNode(
        id="heater-1",
        node_type="chamber_heater",
        label="Chamber Heater",
    )

    node.ports[
        "heater-1-terminal-a"
    ] = VisualPort(
        id="heater-1-terminal-a",
        node_id=node.id,
        label="Power",
        port_type="power",
        direction="input",
        side="left",
        order=0,
    )

    node.ports[
        "heater-1-terminal-b"
    ] = VisualPort(
        id="heater-1-terminal-b",
        node_id=node.id,
        label="Power",
        port_type="power",
        direction="input",
        side="left",
        order=1,
    )

    return node


def build_real_component_model() -> ModelStore:
    store = ModelStore()

    store.commit(
        CreateNode(
            build_fan_node()
        )
    )

    store.commit(
        CreateNode(
            build_heater_node()
        )
    )

    store.semantic_model.add_function(
        "machine-1",
        Function(
            id="function-cooling",
            name="Cool Material",
        ),
    )

    store.semantic_model.add_function(
        "machine-1",
        Function(
            id="function-temperature",
            name="Control Chamber Temperature",
        ),
    )

    store.semantic_model.add_capability(
        "machine-1",
        Capability(
            id="capability-cooling",
            name="Material Cooling",
        ),
    )

    store.semantic_model.add_capability(
        "machine-1",
        Capability(
            id="capability-temperature",
            name="Chamber Temperature Control",
        ),
    )

    return store


def test_fan_can_participate_in_cooling_function() -> None:
    store = build_real_component_model()

    relationship = SemanticRelationship(
        id="relationship-fan-cooling",
        source_id="component-fan-1",
        target_id="function-cooling",
        relationship_type="participates_in",
    )

    store.semantic_model.add_relationship(
        relationship
    )

    results = relationships_from(
        store.semantic_model,
        "component-fan-1",
    )

    assert results == [
        relationship
    ]


def test_heater_can_realize_temperature_function() -> None:
    store = build_real_component_model()

    relationship = SemanticRelationship(
        id="relationship-heater-temperature",
        source_id="component-heater-1",
        target_id="function-temperature",
        relationship_type="realizes",
    )

    store.semantic_model.add_relationship(
        relationship
    )

    results = relationships_from(
        store.semantic_model,
        "component-heater-1",
    )

    assert results == [
        relationship
    ]


def test_fan_can_support_cooling_capability() -> None:
    store = build_real_component_model()

    relationship = SemanticRelationship(
        id="relationship-fan-capability",
        source_id="component-fan-1",
        target_id="capability-cooling",
        relationship_type="supports",
    )

    store.semantic_model.add_relationship(
        relationship
    )

    results = relationships_to(
        store.semantic_model,
        "capability-cooling",
    )

    assert results == [
        relationship
    ]


def test_heater_can_support_temperature_capability() -> None:
    store = build_real_component_model()

    relationship = SemanticRelationship(
        id="relationship-heater-capability",
        source_id="component-heater-1",
        target_id="capability-temperature",
        relationship_type="supports",
    )

    store.semantic_model.add_relationship(
        relationship
    )

    results = relationships_to(
        store.semantic_model,
        "capability-temperature",
    )

    assert results == [
        relationship
    ]


def test_function_can_realize_capability() -> None:
    store = build_real_component_model()

    relationship = SemanticRelationship(
        id="relationship-function-capability",
        source_id="function-temperature",
        target_id="capability-temperature",
        relationship_type="realizes",
    )

    store.semantic_model.add_relationship(
        relationship
    )

    results = relationships_to(
        store.semantic_model,
        "capability-temperature",
    )

    assert results == [
        relationship
    ]


def test_real_components_can_have_multiple_relationships() -> None:
    store = build_real_component_model()

    fan_function_relationship = SemanticRelationship(
        id="relationship-fan-function",
        source_id="component-fan-1",
        target_id="function-cooling",
        relationship_type="participates_in",
    )

    fan_capability_relationship = SemanticRelationship(
        id="relationship-fan-capability",
        source_id="component-fan-1",
        target_id="capability-cooling",
        relationship_type="supports",
    )

    store.semantic_model.add_relationship(
        fan_function_relationship
    )

    store.semantic_model.add_relationship(
        fan_capability_relationship
    )

    results = relationships_from(
        store.semantic_model,
        "component-fan-1",
    )

    assert {
        relationship.id
        for relationship in results
    } == {
        "relationship-fan-function",
        "relationship-fan-capability",
    }


def test_real_component_relationships_are_independent_of_hardware_definition() -> None:
    store = build_real_component_model()

    relationship = SemanticRelationship(
        id="relationship-heater-temperature",
        source_id="component-heater-1",
        target_id="function-temperature",
        relationship_type="realizes",
    )

    store.semantic_model.add_relationship(
        relationship
    )

    heater = store.semantic_model.components[
        "component-heater-1"
    ]

    assert (
        heater.hardware_definition_id
        == "generic-120vac-400w-heater"
    )

    assert (
        store.semantic_model.get_relationship(
            "relationship-heater-temperature"
        )
        is relationship
    )


def test_real_heater_fixture_can_be_added_to_same_model() -> None:
    store = build_real_component_model()

    component = add_generic_120vac_400w_heater(
        store.semantic_model,
        "machine-1",
        component_id="fixture-heater-2",
    )

    assert component.id == "fixture-heater-2"

    assert (
        component.hardware_definition_id
        == "generic-120vac-400w-heater"
    )

    assert len(
        component.port_ids
    ) == 2