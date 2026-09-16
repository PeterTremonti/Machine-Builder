"""Tests for canonical semantic relationships."""

import pytest

from machine_builder.semantic_model import (
    Provenance,
)
from machine_builder.semantic_relationship import (
    RELATIONSHIP_TYPES,
    SemanticRelationship,
)


def test_relationship_can_be_created() -> None:
    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="component-fan-a",
        target_id="function-cooling",
        relationship_type="participates_in",
    )

    assert relationship.id == "relationship-1"
    assert relationship.source_id == "component-fan-a"
    assert relationship.target_id == "function-cooling"
    assert (
        relationship.relationship_type
        == "participates_in"
    )


def test_relationship_can_store_properties() -> None:
    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="component-fan-a",
        target_id="function-cooling",
        relationship_type="participates_in",
        properties={
            "confidence": "inferred",
            "notes": "Cooling airflow function.",
        },
    )

    assert (
        relationship.properties["confidence"]
        == "inferred"
    )

    assert (
        relationship.properties["notes"]
        == "Cooling airflow function."
    )


def test_relationship_can_store_provenance() -> None:
    provenance = Provenance(
        source="Machine Builder research",
        evidence_type="architectural",
        method="research checkpoint",
    )

    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="component-fan-a",
        target_id="function-cooling",
        relationship_type="participates_in",
        provenance=[
            provenance
        ],
    )

    assert (
        relationship.provenance[0]
        is provenance
    )

    assert (
        relationship.provenance[0].source
        == "Machine Builder research"
    )


def test_known_relationship_types_are_accepted() -> None:
    for relationship_type in RELATIONSHIP_TYPES:
        relationship = SemanticRelationship(
            id=f"relationship-{relationship_type}",
            source_id="source",
            target_id="target",
            relationship_type=relationship_type,
        )

        assert (
            relationship.relationship_type
            == relationship_type
        )


def test_unknown_relationship_type_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Unknown semantic relationship type",
    ):
        SemanticRelationship(
            id="relationship-1",
            source_id="source",
            target_id="target",
            relationship_type="made_of",
        )


def test_empty_id_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="ID cannot be empty",
    ):
        SemanticRelationship(
            id="",
            source_id="source",
            target_id="target",
            relationship_type="supports",
        )


def test_self_relationship_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="cannot reference itself",
    ):
        SemanticRelationship(
            id="relationship-1",
            source_id="object-1",
            target_id="object-1",
            relationship_type="supports",
        )


def test_relationship_can_match_endpoints() -> None:
    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="component-heater",
        target_id="function-temperature-control",
        relationship_type="realizes",
    )

    assert relationship.connects(
        "component-heater",
        "function-temperature-control",
    )

    assert not relationship.connects(
        "function-temperature-control",
        "component-heater",
    )


def test_relationship_can_match_type() -> None:
    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="component-heater",
        target_id="function-temperature-control",
        relationship_type="realizes",
    )

    assert relationship.is_type(
        "realizes"
    )

    assert not relationship.is_type(
        "supports"
    )