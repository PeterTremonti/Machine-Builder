"""Tests for documented controller-board physical-interface fixtures."""

from collections import Counter

from machine_builder.controller_board_fixtures import (
    add_duet_2_maestro_physical_interfaces,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
)


def _build_model() -> CanonicalMachineModel:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="test-machine",
            name="Test Machine",
        )
    )

    return model


def test_duet_maestro_fixture_creates_installed_controller() -> None:
    model = _build_model()

    controller, _ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            "test-machine",
        )
    )

    assert controller.id in model.controllers
    assert controller.hardware_definition_id == (
        "duet-2-maestro-v1-0"
    )


def test_duet_maestro_physical_ports_are_controller_owned() -> None:
    model = _build_model()

    controller, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            "test-machine",
        )
    )

    assert len(ports) == 26
    assert all(
        port.controller_id == controller.id
        for port in ports
    )
    assert all(
        port.component_id is None
        for port in ports
    )
    assert controller.port_ids == [
        port.id
        for port in ports
    ]


def test_duet_maestro_connector_groups_have_expected_sizes() -> None:
    model = _build_model()

    _controller, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            "test-machine",
        )
    )

    counts = Counter(
        port.connector_id
        for port in ports
    )

    assert counts == {
        "x-motor": 4,
        "z-a-motor": 4,
        "z-b-motor": 4,
        "heater": 2,
        "thermistor": 2,
        "endstop": 3,
        "z-probe": 5,
        "fan": 2,
    }


def test_duet_maestro_connector_positions_are_numbered() -> None:
    model = _build_model()

    _controller, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            "test-machine",
        )
    )

    positions: dict[str, set[str]] = {}

    for port in ports:
        positions.setdefault(
            port.connector_id,
            set(),
        ).add(port.pin_id)

    assert positions == {
        "x-motor": {"1", "2", "3", "4"},
        "z-a-motor": {"1", "2", "3", "4"},
        "z-b-motor": {"1", "2", "3", "4"},
        "heater": {"1", "2"},
        "thermistor": {"1", "2"},
        "endstop": {"1", "2", "3"},
        "z-probe": {"1", "2", "3", "4", "5"},
        "fan": {"1", "2"},
    }


def test_duet_maestro_z_a_and_z_b_are_distinct_physical_connectors() -> None:
    model = _build_model()

    _controller, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            "test-machine",
        )
    )

    z_a_ids = {
        port.id
        for port in ports
        if port.connector_id == "z-a-motor"
    }
    z_b_ids = {
        port.id
        for port in ports
        if port.connector_id == "z-b-motor"
    }

    assert len(z_a_ids) == 4
    assert len(z_b_ids) == 4
    assert z_a_ids.isdisjoint(z_b_ids)


def test_duet_maestro_fixture_does_not_create_connector_resource_mapping() -> None:
    model = _build_model()

    _controller, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            "test-machine",
        )
    )

    assert ports
    assert model.controller_resources == {}