"""Tests for canonical hardware-component fixture helpers."""

from machine_builder.hardware_component_fixtures import (
    add_generic_120vac_400w_heater,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
)


def test_add_heater_adds_component() -> None:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    component = add_generic_120vac_400w_heater(
        model,
        "machine-1",
    )

    assert component.id == "chamber-heater-1"
    assert component.label == "Chamber Heater"

    assert (
        model.components[
            "chamber-heater-1"
        ]
        is component
    )


def test_add_heater_adds_hardware_definition() -> None:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    component = add_generic_120vac_400w_heater(
        model,
        "machine-1",
    )

    assert (
        component.hardware_definition_id
        == "generic-120vac-400w-heater"
    )

    assert (
        "generic-120vac-400w-heater"
        in model.hardware_definitions
    )


def test_add_heater_adds_component_scoped_ports() -> None:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    component = add_generic_120vac_400w_heater(
        model,
        "machine-1",
    )

    assert component.port_ids == [
        "chamber-heater-1-terminal-a",
        "chamber-heater-1-terminal-b",
    ]


def test_add_heater_ports_belong_to_component() -> None:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    component = add_generic_120vac_400w_heater(
        model,
        "machine-1",
    )

    for port_id in component.port_ids:
        assert (
            model.get_port(
                port_id
            ).component_id
            == component.id
        )


def test_multiple_heaters_can_share_hardware_definition() -> None:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    first = add_generic_120vac_400w_heater(
        model,
        "machine-1",
        component_id="chamber-heater-1",
    )

    second = add_generic_120vac_400w_heater(
        model,
        "machine-1",
        component_id="chamber-heater-2",
    )

    assert (
        first.hardware_definition_id
        == second.hardware_definition_id
    )

    assert first.port_ids == [
        "chamber-heater-1-terminal-a",
        "chamber-heater-1-terminal-b",
    ]

    assert second.port_ids == [
        "chamber-heater-2-terminal-a",
        "chamber-heater-2-terminal-b",
    ]

    assert (
        first.port_ids[0]
        != second.port_ids[0]
    )