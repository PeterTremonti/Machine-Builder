"""Tests for hardware-backed component authoring."""

from machine_builder.hardware_authoring import (
    add_hardware_component,
)
from machine_builder.hardware_catalog import (
    build_generic_120vac_400w_heater,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
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


def test_add_hardware_component_creates_component() -> None:
    model = build_model()

    hardware, ports = (
        build_generic_120vac_400w_heater()
    )

    component = add_hardware_component(
        model=model,
        machine_id="machine-1",
        component_id="heater-1",
        role="Chamber Heater",
        label="Chamber Heater",
        hardware=hardware,
        ports=ports,
    )

    assert (
        model.components["heater-1"]
        is component
    )


def test_add_hardware_component_references_hardware() -> None:
    model = build_model()

    hardware, ports = (
        build_generic_120vac_400w_heater()
    )

    component = add_hardware_component(
        model=model,
        machine_id="machine-1",
        component_id="heater-1",
        role="Chamber Heater",
        label="Chamber Heater",
        hardware=hardware,
        ports=ports,
    )

    assert (
        component.hardware_definition_id
        == hardware.id
    )

    assert (
        model.hardware_definitions[
            hardware.id
        ]
        is hardware
    )


def test_add_hardware_component_adds_instance_ports() -> None:
    model = build_model()

    hardware, ports = (
        build_generic_120vac_400w_heater()
    )

    component = add_hardware_component(
        model=model,
        machine_id="machine-1",
        component_id="heater-1",
        role="Chamber Heater",
        label="Chamber Heater",
        hardware=hardware,
        ports=ports,
    )

    assert len(
        component.port_ids
    ) == 2

    for port_id in component.port_ids:
        assert (
            model.get_port(
                port_id
            ).component_id
            == component.id
        )


def test_add_hardware_component_reuses_existing_hardware() -> None:
    model = build_model()

    hardware, ports = (
        build_generic_120vac_400w_heater()
    )

    first = add_hardware_component(
        model=model,
        machine_id="machine-1",
        component_id="heater-1",
        role="Chamber Heater",
        label="Chamber Heater 1",
        hardware=hardware,
        ports=ports,
    )

    second = add_hardware_component(
        model=model,
        machine_id="machine-1",
        component_id="heater-2",
        role="Chamber Heater",
        label="Chamber Heater 2",
        hardware=hardware,
        ports=ports,
    )

    assert (
        first.hardware_definition_id
        == second.hardware_definition_id
    )

    assert (
        first.id != second.id
    )

    assert (
        first.port_ids
        != second.port_ids
    )


def test_add_hardware_component_preserves_port_properties() -> None:
    model = build_model()

    hardware, ports = (
        build_generic_120vac_400w_heater()
    )

    component = add_hardware_component(
        model=model,
        machine_id="machine-1",
        component_id="heater-1",
        role="Chamber Heater",
        label="Chamber Heater",
        hardware=hardware,
        ports=ports,
    )

    for port_id in component.port_ids:
        port = model.get_port(
            port_id
        )

        assert (
            port.properties[
                "expected_voltage"
            ]
            == "120 VAC"
        )