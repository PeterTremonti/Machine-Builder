"""Tests for verified Duet 2 Maestro connector information."""

from machine_builder.controller_board_fixtures import (
    add_duet_2_maestro_physical_interfaces,
)
from machine_builder.hardware_catalog import (
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


def test_maestro_motor_connector_specification_is_verified() -> None:
    hardware = build_duet_2_maestro()

    specifications = hardware.properties[
        "connector_specifications"
    ]

    assert set(specifications) == {
        "x-motor",
        "y-motor",
        "z-a-motor",
        "z-b-motor",
        "e0-motor",
        "e1-motor",
    }

    for specification in specifications.values():
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


def test_maestro_z_motor_ports_have_verified_pin_labels() -> None:
    model = make_test_model()

    _, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            machine_id="machine-1",
        )
    )

    for connector_id in (
        "z-a-motor",
        "z-b-motor",
    ):
        motor_ports = [
            port
            for port in ports
            if port.connector_id
            == connector_id
        ]

        assert [
            port.properties["pin_label"]
            for port in motor_ports
        ] == list(
            DUET2_MAESTRO_MOTOR_PIN_LABELS
        )

        assert [
            port.purpose
            for port in motor_ports
        ] == [
            "Stepper motor coil B1 terminal",
            "Stepper motor coil B2 terminal",
            "Stepper motor coil A1 terminal",
            "Stepper motor coil A2 terminal",
        ]