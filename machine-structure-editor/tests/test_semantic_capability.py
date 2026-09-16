"""Tests for canonical capabilities."""

import pytest

from machine_builder.semantic_capability import (
    Capability,
)
from machine_builder.semantic_model import (
    Provenance,
)


def test_capability_can_be_created() -> None:
    capability = Capability(
        id="capability-1",
        name="Temperature Control",
    )

    assert capability.id == "capability-1"
    assert capability.name == "Temperature Control"
    assert capability.description == ""


def test_capability_can_store_description() -> None:
    capability = Capability(
        id="capability-1",
        name="Temperature Control",
        description=(
            "Maintain a machine zone near "
            "a requested temperature."
        ),
    )

    assert (
        capability.description
        == (
            "Maintain a machine zone near "
            "a requested temperature."
        )
    )


def test_capability_can_store_properties() -> None:
    capability = Capability(
        id="capability-1",
        name="Temperature Control",
        properties={
            "domain": "thermal",
            "target": "hotend",
        },
    )

    assert (
        capability.properties["domain"]
        == "thermal"
    )

    assert (
        capability.properties["target"]
        == "hotend"
    )


def test_capability_can_store_provenance() -> None:
    provenance = Provenance(
        source="Machine Builder research",
        evidence_type="architectural",
        method="research checkpoint",
    )

    capability = Capability(
        id="capability-1",
        name="Temperature Control",
        provenance=[
            provenance
        ],
    )

    assert (
        capability.provenance[0]
        is provenance
    )


def test_empty_capability_id_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Capability ID cannot be empty",
    ):
        Capability(
            id="",
            name="Temperature Control",
        )


def test_empty_capability_name_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Capability name cannot be empty",
    ):
        Capability(
            id="capability-1",
            name="",
        )


def test_capability_is_distinct_from_function() -> None:
    from machine_builder.semantic_model import (
        Function,
    )

    capability = Capability(
        id="capability-1",
        name="Temperature Control",
    )

    function = Function(
        id="function-1",
        name="Control Hotend Temperature",
    )

    assert capability.id != function.id
    assert capability.name != function.name


def test_capability_can_preserve_partial_information() -> None:
    capability = Capability(
        id="capability-1",
        name="Material Cooling",
        properties={
            "confidence": "partial",
            "implementation": None,
        },
    )

    assert (
        capability.properties["confidence"]
        == "partial"
    )

    assert (
        capability.properties["implementation"]
        is None
    )