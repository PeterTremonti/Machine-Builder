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
            "connector_specifications": (
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
            ),
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