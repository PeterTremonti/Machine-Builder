"""Real-hardware fixture for the user's 120 VAC 400 W chamber heater."""

from machine_builder.hardware_catalog import (
    build_generic_120vac_400w_heater,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
)


def build_real_120vac_400w_heater() -> (
    tuple[
        CanonicalMachineModel,
        Machine,
        MachineComponent,
    ]
):
    """Build a canonical representation of one physical chamber heater."""
    model = CanonicalMachineModel()

    machine = Machine(
        id="test-machine",
        name="Test Machine",
    )

    model.add_machine(
        machine
    )

    hardware, ports = (
        build_generic_120vac_400w_heater()
    )

    model.add_hardware_definition(
        hardware
    )

    component = MachineComponent(
        id="chamber-heater-1",
        role="Chamber Heater",
        label="Chamber Heater",
        hardware_definition_id=hardware.id,
    )

    model.add_component(
        machine.id,
        component,
    )

    for source_port in ports:
        component_port = type(source_port)(
            id=(
                source_port.id.replace(
                    "generic-120vac-400w-heater",
                    "chamber-heater-1",
                )
            ),
            component_id=component.id,
            purpose=source_port.purpose,
            direction=source_port.direction,
            connector_id=source_port.connector_id,
            pin_id=source_port.pin_id,
            properties=source_port.properties.copy(),
            provenance=source_port.provenance.copy(),
        )

        model.add_port(
            component_port
        )

    return (
        model,
        machine,
        component,
    )


def test_real_heater_has_reusable_hardware_definition() -> None:
    (
        model,
        _machine,
        component,
    ) = build_real_120vac_400w_heater()

    hardware = model.hardware_definitions[
        component.hardware_definition_id
    ]

    assert hardware.family == (
        "resistive heater"
    )

    assert hardware.variant == (
        "120 VAC 400 W"
    )


def test_real_heater_component_has_two_ports() -> None:
    (
        model,
        _machine,
        component,
    ) = build_real_120vac_400w_heater()

    assert len(
        component.port_ids
    ) == 2

    ports = [
        model.get_port(
            port_id
        )
        for port_id in component.port_ids
    ]

    assert {
        port.purpose
        for port in ports
    } == {
        "Power"
    }


def test_real_heater_ports_have_component_scoped_identity() -> None:
    (
        model,
        _machine,
        component,
    ) = build_real_120vac_400w_heater()

    assert component.port_ids == [
        "chamber-heater-1-terminal-a",
        "chamber-heater-1-terminal-b",
    ]

    for port_id in component.port_ids:
        assert (
            model.get_port(
                port_id
            ).component_id
            == component.id
        )


def test_real_heater_preserves_partial_terminal_information() -> None:
    (
        model,
        _machine,
        component,
    ) = build_real_120vac_400w_heater()

    ports = [
        model.get_port(
            port_id
        )
        for port_id in component.port_ids
    ]

    assert all(
        port.connector_id is None
        for port in ports
    )

    assert all(
        port.pin_id is None
        for port in ports
    )