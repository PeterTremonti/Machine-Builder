"""Tests for Capability integration into the canonical model."""

import pytest

from machine_builder.semantic_capability import (
    Capability,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Function,
    Machine,
    MachineComponent,
)
from machine_builder.semantic_relationship import (
    SemanticRelationship,
)


def build_model() -> CanonicalMachineModel:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    return model


def test_capability_can_be_added_to_machine() -> None:
    model = build_model()

    capability = Capability(
        id="capability-1",
        name="Temperature Control",
    )

    model.add_capability(
        "machine-1",
        capability,
    )

    assert (
        model.capabilities["capability-1"]
        is capability
    )

    assert (
        model.machines[
            "machine-1"
        ].capability_ids
        == ["capability-1"]
    )


def test_capability_can_be_retrieved() -> None:
    model = build_model()

    capability = Capability(
        id="capability-1",
        name="Temperature Control",
    )

    model.add_capability(
        "machine-1",
        capability,
    )

    assert (
        model.get_capability(
            "capability-1"
        )
        is capability
    )


def test_capability_can_be_removed() -> None:
    model = build_model()

    capability = Capability(
        id="capability-1",
        name="Temperature Control",
    )

    model.add_capability(
        "machine-1",
        capability,
    )

    removed = model.remove_capability(
        "capability-1"
    )

    assert removed is capability
    assert (
        "capability-1"
        not in model.capabilities
    )
    assert (
        model.machines[
            "machine-1"
        ].capability_ids
        == []
    )


def test_capability_with_unknown_machine_is_rejected() -> None:
    model = CanonicalMachineModel()

    with pytest.raises(
        ValueError,
        match="Unknown machine",
    ):
        model.add_capability(
            "missing-machine",
            Capability(
                id="capability-1",
                name="Temperature Control",
            ),
        )


def test_duplicate_capability_is_rejected() -> None:
    model = build_model()

    model.add_capability(
        "machine-1",
        Capability(
            id="capability-1",
            name="Temperature Control",
        ),
    )

    with pytest.raises(
        ValueError,
        match="Capability already exists",
    ):
        model.add_capability(
            "machine-1",
            Capability(
                id="capability-1",
                name="Material Cooling",
            ),
        )


def test_unknown_capability_is_rejected_when_retrieved() -> None:
    model = build_model()

    with pytest.raises(
        KeyError,
        match="Unknown capability",
    ):
        model.get_capability(
            "missing-capability"
        )


def test_unknown_capability_is_rejected_when_removed() -> None:
    model = build_model()

    with pytest.raises(
        KeyError,
        match="Unknown capability",
    ):
        model.remove_capability(
            "missing-capability"
        )


def test_relationship_can_target_capability() -> None:
    model = build_model()

    model.add_component(
        "machine-1",
        MachineComponent(
            id="component-1",
            role="Heater",
        ),
    )

    model.add_capability(
        "machine-1",
        Capability(
            id="capability-1",
            name="Temperature Control",
        ),
    )

    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="component-1",
        target_id="capability-1",
        relationship_type="supports",
    )

    model.add_relationship(
        relationship
    )

    assert (
        model.get_relationship(
            "relationship-1"
        )
        is relationship
    )


def test_relationship_can_connect_function_and_capability() -> None:
    model = build_model()

    model.add_function(
        "machine-1",
        Function(
            id="function-1",
            name="Control Hotend Temperature",
        ),
    )

    model.add_capability(
        "machine-1",
        Capability(
            id="capability-1",
            name="Temperature Control",
        ),
    )

    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="function-1",
        target_id="capability-1",
        relationship_type="realizes",
    )

    model.add_relationship(
        relationship
    )

    assert (
        model.get_relationship(
            "relationship-1"
        ).relationship_type
        == "realizes"
    )


def test_remove_capability_removes_related_relationships() -> None:
    model = build_model()

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

    relationship = SemanticRelationship(
        id="relationship-1",
        source_id="function-1",
        target_id="capability-1",
        relationship_type="realizes",
    )

    model.add_relationship(
        relationship
    )

    model.remove_capability(
        "capability-1"
    )

    assert (
        "relationship-1"
        not in model.relationships
    )


def test_machine_can_contain_functions_and_capabilities() -> None:
    model = build_model()

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

    machine = model.machines[
        "machine-1"
    ]

    assert machine.function_ids == [
        "function-1"
    ]

    assert machine.capability_ids == [
        "capability-1"
    ]