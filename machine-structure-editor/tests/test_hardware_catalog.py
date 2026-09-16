"""Tests for reusable hardware definitions."""

from machine_builder.hardware_catalog import (
    FAN_LISTING_URL,
    build_generic_120vac_400w_heater,
    build_generic_4010_24v_fan,
)


def test_real_fan_definition_is_24v_generic_4010() -> None:
    hardware, ports = (
        build_generic_4010_24v_fan()
    )

    assert hardware.family == (
        "4010 axial fan"
    )

    assert hardware.manufacturer == (
        "Generic / Unbranded"
    )

    assert hardware.variant == "24 V"

    assert len(
        ports
    ) == 2


def test_real_fan_definition_preserves_listing_source() -> None:
    hardware, _ports = (
        build_generic_4010_24v_fan()
    )

    assert FAN_LISTING_URL in [
        provenance.source
        for provenance in hardware.provenance
    ]


def test_real_fan_definition_has_power_and_ground_ports() -> None:
    _hardware, ports = (
        build_generic_4010_24v_fan()
    )

    purposes = {
        port.purpose
        for port in ports
    }

    assert purposes == {
        "Power",
        "Ground",
    }


def test_real_fan_definition_keeps_connector_details_partial() -> None:
    hardware, ports = (
        build_generic_4010_24v_fan()
    )

    assert hardware.properties[
        "connector_description"
    ] == "2 Terminal Connector with 2pin-PH2.5"

    assert hardware.properties[
        "connector_series"
    ] is None

    assert hardware.properties[
        "connector_pin_details"
    ] is None

    assert all(
        port.connector_id is None
        and port.pin_id is None
        for port in ports
    )


def test_real_heater_definition_is_120vac_400w() -> None:
    hardware, ports = (
        build_generic_120vac_400w_heater()
    )

    assert hardware.family == (
        "resistive heater"
    )

    assert hardware.manufacturer == (
        "Generic / Unbranded"
    )

    assert hardware.variant == (
        "120 VAC 400 W"
    )

    assert len(
        ports
    ) == 2


def test_real_heater_preserves_known_power_properties() -> None:
    hardware, _ports = (
        build_generic_120vac_400w_heater()
    )

    assert hardware.properties[
        "voltage"
    ] == "120 VAC"

    assert hardware.properties[
        "power"
    ] == "400 W"

    assert hardware.properties[
        "calculated_current"
    ] == "3.33 A"


def test_real_heater_keeps_terminal_identity_partial() -> None:
    hardware, ports = (
        build_generic_120vac_400w_heater()
    )

    assert hardware.properties[
        "terminal_identity"
    ] is None

    assert all(
        port.connector_id is None
        and port.pin_id is None
        for port in ports
    )


def test_real_heater_has_two_power_terminals() -> None:
    _hardware, ports = (
        build_generic_120vac_400w_heater()
    )

    assert {
        port.purpose
        for port in ports
    } == {
        "Power"
    }

    assert all(
        port.direction == "input"
        for port in ports
    )

    assert all(
        port.properties[
            "expected_voltage"
        ] == "120 VAC"
        for port in ports
    )


def test_fan_and_heater_are_distinct_hardware_definitions() -> None:
    fan, _fan_ports = (
        build_generic_4010_24v_fan()
    )

    heater, _heater_ports = (
        build_generic_120vac_400w_heater()
    )

    assert (
        fan.id
        != heater.id
    )

    assert (
        fan.family
        != heater.family
    )

    assert (
        fan.variant
        != heater.variant
    )