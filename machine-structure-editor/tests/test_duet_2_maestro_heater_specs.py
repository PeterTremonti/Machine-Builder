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

    assert set(DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS) == {
        "e0-heat-molex",
        "e0-heat-screw",
        "e1-heat-molex",
        "e1-heat-screw",
    }
    assert not {
        "bed-heat-molex",
        "bed-heat-screw",
    }.intersection(specifications)

    for connector_id, expected in (
        DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS.items()
    ):
        specification = specifications[connector_id]
        assert specification == expected
        assert specification["position_count"] == 2


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

        expected_exposed_connector_ids = expected_connector_ids

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

        expected_relationship_count = 4

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
    ) == 8

    assert all(
        port.direction == "output"
        for port in heater_ports
    )

    assert all(
        port.properties["electrical_role"]
        == "heater_output"
        for port in heater_ports
    )


def test_heater_ratings_and_bed_capability_evidence_are_scoped_correctly() -> None:
    hardware = build_duet_2_maestro()
    specifications = hardware.properties["connector_specifications"]

    assert "bed-heat-molex" not in specifications
    assert "bed-heat-screw" not in specifications
    assert "maximum_current" not in specifications["j4"]

    for connector_id in ("e0-heat-molex", "e1-heat-molex"):
        assert specifications[connector_id]["maximum_current"] == "2 A at 24 V"

    for connector_id in ("e0-heat-screw", "e1-heat-screw"):
        assert specifications[connector_id]["maximum_current"] == "5 A at 24 V"

    bed_capability_contexts = [
        item.context
        for item in hardware.provenance
        if "Duet_2_Maestro.md" in item.source
    ]
    assert bed_capability_contexts
    bed_context = "\n".join(bed_capability_contexts)
    assert "up to 18 A" in bed_context
    assert "subject to thermal testing" in bed_context
    assert "25 A maximum" in bed_context
    assert "not a J4" in bed_context
    assert "thermal-test results" in bed_context

    wiring_contexts = [
        item.context
        for item in hardware.provenance
        if "Wiring_your_Duet_2" in item.source
    ]
    assert any(
        "2 A at 24 V" in context
        and "5 A at 24 V" in context
        and "do not establish a verified current limit for J4" in context
        for context in wiring_contexts
    )
