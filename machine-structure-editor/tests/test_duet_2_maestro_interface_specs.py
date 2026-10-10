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
    "j4",
    "temp-ob",
    "usdhc",
    "j23",
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
        15 + len(EXPECTED_ADDITIONAL_INTERFACE_IDS)
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
        "temp-ob": "expansion_or_service",
        "usdhc": "expansion_or_service",
        "j23": "power_configuration",
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
        .startswith("Manufacturer schematic")
    )


def test_maestro_catalog_physical_references_are_documented() -> None:
    specifications = build_duet_2_maestro().properties[
        "connector_specifications"
    ]

    expected_board_references = {
        "usdhc": "J15",
        "5v-ps": "J20",
        "usb": "J22",
        "j23": "J23",
        "c-gnd": "J27",
        "paneldue": "J30",
        "ethernet": "J38",
        "12864-exp2": "P1",
        "12864-exp1": "P2",
        "paneldue-sd": "P3",
        "a-vin": "J3",
    }

    for connector_id, board_reference in expected_board_references.items():
        assert specifications[connector_id]["board_reference"] == board_reference

    assert specifications["usdhc"]["position_count"] == 9
    assert specifications["5v-ps"]["position_count"] == 3
    assert specifications["usb"]["position_count"] == 5
    assert specifications["j23"]["position_count"] == 3
    assert specifications["ethernet"]["position_count"] == 8
    assert specifications["12864-exp2"]["pin_positions"] == {
        "1": "SPI0_MISO_BUFF",
        "2": "SPI0_SCK_BUFF",
        "3": "ENC_B",
        "4": "SPI0_CS0",
        "5": "ENC_A",
        "6": "SPI0_MOSI_BUFF",
        "7": "NC",
        "8": "RESET_EXT",
        "9": "GND",
        "10": "NC",
    }
    assert specifications["12864-exp1"]["pin_positions"] == {
        "1": "BEEP",
        "2": "ENC_SW",
        "3": "SPI0_MOSI_LCD_BUFF",
        "4": "LCD_CS_BUFF",
        "5": "SPI0_SCK_LCD_BUFF",
        "6": "NC",
        "7": "NC",
        "8": "NC",
        "9": "GND",
        "10": "+5V",
    }
def test_maestro_board_test_points_are_cataloged_as_ate_features() -> None:
    board_features = build_duet_2_maestro().properties[
        "board_features"
    ]
    test_ate = board_features["test_ate"]
    points = test_ate["points"]

    assert test_ate["all_test_points_dnp"] is True
    assert test_ate["point_count"] == 15
    assert test_ate["physical_contact_count"] == 25
    assert set(points) == {
        "TP1",
        "TP2",
        "TP3",
        "TP4",
        "TP5",
        "TP6",
        "TP7",
        "TP8",
        "TP9",
        "TP10",
        "TP11",
        "TP12",
        "TP13",
        "TP14",
        "TP16",
    }
    assert "TP15" not in points

    expected_step_dir_uart = {
        "TP1": ("Z_STEP", "Z_DIR", "Z_UART"),
        "TP2": ("Y_STEP", "Y_DIR", "Y_UART"),
        "TP3": ("X_STEP", "X_DIR", "X_UART"),
        "TP4": ("E0_STEP", "E0_DIR", "E0_UART"),
        "TP5": ("E1_STEP", "E1_DIR", "E1_UART"),
    }

    for point_id, signals in expected_step_dir_uart.items():
        assert points[point_id]["position_count"] == 3
        assert tuple(
            points[point_id]["pin_positions"].values()
        ) == signals
        assert points[point_id]["purpose"] == "ATE/test only"

    expected_individual_nets = {
        "TP6": "HEATER0",
        "TP7": "HEATER1",
        "TP8": "HEATER2",
        "TP9": "BED_PWM",
        "TP10": "E0_PWM",
        "TP11": "E1_PWM",
        "TP12": "FAN0",
        "TP13": "FAN1",
        "TP14": "FAN2",
        "TP16": "D6_TestPoint",
    }

    for point_id, net in expected_individual_nets.items():
        assert points[point_id]["net"] == net


def test_maestro_board_indicators_are_cataloged_without_becoming_machine_io() -> None:
    board_features = build_duet_2_maestro().properties[
        "board_features"
    ]
    indicators = board_features["board_indicators"]

    assert set(indicators["items"]) == {
        "D3",
        "D4",
        "D6",
        "D7",
        "D20",
        "D15",
        "D16",
        "D17",
    }
    assert indicators["items"]["D3"]["net"] == "VBUS"
    assert indicators["items"]["D15"]["net"] == "V_IN"
    assert indicators["items"]["D16"]["net"] == "+3.3V"
    assert indicators["items"]["D17"]["net"] == "+5V"
    assert indicators["items"]["D20"]["board_label"] == "E1 Heat"
    assert (
        indicators["items"]["D20"]["purpose"]
        == "E1 heater activity indication"
    )
    assert indicators["items"]["D4"]["classification"] == (
        "board_status_observability"
    )
    assert indicators["items"]["D4"]["net"] == "SERVO"
    assert indicators["items"]["D4"]["series_resistance"] == "2.2 kΩ"
    assert (
        "not established"
        in indicators["items"]["D4"]["evidence_status"]
    )

    ethernet_indicators = indicators[
        "integrated_interface_indicators"
    ]["ethernet-j38"]
    assert ethernet_indicators["board_reference"] == "J38"
    assert tuple(ethernet_indicators["signals"]) == (
        "ACTLED",
        "LINKLED",
    )


def test_maestro_service_controls_are_cataloged() -> None:
    board_features = build_duet_2_maestro().properties[
        "board_features"
    ]
    controls = board_features["service_controls"]["items"]

    assert set(controls) == {
        "S1",
        "JP1",
        "JP9",
        "JP10",
    }
    assert controls["S1"]["board_label"] == "RESET"
    assert controls["JP1"]["catalog_reference"] == "erase"
    assert controls["JP9"]["board_label"] == "I 5V EN"
    assert controls["JP10"]["catalog_reference"] == "e-5v-en"

def test_maestro_alternate_heater_access_is_cataloged() -> None:
    board_features = build_duet_2_maestro().properties[
        "board_features"
    ]
    access = board_features["alternate_heater_access"]["items"]

    assert set(access) == {"J16", "J17"}

    assert access["J16"]["board_reference"] == "J16"
    assert access["J16"]["electrical_association"] == "E0 HEAT"
    assert access["J16"]["position_count"] == 2
    assert (
        access["J16"]["population_status"]
        == "Design-level; production population unverified."
    )

    assert access["J17"]["board_reference"] == "J17"
    assert access["J17"]["electrical_association"] == "E1 HEAT"
    assert access["J17"]["position_count"] == 2
    assert (
        access["J17"]["population_status"]
        == "Design-level; production population unverified."
    )
