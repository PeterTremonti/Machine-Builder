"""Tests for the canonical Function model."""

import pytest

from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Function,
    Machine,
    Provenance,
)


def test_function_can_be_added_to_machine() -> None:
    model = CanonicalMachineModel()

    machine = Machine(
        id="machine-1",
        name="Test Printer",
    )

    model.add_machine(
        machine
    )

    function = Function(
        id="function-1",
        name="Control Hotend Temperature",
    )

    model.add_function(
        "machine-1",
        function,
    )

    assert (
        model.functions["function-1"]
        is function
    )

    assert machine.function_ids == [
        "function-1"
    ]


def test_function_can_store_description() -> None:
    function = Function(
        id="function-1",
        name="Control Hotend Temperature",
        description=(
            "Maintain the hotend at a requested "
            "temperature."
        ),
    )

    assert (
        function.name
        == "Control Hotend Temperature"
    )

    assert (
        function.description
        == (
            "Maintain the hotend at a requested "
            "temperature."
        )
    )


def test_function_can_store_properties() -> None:
    function = Function(
        id="function-1",
        name="Move X",
        properties={
            "axis": "X",
            "behavior": "position_control",
        },
    )

    assert (
        function.properties["axis"]
        == "X"
    )

    assert (
        function.properties["behavior"]
        == "position_control"
    )


def test_function_can_store_provenance() -> None:
    provenance = Provenance(
        source="Research checkpoint",
        evidence_type="architectural",
        method="project research",
    )

    function = Function(
        id="function-1",
        name="Move X",
        provenance=[
            provenance
        ],
    )

    assert (
        function.provenance[0]
        is provenance
    )

    assert (
        function.provenance[0].source
        == "Research checkpoint"
    )


def test_function_with_unknown_machine_is_rejected() -> None:
    model = CanonicalMachineModel()

    function = Function(
        id="function-1",
        name="Move X",
    )

    with pytest.raises(
        ValueError,
        match="Unknown machine",
    ):
        model.add_function(
            "missing-machine",
            function,
        )


def test_duplicate_function_is_rejected() -> None:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Printer",
        )
    )

    model.add_function(
        "machine-1",
        Function(
            id="function-1",
            name="Move X",
        ),
    )

    with pytest.raises(
        ValueError,
        match="Function already exists",
    ):
        model.add_function(
            "machine-1",
            Function(
                id="function-1",
                name="Move Y",
            ),
        )


def test_function_can_be_retrieved() -> None:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Printer",
        )
    )

    function = Function(
        id="function-1",
        name="Measure Hotend Temperature",
    )

    model.add_function(
        "machine-1",
        function,
    )

    assert (
        model.get_function("function-1")
        is function
    )


def test_function_can_be_removed_from_machine() -> None:
    model = CanonicalMachineModel()

    machine = Machine(
        id="machine-1",
        name="Test Printer",
    )

    model.add_machine(
        machine
    )

    model.add_function(
        "machine-1",
        Function(
            id="function-1",
            name="Move X",
        ),
    )

    removed = model.remove_function(
        "function-1"
    )

    assert removed.id == "function-1"

    assert (
        "function-1"
        not in model.functions
    )

    assert machine.function_ids == []


def test_removing_unknown_function_is_rejected() -> None:
    model = CanonicalMachineModel()

    with pytest.raises(
        KeyError,
        match="Unknown function",
    ):
        model.remove_function(
            "missing-function"
        )