"""Tests for canonical semantic relationship queries."""

from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Function,
    Machine,
    MachineComponent,
)
from machine_builder.semantic_relationship import (
    SemanticRelationship,
)
from machine_builder.semantic_relationship_queries import (
    relationships_between,
    relationships_from,
    relationships_of_type,
    relationships_to,
)


def build_model() -> CanonicalMachineModel:
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
            id="component-heater",
            role="Heater",
        ),
    )

    model.add_component(
        "machine-1",
        MachineComponent(
            id="component-fan",
            role="Fan",
        ),
    )

    model.add_function(
        "machine-1",
        Function(
            id="function-temperature",
            name="Control Temperature",
        ),
    )

    model.add_function(
        "machine-1",
        Function(
            id="function-cooling",
            name="Cool Material",
        ),
    )

    model.add_relationship(
        SemanticRelationship(
            id="relationship-1",
            source_id="component-heater",
            target_id="function-temperature",
            relationship_type="realizes",
        )
    )

    model.add_relationship(
        SemanticRelationship(
            id="relationship-2",
            source_id="component-fan",
            target_id="function-cooling",
            relationship_type="realizes",
        )
    )

    model.add_relationship(
        SemanticRelationship(
            id="relationship-3",
            source_id="component-fan",
            target_id="function-temperature",
            relationship_type="supports",
        )
    )

    return model


def test_relationships_from_returns_matching_relationships() -> None:
    model = build_model()

    relationships = relationships_from(
        model,
        "component-fan",
    )

    assert {
        relationship.id
        for relationship in relationships
    } == {
        "relationship-2",
        "relationship-3",
    }


def test_relationships_to_returns_matching_relationships() -> None:
    model = build_model()

    relationships = relationships_to(
        model,
        "function-temperature",
    )

    assert {
        relationship.id
        for relationship in relationships
    } == {
        "relationship-1",
        "relationship-3",
    }


def test_relationships_of_type_returns_matching_relationships() -> None:
    model = build_model()

    relationships = relationships_of_type(
        model,
        "realizes",
    )

    assert {
        relationship.id
        for relationship in relationships
    } == {
        "relationship-1",
        "relationship-2",
    }


def test_relationships_between_returns_ordered_match() -> None:
    model = build_model()

    relationships = relationships_between(
        model,
        "component-fan",
        "function-temperature",
    )

    assert [
        relationship.id
        for relationship in relationships
    ] == [
        "relationship-3"
    ]


def test_relationships_between_does_not_reverse_match() -> None:
    model = build_model()

    relationships = relationships_between(
        model,
        "function-temperature",
        "component-fan",
    )

    assert relationships == []


def test_relationship_queries_return_empty_list_when_no_match() -> None:
    model = build_model()

    assert (
        relationships_from(
            model,
            "missing-object",
        )
        == []
    )

    assert (
        relationships_to(
            model,
            "missing-object",
        )
        == []
    )

    assert (
        relationships_of_type(
            model,
            "requires",
        )
        == []
    )

    assert (
        relationships_between(
            model,
            "component-heater",
            "function-cooling",
        )
        == []
    )


def test_relationship_queries_preserve_relationship_objects() -> None:
    model = build_model()

    relationships = relationships_from(
        model,
        "component-heater",
    )

    assert len(relationships) == 1

    relationship = relationships[0]

    assert (
        model.relationships[
            relationship.id
        ]
        is relationship
    )


def test_relationship_queries_do_not_modify_model() -> None:
    model = build_model()

    before = dict(
        model.relationships
    )

    relationships_from(
        model,
        "component-fan",
    )
    relationships_to(
        model,
        "function-temperature",
    )
    relationships_of_type(
        model,
        "realizes",
    )
    relationships_between(
        model,
        "component-fan",
        "function-temperature",
    )

    assert model.relationships == before