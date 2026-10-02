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

DUET2_MAESTRO_ENDSTOP_DOC_SOURCE = (
    "https://docs.duet3d.com/User_manual/Tuning/Triggers"
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
                    "Headers.sch identifies the five X/Y/Z/E0/E1 "
                    "endstop connectors as 3-position headers and "
                    "shows their signal, +3.3 V, and GND connections."
                ),
            ),
            Provenance(
                source=(
                    "https://forum.duet3d.com/topic/22167/"
                    "nema-14-don-t-work-with-duet-wifi-drivers"
                ),
                evidence_type="published",
                method="manufacturer support forum",
                context=(
                    "Duet3D administrator identifies the Duet 2 Maestro "
                    "motor connector convention as B1, B2, A1, A2."
                ),
            ),
            Provenance(
                source=(
                    "https://reprapltd.com/documentation/"
                    "fisher-build-instructions/troubleshooting/"
                ),
                evidence_type="published",
                method="technical documentation",
                context=(
                    "RepRap Ltd identifies the Duet wiring crimps as "
                    "standard Molex KK 2.54 mm crimps."
                ),
            ),
            Provenance(
                source=DUET2_MAESTRO_ENDSTOP_DOC_SOURCE,
                evidence_type="published",
                method="manufacturer technical documentation",
                context=(
                    "Duet documentation describes Duet 2 endstop "
                    "connections using the endstop signal and GND, "
                    "and identifies Molex KK as the connector family."
                ),
            ),
            Provenance(
                source=(
                    "https://www.connecticc.com/mol22-01-3037.html"
                ),
                evidence_type="published",
                method="component distributor catalog",
                context=(
                    "Molex 22-01-3037 is a 3-circuit KK 254 "
                    "crimp housing."
                ),
            ),
            Provenance(
                source=(
                    "https://www.connecticc.com/mol08-50-0114.html"
                ),
                evidence_type="published",
                method="component distributor catalog",
                context=(
                    "Molex 08-50-0114 is a KK 254 crimp terminal "
                    "used with the mating housing."
                ),
            ),
        ],
    )