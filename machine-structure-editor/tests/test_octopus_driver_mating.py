"""Tests for the Octopus driver-module mating experiment."""

from machine_builder.controller_board_fixtures import (
    add_octopus_tmc5160t_mating_experiment,
)
from machine_builder.hardware_catalog import (
    BTT_OCTOPUS_DOCUMENTATION_SOURCE,
    BTT_OCTOPUS_HARDWARE_SOURCE,
    BTT_OCTOPUS_MOTOR_DRIVER_RECEIVING_INTERFACE_SPEC,
    BTT_TMC5160T_HARDWARE_SOURCE,
    build_btt_tmc5160t,
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


def test_tmc5160t_hardware_definition_contains_verified_module_information() -> None:
    hardware = build_btt_tmc5160t()

    assert hardware.id == (
        "btt-tmc5160t-v1-0"
    )

    assert hardware.family == "TMC5160T"
    assert hardware.manufacturer == (
        "BIGTREETECH"
    )

    assert hardware.variant == "V1.0"

    assert hardware.properties[
        "driver_chip"
    ] == "TMC5160-TA"

    assert hardware.properties[
        "dimensions"
    ] == "20.4 × 15.3 × 23.2 mm"

    assert hardware.properties[
        "input_voltage"
    ] == "8 V to 24 V"

    assert hardware.properties[
        "maximum_current_rms"
    ] == "3.1 A"

    assert hardware.properties[
        "maximum_current_peak"
    ] == "4.4 A"

    assert hardware.properties[
        "maximum_microstepping"
    ] == 256

    assert hardware.properties[
        "operating_mode"
    ] == "SPI"

    assert hardware.properties[
        "module_interface"
    ]["connector_count"] == 2

    assert hardware.provenance[0].source == (
        BTT_TMC5160T_HARDWARE_SOURCE
    )


def test_octopus_mating_uses_existing_semantic_port_endpoints() -> None:
    model = make_test_model()

    (
        controller,
        module,
        socket_port,
        module_port,
    ) = add_octopus_tmc5160t_mating_experiment(
        model,
        machine_id="machine-1",
    )

    assert module.hardware_definition_id == (
        "btt-tmc5160t-v1-0"
    )

    assert socket_port.controller_id == (
        controller.id
    )

    assert socket_port.component_id is None

    assert module_port.component_id == (
        module.id
    )

    assert module_port.controller_id is None

    assert socket_port.pin_id is None
    assert module_port.pin_id is None


def test_octopus_receiving_interface_evidence_is_explicit() -> None:
    model = make_test_model()

    (
        _,
        _,
        socket_port,
        _,
    ) = add_octopus_tmc5160t_mating_experiment(
        model,
        machine_id="machine-1",
    )

    spec = socket_port.properties[
        "interface_spec"
    ]

    assert spec == (
        BTT_OCTOPUS_MOTOR_DRIVER_RECEIVING_INTERFACE_SPEC
    )
    assert spec["interface_type"] == "MOTOR_DRIVER"
    assert spec["interface_role"] == (
        "driver_module_receiving_interface"
    )
    assert spec["board_revision"] == "V1.1"
    assert spec["schematic_scope"] == "V1.0/V1.1"
    assert spec["contact_count"] == 18
    assert spec["active_contact_count"] == 16

    for contact in range(1, 17):
        assert spec["contacts"][contact][
            "classification"
        ] == "active"

    assert spec["contacts"][17] == {
        "label": "NC",
        "classification": "not_connected",
    }

    assert spec["contacts"][18] == {
        "label": "DIAG",
        "classification": "diagnostic",
    }

    assert socket_port.properties[
        "driver_position"
    ] == {
        "driver_number": 2,
        "module_position": "M3",
        "motor_outputs": (
            "MOTOR2_1",
            "MOTOR2_2",
        ),
    }

    assert socket_port.properties[
        "contact_6_net"
    ] == "DRIVER2_SLP"

    provenance_sources = {
        provenance.source
        for provenance
        in socket_port.provenance
    }

    assert BTT_OCTOPUS_HARDWARE_SOURCE in (
        provenance_sources
    )
    assert BTT_OCTOPUS_DOCUMENTATION_SOURCE in (
        provenance_sources
    )
    assert BTT_TMC5160T_HARDWARE_SOURCE in (
        provenance_sources
    )


def test_octopus_tmc5160t_pin_6_discrepancy_is_preserved() -> None:
    spec = (
        BTT_OCTOPUS_MOTOR_DRIVER_RECEIVING_INTERFACE_SPEC
    )

    discrepancy = spec[
        "pin_6_discrepancy"
    ]

    assert discrepancy["octopus_contact"] == 6
    assert discrepancy["octopus_label"] == "SLEEP"
    assert discrepancy["octopus_net_pattern"] == (
        "DRIVERx_SLP"
    )

    assert discrepancy["tmc5160t_connector"] == "J1"
    assert discrepancy["tmc5160t_contact"] == 6
    assert discrepancy["tmc5160t_label"] == "CLK"
    assert discrepancy["mapped_as_equivalent"] is False
    assert discrepancy["equivalence_status"] == (
        "unresolved"
    )
    assert discrepancy["spi_jumper_electrical_state"] == (
        "unresolved"
    )

def test_tmc5160t_module_interface_is_interface_level() -> None:
    model = make_test_model()

    (
        _,
        _,
        _,
        module_port,
    ) = add_octopus_tmc5160t_mating_experiment(
        model,
        machine_id="machine-1",
    )

    assert module_port.properties[
        "interface_role"
    ] == "driver_module_mating_interface"

    assert module_port.properties[
        "contact_count"
    ] == 16


def test_octopus_mating_relationship_is_interface_level() -> None:
    model = make_test_model()

    (
        controller,
        module,
        socket_port,
        module_port,
    ) = add_octopus_tmc5160t_mating_experiment(
        model,
        machine_id="machine-1",
    )

    relationships = [
        relationship
        for relationship
        in model.relationships.values()
        if relationship.relationship_type
        == "mated_with"
    ]

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source_id == (
        socket_port.id
    )

    assert relationship.target_id == (
        module_port.id
    )

    assert relationship.is_type(
        "mated_with"
    )

    assert model.ports[
        relationship.source_id
    ].controller_id == controller.id

    assert model.ports[
        relationship.target_id
    ].component_id == module.id


def test_octopus_mating_is_not_exposed_through() -> None:
    model = make_test_model()

    add_octopus_tmc5160t_mating_experiment(
        model,
        machine_id="machine-1",
    )

    mating_relationships = [
        relationship
        for relationship
        in model.relationships.values()
        if relationship.relationship_type
        == "mated_with"
    ]

    exposure_relationships = [
        relationship
        for relationship
        in model.relationships.values()
        if relationship.relationship_type
        == "exposed_through"
    ]

    assert len(
        mating_relationships
    ) == 1

    assert exposure_relationships == []


def test_removing_driver_module_removes_mating_relationship() -> None:
    model = make_test_model()

    (
        _,
        module,
        socket_port,
        module_port,
    ) = add_octopus_tmc5160t_mating_experiment(
        model,
        machine_id="machine-1",
    )

    relationship_id = (
        f"{socket_port.id}"
        "-mated-with-"
        f"{module_port.id}"
    )

    assert relationship_id in (
        model.relationships
    )

    model.remove_component(
        module.id
    )

    assert relationship_id not in (
        model.relationships
    )

    assert module_port.id not in (
        model.ports
    )

    assert socket_port.id in (
        model.ports
    )