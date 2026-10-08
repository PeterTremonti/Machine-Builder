"""Tests for verified Duet 2 Maestro heater interfaces."""

from machine_builder.controller_board_fixtures import (
    add_duet_2_maestro_physical_interfaces,
)
from machine_builder.hardware_catalog import (
    DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS,
    DUET2_MAESTRO_HEATER_RESOURCES,
    build_duet_2_maestro,
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


def test_maestro_heater_connector_specifications_are_present() -> None:
    hardware = build_duet_2_maestro()

    specifications = hardware.properties[
        "connector_specifications"
    ]

    assert set(
        DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS
    ) <= set(specifications)

    for connector_id, expected in (
        DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS.items()
    ):
        specification = specifications[
            connector_id
        ]

        assert specification == expected
        assert (
            specification["position_count"]
            == 2
        )


def test_maestro_heater_interfaces_have_two_access_types() -> None:
    model = make_test_model()

    _, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            machine_id="machine-1",
        )
    )

    for (
        resource_suffix,
        _,
        molex_connector_id,
        screw_connector_id,
    ) in DUET2_MAESTRO_HEATER_RESOURCES:
        expected_connector_ids = {
            molex_connector_id,
            screw_connector_id,
        }

        expected_exposed_connector_ids = (
            expected_connector_ids | {"j4"}
            if resource_suffix == "bed-heater"
            else expected_connector_ids
        )

        connector_ids = {
            port.connector_id
            for port in ports
            if port.connector_id
            in expected_connector_ids
        }

        assert connector_ids == (
            expected_connector_ids
        )

        assert sum(
            1
            for port in ports
            if port.connector_id
            in expected_connector_ids
        ) == 4

        resource_id = (
            f"duet-2-maestro-v1-0-controller"
            f"-{resource_suffix}"
        )

        exposed_relationships = [
            relationship
            for relationship
            in model.relationships.values()
            if (
                relationship.source_id
                == resource_id
                and relationship.relationship_type
                == "exposed_through"
            )
        ]

        expected_relationship_count = (
            5
            if resource_suffix == "bed-heater"
            else 4
        )

        assert len(
            exposed_relationships
        ) == expected_relationship_count

        assert {
            model.ports[
                relationship.target_id
            ].connector_id
            for relationship
            in exposed_relationships
        } == expected_exposed_connector_ids


def test_heater_ports_are_output_interfaces() -> None:
    model = make_test_model()

    _, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            machine_id="machine-1",
        )
    )

    heater_ports = [
        port
        for port in ports
        if port.connector_id
        in DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS
    ]

    assert len(
        heater_ports
    ) == 12

    assert all(
        port.direction == "output"
        for port in heater_ports
    )

    assert all(
        port.properties["electrical_role"]
        == "heater_output"
        for port in heater_ports
    )


def test_heater_molex_and_screw_outputs_have_different_ratings() -> None:
    assert (
        DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS[
            "bed-heat-molex"
        ]["maximum_current"]
        == "2 A at 24 V"
    )

    assert (
        DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS[
            "bed-heat-screw"
        ]["maximum_current"]
        == "5 A at 24 V"
    )