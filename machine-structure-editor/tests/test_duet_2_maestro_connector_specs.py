"""Tests for verified Duet 2 Maestro connector information."""

from machine_builder.controller_board_fixtures import (
    add_duet_2_maestro_physical_interfaces,
)
from machine_builder.hardware_catalog import (
    DUET2_MAESTRO_ENDSTOP_CONNECTOR_IDS,
    DUET2_MAESTRO_ENDSTOP_SIGNAL_LABELS,
    DUET2_MAESTRO_MOTOR_PIN_LABELS,
    build_duet_2_maestro,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
)


def make_test_model() -> CanonicalMachineModel:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test machine",
        )
    )

    return model


def test_maestro_motor_connector_specifications_are_present() -> None:
    hardware = build_duet_2_maestro()

    specifications = hardware.properties[
        "connector_specifications"
    ]

    for connector_id in (
        "x-motor",
        "y-motor",
        "z-a-motor",
        "z-b-motor",
        "e0-motor",
        "e1-motor",
    ):
        specification = specifications[
            connector_id
        ]

        assert (
            specification["position_count"]
            == 4
        )

        assert (
            specification["board_interface"]
            == "4-position 2.54 mm pin header"
        )

        assert (
            specification["mating_interface_family"]
            == "Molex KK 254-compatible"
        )

        assert (
            specification["mating_housing_part_number"]
            == "22-01-3047"
        )

        assert (
            specification["mating_contact_part_number"]
            == "08-50-0114"
        )

        assert (
            specification["pin_labels"]
            == list(
                DUET2_MAESTRO_MOTOR_PIN_LABELS
            )
        )


def test_maestro_endstop_connector_specifications_are_present() -> None:
    hardware = build_duet_2_maestro()

    specifications = hardware.properties[
        "connector_specifications"
    ]

    for connector_id in (
        DUET2_MAESTRO_ENDSTOP_CONNECTOR_IDS
    ):
        specification = specifications[
            connector_id
        ]

        assert (
            specification["position_count"]
            == 3
        )

        assert (
            specification["board_interface"]
            == "3-position 2.54 mm pin header"
        )

        assert (
            specification["mating_interface_family"]
            == "Molex KK 254-compatible"
        )

        assert (
            specification["mating_housing_part_number"]
            == "22-01-3037"
        )

        assert (
            specification["mating_contact_part_number"]
            == "08-50-0114"
        )

        assert (
            specification["pin_positions"]["1"]
            == DUET2_MAESTRO_ENDSTOP_SIGNAL_LABELS[
                connector_id
            ]
        )

        assert (
            specification["pin_positions"]["2"]
            == "+3.3 V"
        )

        assert (
            specification["pin_positions"]["3"]
            == "GND"
        )


def test_installed_endstop_ports_have_verified_roles() -> None:
    model = make_test_model()

    _, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            machine_id="machine-1",
        )
    )

    expected_roles = {
        "1": "endstop_input",
        "2": "power_supply_3v3",
        "3": "ground_reference",
    }

    for connector_id in (
        DUET2_MAESTRO_ENDSTOP_CONNECTOR_IDS
    ):
        connector_ports = [
            port
            for port in ports
            if port.connector_id == connector_id
        ]

        assert len(
            connector_ports
        ) == 3

        for port in connector_ports:
            assert (
                port.properties[
                    "electrical_role"
                ]
                == expected_roles[
                    port.pin_id
                ]
            )