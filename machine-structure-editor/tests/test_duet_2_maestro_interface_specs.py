"""Tests for the expanded Duet 2 Maestro physical interface specimen."""

from machine_builder.hardware_catalog import (
    DUET2_MAESTRO_ADDITIONAL_INTERFACE_SPECIFICATIONS,
    build_duet_2_maestro,
)


EXPECTED_ADDITIONAL_INTERFACE_IDS = {
    "fan0",
    "fan1",
    "fan2",
    "always-on-fan",
    "bed-temp",
    "e0-temp",
    "e1-temp",
    "c-temp",
    "z-probe",
    "e2-driver",
    "e3-driver",
    "paneldue",
    "paneldue-sd",
    "12864-exp1",
    "12864-exp2",
    "usb",
    "ethernet",
    "c-gnd",
    "j21",
    "temp-ob",
    "erase",
    "a-vin",
    "e-5v-en",
    "5v-ps",
}


def test_maestro_additional_interface_inventory_is_complete() -> None:
    hardware = build_duet_2_maestro()

    specifications = hardware.properties[
        "connector_specifications"
    ]

    assert set(
        DUET2_MAESTRO_ADDITIONAL_INTERFACE_SPECIFICATIONS
    ) == EXPECTED_ADDITIONAL_INTERFACE_IDS

    assert EXPECTED_ADDITIONAL_INTERFACE_IDS <= set(
        specifications
    )

    assert len(specifications) == (
        17 + len(EXPECTED_ADDITIONAL_INTERFACE_IDS)
    )


def test_maestro_controlled_fan_interfaces_are_real_physical_outputs() -> None:
    specifications = build_duet_2_maestro().properties[
        "connector_specifications"
    ]

    for connector_id in (
        "fan0",
        "fan1",
        "fan2",
    ):
        specification = specifications[
            connector_id
        ]

        assert specification["position_count"] == 2
        assert (
            specification["interface_role"]
            == "controlled_fan_output"
        )
        assert (
            specification["usage_classification"]
            == "machine_io"
        )


def test_maestro_temperature_and_probe_interfaces_are_classified() -> None:
    specifications = build_duet_2_maestro().properties[
        "connector_specifications"
    ]

    for connector_id in (
        "bed-temp",
        "e0-temp",
        "e1-temp",
    ):
        specification = specifications[
            connector_id
        ]

        assert specification["position_count"] == 2
        assert (
            specification["interface_role"]
            == "temperature_sensor_input"
        )

    probe = specifications["z-probe"]

    assert probe["position_count"] == 5
    assert probe["used_position_count"] == 3
    assert probe["unused_position_numbers"] == [3, 5]
    assert (
        probe["interface_role"]
        == "z_probe_interface"
    )


def test_maestro_external_driver_interfaces_are_distinct_from_machine_axes() -> None:
    specifications = build_duet_2_maestro().properties[
        "connector_specifications"
    ]

    for connector_id in (
        "e2-driver",
        "e3-driver",
    ):
        specification = specifications[
            connector_id
        ]

        assert specification["position_count"] == 8
        assert (
            specification["interface_role"]
            == "external_stepper_driver_module_interface"
        )
        assert (
            specification["usage_classification"]
            == "expansion_io"
        )


def test_maestro_display_and_communication_interfaces_are_cataloged() -> None:
    specifications = build_duet_2_maestro().properties[
        "connector_specifications"
    ]

    assert specifications["paneldue"]["position_count"] == 4
    assert (
        specifications["paneldue"]["usage_classification"]
        == "user_interface"
    )

    assert specifications["paneldue-sd"]["position_count"] == 10

    for connector_id in (
        "12864-exp1",
        "12864-exp2",
    ):
        assert (
            specifications[connector_id]["position_count"]
            == 10
        )
        assert (
            specifications[connector_id]["usage_classification"]
            == "user_interface"
        )

    assert (
        specifications["usb"]["usage_classification"]
        == "communication_service"
    )
    assert (
        specifications["ethernet"]["usage_classification"]
        == "communication_service"
    )


def test_maestro_service_power_and_unresolved_interfaces_are_not_promoted_to_machine_io() -> None:
    specifications = build_duet_2_maestro().properties[
        "connector_specifications"
    ]

    expected_catalog_only_classifications = {
        "paneldue": "user_interface",
        "paneldue-sd": "user_interface",
        "12864-exp1": "user_interface",
        "12864-exp2": "user_interface",
        "usb": "communication_service",
        "ethernet": "communication_service",
        "c-gnd": "power_reference",
        "j21": "expansion_or_service",
        "temp-ob": "unresolved",
        "erase": "service_configuration",
        "a-vin": "power_configuration",
        "e-5v-en": "power_configuration",
        "5v-ps": "power_configuration",
    }

    for connector_id, classification in (
        expected_catalog_only_classifications.items()
    ):
        assert (
            specifications[connector_id]["usage_classification"]
            == classification
        )

    assert (
        specifications["temp-ob"]["evidence_status"]
        .startswith("Physical label")
    )
