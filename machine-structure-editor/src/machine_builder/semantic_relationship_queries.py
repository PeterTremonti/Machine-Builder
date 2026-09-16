"""Queries for canonical semantic relationships."""

from __future__ import annotations

from .semantic_model import CanonicalMachineModel
from .semantic_relationship import SemanticRelationship


def relationships_from(
    model: CanonicalMachineModel,
    source_id: str,
) -> list[SemanticRelationship]:
    """Return relationships whose source is the given object."""
    return [
        relationship
        for relationship in model.relationships.values()
        if relationship.source_id == source_id
    ]


def relationships_to(
    model: CanonicalMachineModel,
    target_id: str,
) -> list[SemanticRelationship]:
    """Return relationships whose target is the given object."""
    return [
        relationship
        for relationship in model.relationships.values()
        if relationship.target_id == target_id
    ]


def relationships_of_type(
    model: CanonicalMachineModel,
    relationship_type: str,
) -> list[SemanticRelationship]:
    """Return all relationships of the requested type."""
    return [
        relationship
        for relationship in model.relationships.values()
        if relationship.relationship_type == relationship_type
    ]


def relationships_between(
    model: CanonicalMachineModel,
    source_id: str,
    target_id: str,
) -> list[SemanticRelationship]:
    """Return relationships between two specific ordered endpoints."""
    return [
        relationship
        for relationship in model.relationships.values()
        if (
            relationship.source_id == source_id
            and relationship.target_id == target_id
        )
    ]