"""Reusable hardware definitions for the Machine Structure Editor.

This module contains concrete hardware definitions that can be associated
with machine components.

The first entry is the user's real 24 V generic/unbranded 4010 fan.
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
    """Build the user's real generic/unbranded 24 V 4010 fan definition.

    The returned ports are initially associated with a placeholder component
    ID. The caller must replace that component ID with the actual
    MachineComponent ID before adding the ports to the canonical model.
    """

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
            id=(
                "generic-4010-fan-24v-power"
            ),
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
            id=(
                "generic-4010-fan-24v-ground"
            ),
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