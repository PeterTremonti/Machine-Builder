"""Tests for reusable hardware definitions."""

from machine_builder.hardware_catalog import (
    FAN_LISTING_URL,
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