"""Tests for the canonical semantic machine model."""

from machine_builder.semantic_model import (
    CanonicalMachineModel,
    HardwareDefinition,
    Machine,
    MachineComponent,
    Provenance,
    SemanticPort,
)


def test_machine_can_be_added_to_model() -> None:
    model = CanonicalMachineModel()

    machine = Machine(
        id="machine-1",
        name="Test Printer",
    )

    model.add_machine(
        machine
    )

    assert model.machines["machine-1"] is machine
    assert machine.component_ids == []


def test_machine_component_can_be_added_to_machine() -> None:
    model = CanonicalMachineModel()

    machine = Machine(
        id="machine-1",
        name="Test Printer",
    )

    model.add_machine(
        machine
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
        label="Part Cooling Fan",
    )

    model.add_component(
        "machine-1",
        component,
    )

    assert model.components["component-1"] is component
    assert machine.component_ids == [
        "component-1"
    ]


def test_component_can_exist_without_hardware_definition() -> None:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Printer",
        )
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
    )

    model.add_component(
        "machine-1",
        component,
    )

    assert (
        component.hardware_definition_id
        is None
    )


def test_hardware_definition_can_be_assigned_to_component() -> None:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Printer",
        )
    )

    hardware = HardwareDefinition(
        id="hardware-1",
        family="4010 axial fan",
        manufacturer="Generic / Unbranded",
        variant="24 V",
    )

    model.add_hardware_definition(
        hardware
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
        hardware_definition_id="hardware-1",
    )

    model.add_component(
        "machine-1",
        component,
    )

    assert (
        component.hardware_definition_id
        == "hardware-1"
    )


def test_component_can_have_semantic_ports() -> None:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Printer",
        )
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
    )

    model.add_component(
        "machine-1",
        component,
    )

    power = SemanticPort(
        id="port-power",
        component_id="component-1",
        purpose="Power",
        direction="input",
    )

    ground = SemanticPort(
        id="port-ground",
        component_id="component-1",
        purpose="Ground",
        direction="unknown",
    )

    model.add_port(
        power
    )

    model.add_port(
        ground
    )

    assert component.port_ids == [
        "port-power",
        "port-ground",
    ]

    assert (
        model.get_port("port-power")
        is power
    )

    assert (
        model.get_port("port-ground")
        is ground
    )


def test_provenance_is_retained() -> None:
    provenance = Provenance(
        source="AliExpress listing",
        evidence_type="published",
        method="seller description",
        context="Generic 4010 fan listing",
    )

    hardware = HardwareDefinition(
        id="hardware-1",
        family="4010 axial fan",
        manufacturer="Generic / Unbranded",
        variant="24 V",
        properties={
            "voltage": "24 V DC",
        },
        provenance=[
            provenance
        ],
    )

    assert (
        hardware.provenance[0]
        is provenance
    )

    assert (
        hardware.provenance[0].source
        == "AliExpress listing"
    )

    assert (
        hardware.provenance[0].method
        == "seller description"
    )


def test_hardware_definition_properties_can_preserve_multiple_claims() -> None:
    hardware = HardwareDefinition(
        id="hardware-1",
        family="4010 axial fan",
        manufacturer="Generic / Unbranded",
        variant="24 V",
        properties={
            "speed_claims": [
                {
                    "value": "8000 RPM",
                    "source": "listing description",
                },
                {
                    "value": "6200 ±10% RPM",
                    "source": "listing specification",
                },
            ],
        },
    )

    claims = hardware.properties[
        "speed_claims"
    ]

    assert len(claims) == 2
    assert claims[0]["value"] == "8000 RPM"
    assert (
        claims[1]["value"]
        == "6200 ±10% RPM"
    )


def test_unknown_connector_details_can_remain_unspecified() -> None:
    port = SemanticPort(
        id="port-power",
        component_id="component-1",
        purpose="Power",
        direction="input",
        connector_id=None,
        pin_id=None,
    )

    assert port.connector_id is None
    assert port.pin_id is None


def test_duplicate_machine_is_rejected() -> None:
    model = CanonicalMachineModel()

    machine = Machine(
        id="machine-1",
        name="Test Printer",
    )

    model.add_machine(
        machine
    )

    try:
        model.add_machine(
            Machine(
                id="machine-1",
                name="Another Printer",
            )
        )
    except ValueError as exc:
        assert (
            "Machine already exists"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected duplicate machine to be rejected"
        )


def test_component_with_unknown_machine_is_rejected() -> None:
    model = CanonicalMachineModel()

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
    )

    try:
        model.add_component(
            "missing-machine",
            component,
        )
    except ValueError as exc:
        assert (
            "Unknown machine"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected unknown machine to be rejected"
        )


def test_component_with_unknown_hardware_definition_is_rejected() -> None:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Printer",
        )
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
        hardware_definition_id="missing-hardware",
    )

    try:
        model.add_component(
            "machine-1",
            component,
        )
    except ValueError as exc:
        assert (
            "Unknown hardware definition"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected unknown hardware definition "
            "to be rejected"
        )


def test_port_with_unknown_component_is_rejected() -> None:
    model = CanonicalMachineModel()

    port = SemanticPort(
        id="port-1",
        component_id="missing-component",
        purpose="Power",
    )

    try:
        model.add_port(
            port
        )
    except ValueError as exc:
        assert (
            "Unknown component"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected unknown component to be rejected"
        )


def test_duplicate_component_is_rejected() -> None:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Printer",
        )
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
    )

    model.add_component(
        "machine-1",
        component,
    )

    try:
        model.add_component(
            "machine-1",
            MachineComponent(
                id="component-1",
                role="Heater",
            ),
        )
    except ValueError as exc:
        assert (
            "Machine component already exists"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected duplicate component to be rejected"
        )


def test_duplicate_port_is_rejected() -> None:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Printer",
        )
    )

    model.add_component(
        "machine-1",
        MachineComponent(
            id="component-1",
            role="Part Cooling Fan",
        ),
    )

    model.add_port(
        SemanticPort(
            id="port-1",
            component_id="component-1",
            purpose="Power",
        )
    )

    try:
        model.add_port(
            SemanticPort(
                id="port-1",
                component_id="component-1",
                purpose="Ground",
            )
        )
    except ValueError as exc:
        assert (
            "Port already exists"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected duplicate port to be rejected"
        )