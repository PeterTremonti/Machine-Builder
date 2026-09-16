"""Reusable hardware definitions for the Machine Structure Editor.

This module contains concrete hardware definitions that can be associated
with machine components.
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