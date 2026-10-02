"""Tests for concrete controller-board fixtures."""

from machine_builder.controller_board_fixtures import (
    add_duet_2_maestro_physical_interfaces,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
)


def make_test_model() -> CanonicalMachineModel:
    model = CanonicalMachineModel()

    machine = Machine(
        id="machine-1",
        name="Test machine",
    )

    model.add_machine(
        machine
    )

    return model


def test_fixture_creates_installed_controller() -> None:
    model = make_test_model()

    controller, _ = (
        add_duet_2_maestro_physical_interfaces(
            model,
            machine_id="machine-1",
        )
    )

    assert controller.id == (
        "duet-2-maestro-v1-0-controller"
    )

    assert controller.hardware_definition_id == (
        "duet-2-maestro-v1-0"
    )

    assert controller.controller_type == (
        "motion_controller"
    )

    assert controller.version == "v1.0"


def test_fixture_creates_controller_owned_physical_ports() -> None:
    model = make_test_model()

    controller, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            machine_id="machine-1",
        )
    )

    assert len(ports) == 26

    assert all(
        port.component_id is None
        for port in ports
    )

    assert all(
        port.controller_id == controller.id
        for port in ports
    )

    assert controller.port_ids == [
        port.id
        for port in ports
    ]


def test_fixture_connector_group_sizes() -> None:
    model = make_test_model()

    _, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            machine_id="machine-1",
        )
    )

    expected_counts = {
        "x-motor": 4,
        "z-a-motor": 4,
        "z-b-motor": 4,
        "heater": 2,
        "thermistor": 2,
        "endstop": 3,
        "z-probe": 5,
        "fan": 2,
    }

    actual_counts: dict[str, int] = {}

    for port in ports:
        assert port.connector_id is not None

        actual_counts[port.connector_id] = (
            actual_counts.get(
                port.connector_id,
                0,
            )
            + 1
        )

    assert actual_counts == expected_counts


def test_fixture_connector_positions_are_numbered() -> None:
    model = make_test_model()

    _, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            machine_id="machine-1",
        )
    )

    for connector_id, expected_count in (
        (
            "x-motor",
            4,
        ),
        (
            "z-a-motor",
            4,
        ),
        (
            "z-b-motor",
            4,
        ),
        (
            "heater",
            2,
        ),
        (
            "thermistor",
            2,
        ),
        (
            "endstop",
            3,
        ),
        (
            "z-probe",
            5,
        ),
        (
            "fan",
            2,
        ),
    ):
        positions = {
            port.pin_id
            for port in ports
            if port.connector_id == connector_id
        }

        assert positions == {
            str(position)
            for position in range(
                1,
                expected_count + 1,
            )
        }


def test_z_a_and_z_b_are_separate_connector_groups() -> None:
    model = make_test_model()

    _, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            machine_id="machine-1",
        )
    )

    z_a_ids = {
        port.id
        for port in ports
        if port.connector_id == "z-a-motor"
    }

    z_b_ids = {
        port.id
        for port in ports
        if port.connector_id == "z-b-motor"
    }

    assert len(z_a_ids) == 4
    assert len(z_b_ids) == 4
    assert z_a_ids.isdisjoint(
        z_b_ids
    )


def test_fixture_creates_z_stepper_resource() -> None:
    model = make_test_model()

    controller, _ = (
        add_duet_2_maestro_physical_interfaces(
            model,
            machine_id="machine-1",
        )
    )

    resource_id = (
        f"{controller.id}-z-stepper"
    )

    resource = model.controller_resources[
        resource_id
    ]

    assert resource.name == (
        "Z stepper driver"
    )

    assert resource.resource_type == (
        "stepper"
    )

    assert resource.controller_id == (
        controller.id
    )


def test_z_stepper_resource_is_exposed_through_z_a_and_z_b() -> None:
    model = make_test_model()

    controller, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            machine_id="machine-1",
        )
    )

    resource_id = (
        f"{controller.id}-z-stepper"
    )

    relationships = [
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

    expected_ports = {
        port.id
        for port in ports
        if port.connector_id
        in {
            "z-a-motor",
            "z-b-motor",
        }
    }

    assert len(relationships) == 8

    assert {
        relationship.target_id
        for relationship in relationships
    } == expected_ports

    assert {
        model.ports[
            relationship.target_id
        ].connector_id
        for relationship
        in relationships
    } == {
        "z-a-motor",
        "z-b-motor",
    }


def test_fixture_does_not_create_controller_resource_assignment() -> None:
    model = make_test_model()

    add_duet_2_maestro_physical_interfaces(
        model,
        machine_id="machine-1",
    )

    assert (
        model.controller_resource_assignments
        == {}
    )

    assert len(
        model.controller_resources
    ) == 1


def test_removing_z_stepper_resource_removes_exposure_relationships() -> None:
    model = make_test_model()

    controller, _ = (
        add_duet_2_maestro_physical_interfaces(
            model,
            machine_id="machine-1",
        )
    )

    resource_id = (
        f"{controller.id}-z-stepper"
    )

    assert any(
        relationship.source_id
        == resource_id
        for relationship
        in model.relationships.values()
    )

    model.remove_controller_resource(
        resource_id
    )

    assert not any(
        relationship.source_id
        == resource_id
        or relationship.target_id
        == resource_id
        for relationship
        in model.relationships.values()
    )