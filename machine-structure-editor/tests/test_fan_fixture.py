"""Real-hardware fixture for the 24 V generic 4010 fan."""

from machine_builder.semantic_model import (
    CanonicalMachineModel,
    HardwareDefinition,
    Machine,
    MachineComponent,
    Provenance,
    SemanticPort,
)


FAN_LISTING_URL = (
    "https://www.aliexpress.us/item/"
    "3256805820145702.html"
)


def build_real_4010_24v_fan() -> (
    tuple[
        CanonicalMachineModel,
        Machine,
        MachineComponent,
        HardwareDefinition,
        SemanticPort,
        SemanticPort,
    ]
):
    """Build the canonical representation of the physical 24 V fan."""

    model = CanonicalMachineModel()

    machine = Machine(
        id="test-machine",
        name="Test Machine",
    )

    model.add_machine(
        machine
    )

    seller_description_provenance = Provenance(
        source=FAN_LISTING_URL,
        evidence_type="published",
        method="seller listing",
        context="AliExpress product description",
    )

    seller_variant_provenance = Provenance(
        source="user",
        evidence_type="authored",
        method="physical purchase",
        context=(
            "User purchased the 24 V version of the listed fan "
            "for a 24 V printer."
        ),
    )

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
                "Listing does not identify which speed claim "
                "corresponds to the 12 V or 24 V version."
            ),
        },
        provenance=[
            seller_description_provenance,
            seller_variant_provenance,
        ],
    )

    model.add_hardware_definition(
        hardware
    )

    component = MachineComponent(
        id="part-cooling-fan-1",
        role="Part Cooling Fan",
        label="Part Cooling Fan",
        hardware_definition_id=hardware.id,
        properties={
            "installed_voltage": "24 V DC",
        },
        provenance=[
            Provenance(
                source="user",
                evidence_type="authored",
                method="physical inspection / ownership",
                context=(
                    "Physical fan owned by the user and "
                    "selected as the first V0.2 hardware test part."
                ),
            )
        ],
    )

    model.add_component(
        machine.id,
        component,
    )

    power_port = SemanticPort(
        id="part-cooling-fan-1-power",
        component_id=component.id,
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
                    "Two-terminal 24 V DC fan; exact connector "
                    "pin identity is not yet documented."
                ),
            )
        ],
    )

    ground_port = SemanticPort(
        id="part-cooling-fan-1-ground",
        component_id=component.id,
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
                    "Two-terminal 24 V DC fan; exact connector "
                    "pin identity is not yet documented."
                ),
            )
        ],
    )

    model.add_port(
        power_port
    )

    model.add_port(
        ground_port
    )

    return (
        model,
        machine,
        component,
        hardware,
        power_port,
        ground_port,
    )


def test_real_fan_is_a_24v_generic_4010_fan() -> None:
    (
        model,
        machine,
        component,
        hardware,
        power_port,
        ground_port,
    ) = build_real_4010_24v_fan()

    assert model.machines[
        machine.id
    ] is machine

    assert component.role == "Part Cooling Fan"

    assert hardware.manufacturer == (
        "Generic / Unbranded"
    )

    assert hardware.family == (
        "4010 axial fan"
    )

    assert hardware.variant == "24 V"

    assert component.hardware_definition_id == (
        hardware.id
    )

    assert component.port_ids == [
        power_port.id,
        ground_port.id,
    ]


def test_real_fan_preserves_known_physical_properties() -> None:
    (
        _model,
        _machine,
        _component,
        hardware,
        _power_port,
        _ground_port,
    ) = build_real_4010_24v_fan()

    assert hardware.properties[
        "dimensions"
    ] == "40 × 40 × 10 mm"

    assert hardware.properties[
        "voltage"
    ] == "24 V DC"

    assert hardware.properties[
        "working_current"
    ] == "0.12 A"

    assert hardware.properties[
        "bearing"
    ] == "Oil"

    assert hardware.properties[
        "noise"
    ] == "22 dBA"

    assert hardware.properties[
        "cable_length"
    ] == "300 mm"


def test_real_fan_preserves_speed_claims_without_assigning_them_to_variants() -> None:
    (
        _model,
        _machine,
        _component,
        hardware,
        _power_port,
        _ground_port,
    ) = build_real_4010_24v_fan()

    claims = hardware.properties[
        "speed_claims"
    ]

    assert len(claims) == 2

    assert claims[0][
        "value"
    ] == "8000 RPM"

    assert claims[1][
        "value"
    ] == "6200 ±10% RPM"

    assert claims[0][
        "variant"
    ] is None

    assert claims[1][
        "variant"
    ] is None

    assert hardware.properties[
        "speed_variant_assignment"
    ] is None


def test_real_fan_preserves_unknown_connector_details() -> None:
    (
        _model,
        _machine,
        _component,
        hardware,
        power_port,
        ground_port,
    ) = build_real_4010_24v_fan()

    assert hardware.properties[
        "connector_description"
    ] == "2 Terminal Connector with 2pin-PH2.5"

    assert hardware.properties[
        "connector_series"
    ] is None

    assert hardware.properties[
        "connector_pin_details"
    ] is None

    assert power_port.connector_id is None
    assert power_port.pin_id is None

    assert ground_port.connector_id is None
    assert ground_port.pin_id is None


def test_real_fan_has_exactly_two_electrical_ports() -> None:
    (
        _model,
        _machine,
        component,
        _hardware,
        power_port,
        ground_port,
    ) = build_real_4010_24v_fan()

    assert len(
        component.port_ids
    ) == 2

    assert power_port.purpose == "Power"
    assert ground_port.purpose == "Ground"


def test_real_fan_records_user_selected_24v_variant_provenance() -> None:
    (
        _model,
        _machine,
        _component,
        hardware,
        _power_port,
        _ground_port,
    ) = build_real_4010_24v_fan()

    user_sources = [
        provenance
        for provenance in hardware.provenance
        if provenance.source == "user"
    ]

    assert len(
        user_sources
    ) == 1

    assert user_sources[0].method == (
        "physical purchase"
    )