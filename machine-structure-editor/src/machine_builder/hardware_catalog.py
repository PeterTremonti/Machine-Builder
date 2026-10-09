"""Reusable hardware definitions for the Machine Structure Editor.

This module contains concrete hardware definitions that can be associated
with machine components.

Connector specifications stored in HardwareDefinition.properties describe
reusable interface information associated with the documented hardware.
They are catalog information, not separate canonical Connector entities.
"""

from __future__ import annotations

from .semantic_model import (
    HardwareDefinition,
    Provenance,
    SemanticPort,
)


FAN_LISTING_URL = (
    "https://www.aliexpress.us/item/"
    "3256805820145702.html"
)


def build_generic_4010_24v_fan() -> (
    tuple[
        HardwareDefinition,
        tuple[SemanticPort, SemanticPort],
    ]
):
    """Build the real generic/unbranded 24 V 4010 fan definition."""
    hardware = HardwareDefinition(
        id="generic-4010-fan-24v",
        family="4010 axial fan",
        manufacturer="Generic / Unbranded",
        variant="24 V",
        properties={
            "dimensions": "40 × 40 × 10 mm",
            "voltage": "24 V DC",
            "working_current": "0.12 A",
            "bearing": "Oil",
            "noise": "22 dBA",
            "cable_length": "300 mm",
            "connector_description": (
                "2 Terminal Connector with 2pin-PH2.5"
            ),
            "connector_series": None,
            "connector_pin_details": None,
            "speed_claims": [
                {
                    "value": "8000 RPM",
                    "source": FAN_LISTING_URL,
                    "source_context": "listing description",
                    "variant": None,
                },
                {
                    "value": "6200 ±10% RPM",
                    "source": FAN_LISTING_URL,
                    "source_context": "listing specification",
                    "variant": None,
                },
            ],
            "speed_variant_assignment": None,
            "notes": (
                "The listing does not identify which speed claim "
                "corresponds to the 12 V or 24 V version."
            ),
        },
        provenance=[
            Provenance(
                source=FAN_LISTING_URL,
                evidence_type="published",
                method="seller listing",
                context="AliExpress product description",
            ),
            Provenance(
                source="user",
                evidence_type="authored",
                method="physical purchase",
                context=(
                    "User purchased the 24 V version of this "
                    "fan for use on a 24 V printer."
                ),
            ),
        ],
    )

    placeholder_component_id = (
        "PLACEHOLDER_COMPONENT"
    )

    ports = (
        SemanticPort(
            id="generic-4010-fan-24v-power",
            component_id=placeholder_component_id,
            purpose="Power",
            direction="input",
            connector_id=None,
            pin_id=None,
            properties={
                "expected_voltage": "24 V DC",
            },
            provenance=[
                Provenance(
                    source="user + product listing",
                    evidence_type="derived",
                    method="semantic interpretation",
                    context=(
                        "Two-terminal 24 V DC fan; detailed "
                        "connector pin identity is unknown."
                    ),
                )
            ],
        ),
        SemanticPort(
            id="generic-4010-fan-24v-ground",
            component_id=placeholder_component_id,
            purpose="Ground",
            direction="unknown",
            connector_id=None,
            pin_id=None,
            properties={},
            provenance=[
                Provenance(
                    source="user + product listing",
                    evidence_type="derived",
                    method="semantic interpretation",
                    context=(
                        "Two-terminal 24 V DC fan; detailed "
                        "connector pin identity is unknown."
                    ),
                )
            ],
        ),
    )

    return (
        hardware,
        ports,
    )


def build_generic_120vac_400w_heater() -> (
    tuple[
        HardwareDefinition,
        tuple[SemanticPort, SemanticPort],
    ]
):
    """Build the known 120 VAC 400 W chamber-heater definition.

    The exact terminal identities are intentionally left unspecified.
    The heater is represented as a two-terminal resistive load.
    """
    hardware = HardwareDefinition(
        id="generic-120vac-400w-heater",
        family="resistive heater",
        manufacturer="Generic / Unbranded",
        variant="120 VAC 400 W",
        properties={
            "voltage": "120 VAC",
            "power": "400 W",
            "calculated_current": "3.33 A",
            "terminal_count": 2,
            "terminal_identity": None,
            "notes": (
                "Used as a chamber heater on the user's "
                "Stratasys SST1200es. Exact terminal identity "
                "and connector details are not yet documented."
            ),
        },
        provenance=[
            Provenance(
                source="user",
                evidence_type="authored",
                method="physical inspection / ownership",
                context=(
                    "The user's Stratasys SST1200es uses "
                    "two 120 VAC 400 W chamber heaters."
                ),
            )
        ],
    )

    placeholder_component_id = (
        "PLACEHOLDER_COMPONENT"
    )

    ports = (
        SemanticPort(
            id="generic-120vac-400w-heater-terminal-a",
            component_id=placeholder_component_id,
            purpose="Power",
            direction="input",
            connector_id=None,
            pin_id=None,
            properties={
                "expected_voltage": "120 VAC",
            },
            provenance=[
                Provenance(
                    source="user",
                    evidence_type="derived",
                    method="semantic interpretation",
                    context=(
                        "One of two heater terminals; exact "
                        "electrical terminal identity is unknown."
                    ),
                )
            ],
        ),
        SemanticPort(
            id="generic-120vac-400w-heater-terminal-b",
            component_id=placeholder_component_id,
            purpose="Power",
            direction="input",
            connector_id=None,
            pin_id=None,
            properties={
                "expected_voltage": "120 VAC",
            },
            provenance=[
                Provenance(
                    source="user",
                    evidence_type="derived",
                    method="semantic interpretation",
                    context=(
                        "One of two heater terminals; exact "
                        "electrical terminal identity is unknown."
                    ),
                )
            ],
        ),
    )

    return (
        hardware,
        ports,
    )


DUET2_MAESTRO_HARDWARE_SOURCE = (
    "https://github.com/Duet3D/Duet-2-Hardware/tree/master/"
    "Duet2/Duet2Maestro_v1.0"
)

DUET2_MAESTRO_HEADERS_SOURCE = (
    "https://github.com/Duet3D/Duet-2-Hardware/blob/master/"
    "Duet2/Duet2Maestro_v1.0/Headers.sch"
)

DUET2_MAESTRO_WIRING_SOURCE = (
    "https://docs.duet3d.com/en/How_to_guides/"
    "Wiring_your_Duet_2"
)

DUET2_MAESTRO_PHYSICAL_INSPECTION_SOURCE = (
    "Direct physical inspection of a Duet 2 Maestro V1.0 PCB."
)

DUET2_MAESTRO_MOTOR_PIN_LABELS = (
    "B1",
    "B2",
    "A1",
    "A2",
)

DUET2_MAESTRO_MOTOR_CONNECTOR_IDS = (
    "x-motor",
    "y-motor",
    "z-a-motor",
    "z-b-motor",
    "e0-motor",
    "e1-motor",
)

DUET2_MAESTRO_MOTOR_CONNECTOR_SPEC = {
    "position_count": 4,
    "board_interface": (
        "4-position 2.54 mm pin header"
    ),
    "mating_interface_family": (
        "Molex KK 254-compatible"
    ),
    "mating_housing_part_number": (
        "22-01-3047"
    ),
    "mating_contact_part_number": (
        "08-50-0114"
    ),
    "pin_labels": list(
        DUET2_MAESTRO_MOTOR_PIN_LABELS
    ),
    "pin_role": (
        "Stepper motor coil terminal"
    ),
    "part_number_status": (
        "Catalog-compatible mating components; "
        "board-side header part number not yet verified."
    ),
}


DUET2_MAESTRO_ENDSTOP_CONNECTOR_IDS = (
    "x-stop",
    "y-stop",
    "z-stop",
    "e0-stop",
    "e1-stop",
)

DUET2_MAESTRO_ENDSTOP_SIGNAL_LABELS = {
    "x-stop": "xstop",
    "y-stop": "ystop",
    "z-stop": "zstop",
    "e0-stop": "e0stop",
    "e1-stop": "e1stop",
}

DUET2_MAESTRO_ENDSTOP_CONNECTOR_SPEC = {
    "position_count": 3,
    "board_interface": (
        "3-position 2.54 mm pin header"
    ),
    "mating_interface_family": (
        "Molex KK 254-compatible"
    ),
    "mating_housing_part_number": (
        "22-01-3037"
    ),
    "mating_contact_part_number": (
        "08-50-0114"
    ),
    "pin_positions": {
        "1": "endstop signal input",
        "2": "+3.3 V supply",
        "3": "GND",
    },
    "pin_roles": {
        "1": "endstop_input",
        "2": "power_supply_3v3",
        "3": "ground_reference",
    },
    "part_number_status": (
        "Catalog-compatible mating components; "
        "board-side header part number not separately verified."
    ),
}


DUET2_MAESTRO_HEATER_CONNECTOR_IDS = (
    "bed-heat-molex",
    "bed-heat-screw",
    "e0-heat-molex",
    "e0-heat-screw",
    "e1-heat-molex",
    "e1-heat-screw",
)

DUET2_MAESTRO_HEATER_RESOURCES = (
    (
        "bed-heater",
        "Bed heater",
        "bed-heat-molex",
        "bed-heat-screw",
    ),
    (
        "e0-heater",
        "E0 heater",
        "e0-heat-molex",
        "e0-heat-screw",
    ),
    (
        "e1-heater",
        "E1 heater",
        "e1-heat-molex",
        "e1-heat-screw",
    ),
)

DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS = {
    "bed-heat-molex": {
        "position_count": 2,
        "interface_type": "Molex-compatible heater output",
        "output_voltage": "VIN",
        "maximum_current": "2 A at 24 V",
        "mating_interface_family": (
            "Molex-compatible 2.54 mm"
        ),
        "mating_housing_part_number": None,
        "mating_contact_part_number": (
            "08-50-0114"
        ),
        "mating_part_number_status": (
            "Exact heater-output housing not independently "
            "verified; 2-way KK housing is a candidate."
        ),
    },
    "e0-heat-molex": {
        "position_count": 2,
        "interface_type": "Molex-compatible heater output",
        "output_voltage": "VIN",
        "maximum_current": "2 A at 24 V",
        "mating_interface_family": (
            "Molex-compatible 2.54 mm"
        ),
        "mating_housing_part_number": None,
        "mating_contact_part_number": (
            "08-50-0114"
        ),
        "mating_part_number_status": (
            "Exact heater-output housing not independently "
            "verified; 2-way KK housing is a candidate."
        ),
    },
    "e1-heat-molex": {
        "position_count": 2,
        "interface_type": "Molex-compatible heater output",
        "output_voltage": "VIN",
        "maximum_current": "2 A at 24 V",
        "mating_interface_family": (
            "Molex-compatible 2.54 mm"
        ),
        "mating_housing_part_number": None,
        "mating_contact_part_number": (
            "08-50-0114"
        ),
        "mating_part_number_status": (
            "Exact heater-output housing not independently "
            "verified; 2-way KK housing is a candidate."
        ),
    },
    "bed-heat-screw": {
        "position_count": 2,
        "interface_type": "2-position screw terminal",
        "output_voltage": "VIN",
        "maximum_current": "5 A at 24 V",
        "mating_interface_family": (
            "Direct wire-entry screw terminal"
        ),
        "mating_housing_part_number": None,
        "mating_contact_part_number": None,
        "mating_part_number_status": (
            "No separate mating housing; conductor is "
            "secured directly in the board terminal."
        ),
    },
    "e0-heat-screw": {
        "position_count": 2,
        "interface_type": "2-position screw terminal",
        "output_voltage": "VIN",
        "maximum_current": "5 A at 24 V",
        "mating_interface_family": (
            "Direct wire-entry screw terminal"
        ),
        "mating_housing_part_number": None,
        "mating_contact_part_number": None,
        "mating_part_number_status": (
            "No separate mating housing; conductor is "
            "secured directly in the board terminal."
        ),
    },
    "e1-heat-screw": {
        "position_count": 2,
        "interface_type": "2-position screw terminal",
        "output_voltage": "VIN",
        "maximum_current": "5 A at 24 V",
        "mating_interface_family": (
            "Direct wire-entry screw terminal"
        ),
        "mating_housing_part_number": None,
        "mating_contact_part_number": None,
        "mating_part_number_status": (
            "No separate mating housing; conductor is "
            "secured directly in the board terminal."
        ),
    },
}


DUET2_MAESTRO_ADDITIONAL_INTERFACE_SPECIFICATIONS = {
    "fan0": {
        "board_label": "FAN0",
        "position_count": 2,
        "interface_type": "2-position PWM-controlled fan output",
        "interface_role": "controlled_fan_output",
        "usage_classification": "machine_io",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
    },
    "fan1": {
        "board_label": "FAN1",
        "position_count": 2,
        "interface_type": "2-position PWM-controlled fan output",
        "interface_role": "controlled_fan_output",
        "usage_classification": "machine_io",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
    },
    "fan2": {
        "board_label": "FAN2",
        "position_count": 2,
        "interface_type": "2-position PWM-controlled fan output",
        "interface_role": "controlled_fan_output",
        "usage_classification": "machine_io",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
    },
    "always-on-fan": {
        "board_label": "Always on FAN 0",
        "position_count": 2,
        "interface_type": "2-position always-on fan connection",
        "interface_role": "always_on_fan_output",
        "usage_classification": "machine_io",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
    },
    "bed-temp": {
        "board_label": "BED TEMP",
        "position_count": 2,
        "interface_type": "2-position thermistor/PT1000 temperature input",
        "interface_role": "temperature_sensor_input",
        "usage_classification": "machine_io",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
    },
    "e0-temp": {
        "board_label": "E0 TEMP",
        "position_count": 2,
        "interface_type": "2-position thermistor/PT1000 temperature input",
        "interface_role": "temperature_sensor_input",
        "usage_classification": "machine_io",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
    },
    "e1-temp": {
        "board_label": "E1 TEMP",
        "position_count": 2,
        "interface_type": "2-position thermistor/PT1000 temperature input",
        "interface_role": "temperature_sensor_input",
        "usage_classification": "machine_io",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
    },
    "c-temp": {
        "board_label": "C Temp",
        "position_count": 2,
        "interface_type": "2-position thermistor/PT1000 temperature input",
        "interface_role": "temperature_sensor_input",
        "usage_classification": "machine_io",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "evidence_status": "Manufacturer schematic identifies C TEMP as THERMISTOR3.",
    },
    "z-probe": {
        "board_label": "Probe",
        "position_count": 5,
        "interface_type": "5-position probe interface",
        "interface_role": "z_probe_interface",
        "usage_classification": "machine_io",
        "unused_position_numbers": [3, 5],
        "used_position_count": 3,
        "evidence_source": DUET2_MAESTRO_PHYSICAL_INSPECTION_SOURCE,
    },
    "e2-driver": {
        "board_label": "E2",
        "position_count": 8,
        "interface_type": "8-position external stepper-driver module interface",
        "interface_role": "external_stepper_driver_module_interface",
        "usage_classification": "expansion_io",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
    },
    "e3-driver": {
        "board_label": "E3",
        "position_count": 8,
        "interface_type": "8-position external stepper-driver module interface",
        "interface_role": "external_stepper_driver_module_interface",
        "usage_classification": "expansion_io",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
    },
    "usdhc": {
        "board_reference": "J15",
        "board_label": "uSDHC",
        "position_count": 9,
        "interface_type": "9-contact micro-SD storage interface",
        "interface_role": "storage_service_interface",
        "usage_classification": "expansion_or_service",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "evidence_status": (
            "Manufacturer schematic identifies J15 / uSDHC and the "
            "nine-contact SD interface including the SD_CD net; actual "
            "firmware card-detect use is not established by current evidence."
        ),
    },
    "paneldue": {
        "board_reference": "J30",
        "board_label": "PanelDUE",
        "position_count": 4,
        "interface_type": "4-position display/serial interface",
        "interface_role": "panel_display_interface",
        "usage_classification": "user_interface",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
    },
    "paneldue-sd": {
        "board_reference": "P3",
        "board_label": "PanelDue_SD",
        "position_count": 10,
        "interface_type": "10-position PanelDue SD interface",
        "interface_role": "panel_display_storage_interface",
        "usage_classification": "user_interface",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
    },
    "12864-exp1": {
        "board_reference": "P2",
        "board_label": "12864 EXP1",
        "position_count": 10,
        "interface_type": "10-position IDC display expansion interface",
        "interface_role": "12864_display_expansion_interface",
        "usage_classification": "user_interface",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "pin_positions": {
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
        },
        "evidence_status": (
            "Manufacturer schematic identifies all ten P2 / 12864_EXP1 "
            "contact positions: 1 = BEEP, 2 = ENC_SW, "
            "3 = SPI0_MOSI_LCD_BUFF, 4 = LCD_CS_BUFF, "
            "5 = SPI0_SCK_LCD_BUFF, 6 = NC, 7 = NC, 8 = NC, "
            "9 = GND, 10 = +5V."
        ),
    },
    "12864-exp2": {
        "board_reference": "P1",
        "board_label": "12864 EXP2",
        "position_count": 10,
        "interface_type": "10-position IDC display expansion interface",
        "interface_role": "12864_display_expansion_interface",
        "usage_classification": "user_interface",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "pin_positions": {
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
        },
        "evidence_status": (
            "Manufacturer schematic identifies all ten P1 / 12864_EXP2 "
            "contact positions: 1 = SPI0_MISO_BUFF, 2 = SPI0_SCK_BUFF, "
            "3 = ENC_B, 4 = SPI0_CS0, 5 = ENC_A, 6 = SPI0_MOSI_BUFF, "
            "7 = NC, 8 = RESET_EXT, 9 = GND, 10 = NC."
        ),
    },
    "usb": {
        "board_reference": "J22",
        "board_label": "USB",
        "position_count": 5,
        "interface_type": "USB device/service connection",
        "interface_role": "usb_communication_interface",
        "usage_classification": "communication_service",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "evidence_status": (
            "Manufacturer schematic identifies J22 / USB Micro-B "
            "with D+, D-, VBUS, GND, and a no-connect ID contact."
        ),
    },
    "ethernet": {
        "board_reference": "J38",
        "board_label": "Ethernet",
        "position_count": 8,
        "interface_type": "Ethernet network connection",
        "interface_role": "ethernet_network_interface",
        "usage_classification": "communication_service",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "evidence_status": (
            "Manufacturer schematic identifies J38 as an RJ45 "
            "connector with integrated magnetics and Ethernet "
            "link/activity circuitry; physical contact-to-PHY "
            "numbering remains unresolved."
        ),
    },
    "c-gnd": {
        "board_reference": "J27",
        "board_label": "C_GND",
        "position_count": 1,
        "interface_type": "single-point ground connection",
        "interface_role": "ground_reference_connection",
        "usage_classification": "power_reference",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "evidence_status": (
            "Manufacturer schematic identifies J27 / C_GND as a "
            "single spade-terminal chassis/ground-bond feature."
        ),
    },
    "j21": {
        "board_label": "Expansion",
        "position_count": 13,
        "interface_type": "13-position expansion header",
        "interface_role": "auxiliary_header",
        "usage_classification": "expansion_or_service",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "evidence_status": "Manufacturer schematic identifies J21 as Expansion.",
    },
    "j4": {
        "board_label": "CONN4 / High Current Terminal",
        "position_count": 4,
        "interface_type": "4-position high-current power and bed-heater terminal",
        "interface_role": "high_current_power_and_bed_heater_interface",
        "usage_classification": "machine_io",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "evidence_status": "Manufacturer schematic identifies J4 as the high-current terminal with GND, V_IN, V_IN, and BED- contacts.",
    },
    "temp-ob": {
        "board_label": "TEMP_DB",
        "position_count": 10,
        "interface_type": "10-position temperature daughterboard/service interface",
        "interface_role": "auxiliary_header",
        "usage_classification": "expansion_or_service",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "evidence_status": "Manufacturer schematic identifies J37 / TEMP_DB and the complete ten-contact signal map.",
    },
    "j23": {
        "board_reference": "J23",
        "board_label": "5V V_FAN_B VIN",
        "position_count": 3,
        "interface_type": "3-position fan supply selection header",
        "interface_role": "fan_supply_selection",
        "usage_classification": "power_configuration",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "evidence_status": (
            "Manufacturer schematic identifies J23 and the three "
            "positions as +5V, V_FAN_B, and V_IN."
        ),
    },
    "erase": {
        "board_label": "ERASE",
        "position_count": 2,
        "interface_type": "2-position firmware erase service jumper",
        "interface_role": "firmware_erase_service_interface",
        "usage_classification": "service_configuration",
        "evidence_source": DUET2_MAESTRO_PHYSICAL_INSPECTION_SOURCE,
    },
    "a-vin": {
        "board_reference": "J3",
        "board_label": "A VIN",
        "position_count": 3,
        "interface_type": "3-position fan supply selection jumper",
        "interface_role": "fan_supply_selection",
        "usage_classification": "power_configuration",
        "evidence_source": DUET2_MAESTRO_PHYSICAL_INSPECTION_SOURCE,
    },
    "e-5v-en": {
        "board_label": "E 5V EN",
        "position_count": 2,
        "interface_type": "2-position 5V enable jumper",
        "interface_role": "five_volt_supply_enable",
        "usage_classification": "power_configuration",
        "evidence_source": DUET2_MAESTRO_PHYSICAL_INSPECTION_SOURCE,
    },
    "5v-ps": {
        "board_reference": "J20",
        "board_label": "5V PS",
        "position_count": 3,
        "interface_type": "3-position 5 V supply / PSU-control header",
        "interface_role": "five_volt_power_connection",
        "usage_classification": "power_configuration",
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "evidence_status": (
            "Manufacturer schematic identifies J20 / 5V_PS with "
            "position 1 = 5V_IN, position 2 = PS_ON_IN, and "
            "position 3 = GND."
        ),
    },
}


DUET2_MAESTRO_BOARD_FEATURES = {
    "test_ate": {
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "evidence_status": (
            "Manufacturer schematic identifies TP1-TP5 as 3-contact "
            "Step/Dir/UART ATE test-point arrays and TP6-TP14 plus "
            "TP16 as individual test points; all test points are DNP. "
            "There is no TP15."
        ),
        "point_count": 15,
        "physical_contact_count": 25,
        "all_test_points_dnp": True,
        "points": {
            "TP1": {
                "board_reference": "TP1",
                "board_label": "Z_Stp_Tp",
                "position_count": 3,
                "purpose": "ATE/test only",
                "pin_positions": {
                    "1": "Z_STEP",
                    "2": "Z_DIR",
                    "3": "Z_UART",
                },
            },
            "TP2": {
                "board_reference": "TP2",
                "board_label": "Y_Stp_Tp",
                "position_count": 3,
                "purpose": "ATE/test only",
                "pin_positions": {
                    "1": "Y_STEP",
                    "2": "Y_DIR",
                    "3": "Y_UART",
                },
            },
            "TP3": {
                "board_reference": "TP3",
                "board_label": "X_Stp_Tp",
                "position_count": 3,
                "purpose": "ATE/test only",
                "pin_positions": {
                    "1": "X_STEP",
                    "2": "X_DIR",
                    "3": "X_UART",
                },
            },
            "TP4": {
                "board_reference": "TP4",
                "board_label": "E0_Stp_Tp",
                "position_count": 3,
                "purpose": "ATE/test only",
                "pin_positions": {
                    "1": "E0_STEP",
                    "2": "E0_DIR",
                    "3": "E0_UART",
                },
            },
            "TP5": {
                "board_reference": "TP5",
                "board_label": "E1_Stp_Tp",
                "position_count": 3,
                "purpose": "ATE/test only",
                "pin_positions": {
                    "1": "E1_STEP",
                    "2": "E1_DIR",
                    "3": "E1_UART",
                },
            },
            "TP6": {
                "board_reference": "TP6",
                "purpose": "ATE/test point",
                "net": "HEATER0",
            },
            "TP7": {
                "board_reference": "TP7",
                "purpose": "ATE/test point",
                "net": "HEATER1",
            },
            "TP8": {
                "board_reference": "TP8",
                "purpose": "ATE/test point",
                "net": "HEATER2",
            },
            "TP9": {
                "board_reference": "TP9",
                "purpose": "ATE/test point",
                "net": "BED_PWM",
            },
            "TP10": {
                "board_reference": "TP10",
                "purpose": "ATE/test point",
                "net": "E0_PWM",
            },
            "TP11": {
                "board_reference": "TP11",
                "purpose": "ATE/test point",
                "net": "E1_PWM",
            },
            "TP12": {
                "board_reference": "TP12",
                "purpose": "ATE/test point",
                "net": "FAN0",
            },
            "TP13": {
                "board_reference": "TP13",
                "purpose": "ATE/test point",
                "net": "FAN1",
            },
            "TP14": {
                "board_reference": "TP14",
                "purpose": "ATE/test point",
                "net": "FAN2",
            },
            "TP16": {
                "board_reference": "TP16",
                "purpose": "ATE/test point",
                "net": "D6_TestPoint",
            },
        },
    },
    "board_indicators": {
        "evidence_source": DUET2_MAESTRO_HARDWARE_SOURCE,
        "evidence_status": (
            "Board indicators include USB and diagnostic LEDs, power "
            "rail LEDs, and heater LEDs identified by the board design "
            "and BOM evidence. D20 is explicitly identified as E1 Heat."
        ),
        "items": {
            "D3": {
                "board_reference": "D3",
                "board_label": "USB",
                "net": "VBUS",
                "classification": "board_status_observability",
                "purpose": "USB power presence",
            },
            "D4": {
                "board_reference": "D4",
                "board_label": "Diag",
                "classification": "board_status_observability",
                "purpose": "board indicator labelled Diag",
                "net": "SERVO",
                "series_resistance": "2.2 kΩ",
                "evidence_status": (
                    "Maestro V1.0 Processor.sch shows D4 labelled Diag "
                    "on the SERVO net, with R104 = 2.2 kΩ to GND; "
                    "Maestro-specific firmware diagnostic/status semantics "
                    "are not established."
                ),
            },
            "D6": {
                "board_reference": "D6",
                "board_label": "Bed Heat",
                "classification": "board_status_observability",
                "purpose": "bed heater activity indication",
            },
            "D7": {
                "board_reference": "D7",
                "board_label": "E0 Heat",
                "classification": "board_status_observability",
                "purpose": "E0 heater activity indication",
            },
            "D20": {
                "board_reference": "D20",
                "board_label": "E1 Heat",
                "classification": "board_status_observability",
                "purpose": "E1 heater activity indication",
            },
            "D15": {
                "board_reference": "D15",
                "board_label": "VIN",
                "net": "V_IN",
                "color": "blue",
                "classification": "board_status_observability",
                "purpose": "input power presence",
            },
            "D16": {
                "board_reference": "D16",
                "board_label": "3.3V",
                "net": "+3.3V",
                "color": "green",
                "classification": "board_status_observability",
                "purpose": "3.3 V rail presence",
            },
            "D17": {
                "board_reference": "D17",
                "board_label": "5V+",
                "net": "+5V",
                "color": "red",
                "classification": "board_status_observability",
                "purpose": "5 V rail presence",
            },
        },
        "integrated_interface_indicators": {
            "ethernet-j38": {
                "board_reference": "J38",
                "signals": [
                    "ACTLED",
                    "LINKLED",
                ],
                "classification": "communication_observability",
                "purpose": "Ethernet link/activity indication",
                "evidence_status": (
                    "Indicators are integrated into the Ethernet "
                    "RJ45/magnetics interface and are not separate "
                    "board connectors or ordinary SemanticPorts."
                ),
            },
        },
    },
    "alternate_heater_access": {
        "evidence_source": DUET2_MAESTRO_HEADERS_SOURCE,
        "evidence_status": (
            "Manufacturer schematic identifies J16 and J17 as "
            "two-position alternate access points associated with "
            "the E0 and E1 heater circuits. Production population "
            "of these design-level points is not verified."
        ),
        "items": {
            "J16": {
                "board_reference": "J16",
                "board_label": "E0 HEAT",
                "position_count": 2,
                "electrical_association": "E0 HEAT",
                "population_status": (
                    "Design-level; production population unverified."
                ),
            },
            "J17": {
                "board_reference": "J17",
                "board_label": "E1 HEAT",
                "position_count": 2,
                "electrical_association": "E1 HEAT",
                "population_status": (
                    "Design-level; production population unverified."
                ),
            },
        },
    },
    "service_controls": {
        "evidence_source": DUET2_MAESTRO_HARDWARE_SOURCE,
        "evidence_status": (
            "These are board-level service/configuration controls "
            "rather than ordinary machine-topology interfaces."
        ),
        "items": {
            "S1": {
                "board_reference": "S1",
                "board_label": "RESET",
                "classification": "service_control",
                "purpose": "board reset",
            },
            "JP1": {
                "board_reference": "JP1",
                "board_label": "ERASE",
                "classification": "service_configuration",
                "purpose": "erase/service configuration",
                "catalog_reference": "erase",
            },
            "JP9": {
                "board_reference": "JP9",
                "board_label": "I 5V EN",
                "classification": "power_configuration",
                "purpose": "5 V supply enable configuration",
            },
            "JP10": {
                "board_reference": "JP10",
                "board_label": "E 5V EN",
                "classification": "power_configuration",
                "purpose": "5 V supply enable configuration",
                "catalog_reference": "e-5v-en",
            },
        },
    },
}

def build_duet_2_maestro() -> HardwareDefinition:
    """Build the documented Duet 2 Maestro v1.0 hardware definition."""
    motor_connector_specifications = {
        connector_id: dict(
            DUET2_MAESTRO_MOTOR_CONNECTOR_SPEC
        )
        for connector_id
        in DUET2_MAESTRO_MOTOR_CONNECTOR_IDS
    }

    endstop_connector_specifications = {}

    for connector_id in (
        DUET2_MAESTRO_ENDSTOP_CONNECTOR_IDS
    ):
        signal_label = (
            DUET2_MAESTRO_ENDSTOP_SIGNAL_LABELS[
                connector_id
            ]
        )

        specification = dict(
            DUET2_MAESTRO_ENDSTOP_CONNECTOR_SPEC
        )

        specification["pin_positions"] = {
            "1": signal_label,
            "2": "+3.3 V",
            "3": "GND",
        }

        endstop_connector_specifications[
            connector_id
        ] = specification

    connector_specifications = (
        motor_connector_specifications
        | endstop_connector_specifications
        | {
            connector_id: dict(
                specification
            )
            for (
                connector_id,
                specification,
            ) in (
                DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS.items()
            )
        }
        | {
            interface_id: dict(
                specification
            )
            for (
                interface_id,
                specification,
            ) in (
                DUET2_MAESTRO_ADDITIONAL_INTERFACE_SPECIFICATIONS.items()
            )
        }
    )

    return HardwareDefinition(
        id="duet-2-maestro-v1-0",
        family="Duet 2 Maestro",
        manufacturer="Duet3D",
        variant="v1.0",
        properties={
            "processor": "ATSAM4S8C",
            "onboard_stepper_driver_count": 5,
            "onboard_stepper_driver_type": "TMC2224",
            "heater_output_count": 3,
            "controlled_fan_output_count": 3,
            "connector_specifications": connector_specifications,
            "board_features": DUET2_MAESTRO_BOARD_FEATURES,
        },
        provenance=[
            Provenance(
                source=DUET2_MAESTRO_HARDWARE_SOURCE,
                evidence_type="published",
                method="manufacturer hardware design repository",
                context="Duet 2 Maestro v1.0 hardware design files.",
            ),
            Provenance(
                source=DUET2_MAESTRO_HEADERS_SOURCE,
                evidence_type="published",
                method="manufacturer schematic",
                context=(
                    "Headers.sch documents the Maestro's physical "
                    "connector interfaces."
                ),
            ),
            Provenance(
                source=DUET2_MAESTRO_WIRING_SOURCE,
                evidence_type="published",
                method="manufacturer wiring documentation",
                context=(
                    "The Maestro wiring diagram identifies Molex "
                    "heater outputs rated 2 A at 24 V and screw "
                    "terminal heater outputs rated 5 A at 24 V."
                ),
            ),
            Provenance(
                source=(
                    "https://reprapltd.com/shop/duet-2-maestro/"
                ),
                evidence_type="published",
                method="product documentation",
                context=(
                    "The Duet 2 Maestro has three heater channels "
                    "and is supplied with Molex-compatible plugs "
                    "and crimps."
                ),
            ),
            Provenance(
                source=(
                    "https://github.com/Duet3D/wiki-content/"
                    "blob/master/User_manual/"
                    "Connecting_hardware/Motors_servos.md"
                ),
                evidence_type="published",
                method="manufacturer technical documentation",
                context=(
                    "Duet documentation describes heater outputs "
                    "as PWM-controlled outputs on the ground side."
                ),
            ),
        ],
    )
# ---------------------------------------------------------------------------
# BIGTREETECH TMC5160T V1.0
# ---------------------------------------------------------------------------

BTT_TMC5160T_HARDWARE_SOURCE = (
    "https://github.com/bigtreetech/docs/blob/master/docs/"
    "TMC5160T%20Pro%20V1.0.md"
)

BTT_TMC5160T_PIN_LABELS = {
    "J1": {
        1: "EN",
        2: "SDI/CFG1",
        3: "SCK/CFG2",
        4: "CSN/CFG3",
        5: "SDO/CFG0",
        6: "CLK",
        7: "STEP",
        8: "DIR",
    },
    "J2": {
        1: "VM",
        2: "GND",
        3: "A2",
        4: "A1",
        5: "B2",
        6: "B1",
        7: "VIO",
        8: "GND",
    },
}

BTT_TMC5160T_MODULE_INTERFACE_SPEC = {
    "interface_role": "16-contact plug-in driver module interface",
    "connector_count": 2,
    "connectors": {
        "J1": {
            "position_count": 8,
            "pin_labels": BTT_TMC5160T_PIN_LABELS["J1"],
        },
        "J2": {
            "position_count": 8,
            "pin_labels": BTT_TMC5160T_PIN_LABELS["J2"],
        },
    },
    "installation_note": (
        "Power must be off during installation. Orient the module correctly "
        "before insertion."
    ),
}


def build_btt_tmc5160t() -> HardwareDefinition:
    return HardwareDefinition(
        id="btt-tmc5160t-v1-0",
        family="TMC5160T",
        manufacturer="BIGTREETECH",
        variant="V1.0",
        properties={
            "driver_chip": "TMC5160-TA",
            "dimensions": "20.4 × 15.3 × 23.2 mm",
            "input_voltage": "8 V to 24 V",
            "maximum_current_rms": "3.1 A",
            "maximum_current_peak": "4.4 A",
            "base_capacity_max_a": 3.0,
            "maximum_microstepping": 256,
            "operating_mode": "SPI",
            "module_interface": BTT_TMC5160T_MODULE_INTERFACE_SPEC,
        },
        provenance=[
            Provenance(
                source=BTT_TMC5160T_HARDWARE_SOURCE,
            )
        ],
    )

# ---------------------------------------------------------------------------
# BIGTREETECH Octopus V1.1 MOTOR_DRIVER receiving-interface evidence
# ---------------------------------------------------------------------------

BTT_OCTOPUS_HARDWARE_SOURCE = (
    "https://github.com/bigtreetech/BIGTREETECH-OCTOPUS-V1.0"
)

BTT_OCTOPUS_DOCUMENTATION_SOURCE = (
    "https://github.com/bigtreetech/docs/blob/master/docs/Octopus.md"
)

BTT_OCTOPUS_MOTOR_DRIVER_RECEIVING_INTERFACE_SPEC = {
    "interface_type": "MOTOR_DRIVER",
    "interface_role": "driver_module_receiving_interface",
    "board_revision": "V1.1",
    "schematic_scope": "V1.0/V1.1",
    "contact_count": 18,
    "active_contact_count": 16,
    "contacts": {
        1: {"label": "EN", "classification": "active"},
        2: {"label": "SDI/MS0", "classification": "active"},
        3: {"label": "SCK/MS1", "classification": "active"},
        4: {"label": "CS/MS2", "classification": "active"},
        5: {"label": "SDO/RST", "classification": "active"},
        6: {"label": "SLEEP", "classification": "active"},
        7: {"label": "STEP", "classification": "active"},
        8: {"label": "DIR", "classification": "active"},
        9: {"label": "GND", "classification": "active"},
        10: {"label": "VCC_IO", "classification": "active"},
        11: {"label": "A1", "classification": "active"},
        12: {"label": "A2", "classification": "active"},
        13: {"label": "B2", "classification": "active"},
        14: {"label": "B1", "classification": "active"},
        15: {"label": "GND", "classification": "active"},
        16: {"label": "VM", "classification": "active"},
        17: {"label": "NC", "classification": "not_connected"},
        18: {"label": "DIAG", "classification": "diagnostic"},
    },
    "pin_6_discrepancy": {
        "octopus_contact": 6,
        "octopus_label": "SLEEP",
        "octopus_net_pattern": "DRIVERx_SLP",
        "tmc5160t_connector": "J1",
        "tmc5160t_contact": 6,
        "tmc5160t_label": "CLK",
        "tmc5160t_source": BTT_TMC5160T_HARDWARE_SOURCE,
        "mapped_as_equivalent": False,
        "equivalence_status": "unresolved",
        "spi_jumper_electrical_state": "unresolved",
    },
    "evidence_sources": (
        BTT_OCTOPUS_HARDWARE_SOURCE,
        BTT_OCTOPUS_DOCUMENTATION_SOURCE,
        BTT_TMC5160T_HARDWARE_SOURCE,
    ),
}
