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

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test machine",
        )
    )

    return model


def get_fixture():
    model = make_test_model()

    controller, ports = (
        add_duet_2_maestro_physical_interfaces(
            model,
            machine_id="machine-1",
        )
    )

    return model, controller, ports


def test_fixture_creates_installed_controller() -> None:
    _, controller, _ = get_fixture()

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
    _, controller, ports = get_fixture()

    assert len(ports) == 58

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
    _, _, ports = get_fixture()

    expected_counts = {
        "x-motor": 4,
        "z-a-motor": 4,
        "z-b-motor": 4,
        "bed-heat-molex": 2,
        "bed-heat-screw": 2,
        "e0-heat-molex": 2,
        "e0-heat-screw": 2,
        "e1-heat-molex": 2,
        "e1-heat-screw": 2,
        "bed-temp": 2,
        "e0-temp": 2,
        "e1-temp": 2,
        "c-temp": 2,
        "x-stop": 3,
        "y-stop": 3,
        "z-stop": 3,
        "e0-stop": 3,
        "e1-stop": 3,
        "z-probe": 5,
        "fan0": 2,
        "fan1": 2,
        "fan2": 2,
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
    _, _, ports = get_fixture()

    expected_counts = {
        "x-motor": 4,
        "z-a-motor": 4,
        "z-b-motor": 4,
        "bed-heat-molex": 2,
        "bed-heat-screw": 2,
        "e0-heat-molex": 2,
        "e0-heat-screw": 2,
        "e1-heat-molex": 2,
        "e1-heat-screw": 2,
        "bed-temp": 2,
        "e0-temp": 2,
        "e1-temp": 2,
        "c-temp": 2,
        "x-stop": 3,
        "y-stop": 3,
        "z-stop": 3,
        "e0-stop": 3,
        "e1-stop": 3,
        "z-probe": 5,
        "fan0": 2,
        "fan1": 2,
        "fan2": 2,
    }

    for connector_id, expected_count in (
        expected_counts.items()
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


def test_maestro_bed_temp_ports_have_temperature_input_role() -> None:
    _, _, ports = get_fixture()

    bed_temp_ports = [
        port
        for port in ports
        if port.connector_id == "bed-temp"
    ]

    assert len(bed_temp_ports) == 2
    assert all(port.direction == "input" for port in bed_temp_ports)
    assert all(
        port.properties["electrical_role"] == "temperature_sensor_input"
        for port in bed_temp_ports
    )

def test_maestro_e0_temp_ports_have_temperature_input_role() -> None:
    _, _, ports = get_fixture()

    e0_temp_ports = [
        port
        for port in ports
        if port.connector_id == "e0-temp"
    ]

    assert len(e0_temp_ports) == 2
    assert all(port.direction == "input" for port in e0_temp_ports)
    assert all(
        port.properties["electrical_role"] == "temperature_sensor_input"
        for port in e0_temp_ports
    )

def test_maestro_e1_temp_ports_have_temperature_input_role() -> None:
    _, _, ports = get_fixture()

    e1_temp_ports = [
        port
        for port in ports
        if port.connector_id == "e1-temp"
    ]

    assert len(e1_temp_ports) == 2
    assert all(port.direction == "input" for port in e1_temp_ports)
    assert all(
        port.properties["electrical_role"] == "temperature_sensor_input"
        for port in e1_temp_ports
    )


def test_maestro_c_temp_ports_have_temperature_input_role() -> None:
    _, _, ports = get_fixture()

    c_temp_ports = [
        port
        for port in ports
        if port.connector_id == "c-temp"
    ]

    assert len(c_temp_ports) == 2
    assert all(port.direction == "input" for port in c_temp_ports)
    assert all(
        port.properties["electrical_role"] == "temperature_sensor_input"
        for port in c_temp_ports
    )


def test_maestro_fan_ports_have_controlled_output_roles() -> None:
    _, _, ports = get_fixture()

    fan_ports = [
        port
        for port in ports
        if port.connector_id in {"fan0", "fan1", "fan2"}
    ]

    assert len(fan_ports) == 6
    assert all(port.direction == "output" for port in fan_ports)
    assert all(
        port.properties["electrical_role"] == "controlled_fan_output"
        for port in fan_ports
    )

def test_z_a_and_z_b_are_separate_connector_groups() -> None:
    _, _, ports = get_fixture()

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


def test_endstop_connector_pins_have_verified_roles() -> None:
    _, _, ports = get_fixture()

    expected = {
        "x-stop": (
            "xstop",
            "+3.3V",
            "GND",
        ),
        "y-stop": (
            "ystop",
            "+3.3V",
            "GND",
        ),
        "z-stop": (
            "zstop",
            "+3.3V",
            "GND",
        ),
        "e0-stop": (
            "e0stop",
            "+3.3V",
            "GND",
        ),
        "e1-stop": (
            "e1stop",
            "+3.3V",
            "GND",
        ),
    }

    for connector_id, pin_labels in (
        expected.items()
    ):
        connector_ports = [
            port
            for port in ports
            if port.connector_id == connector_id
        ]

        assert [
            port.properties["pin_label"]
            for port in connector_ports
        ] == list(pin_labels)


def test_heater_connector_groups_are_present() -> None:
    _, _, ports = get_fixture()

    expected_groups = {
        "bed-heat-molex",
        "bed-heat-screw",
        "e0-heat-molex",
        "e0-heat-screw",
        "e1-heat-molex",
        "e1-heat-screw",
    }

    actual_groups = {
        port.connector_id
        for port in ports
        if port.connector_id in expected_groups
    }

    assert actual_groups == expected_groups


def test_heater_ports_have_verified_output_information() -> None:
    _, _, ports = get_fixture()

    heater_ports = [
        port
        for port in ports
        if port.connector_id
        in {
            "bed-heat-molex",
            "bed-heat-screw",
            "e0-heat-molex",
            "e0-heat-screw",
            "e1-heat-molex",
            "e1-heat-screw",
        }
    ]

    assert len(heater_ports) == 12

    assert all(
        port.direction == "output"
        for port in heater_ports
    )

    assert all(
        port.properties[
            "electrical_role"
        ] == "heater_output"
        for port in heater_ports
    )


def test_z_stepper_resource_is_exposed_through_z_a_and_z_b() -> None:
    model, controller, ports = get_fixture()

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


def test_heater_resources_are_exposed_through_molex_and_screw_interfaces() -> None:
    model, controller, ports = get_fixture()

    expected = {
        "bed-heater": {
            "bed-heat-molex",
            "bed-heat-screw",
        },
        "e0-heater": {
            "e0-heat-molex",
            "e0-heat-screw",
        },
        "e1-heater": {
            "e1-heat-molex",
            "e1-heat-screw",
        },
    }

    for resource_suffix, connector_ids in (
        expected.items()
    ):
        resource_id = (
            f"{controller.id}-{resource_suffix}"
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

        assert len(relationships) == 4

        assert {
            model.ports[
                relationship.target_id
            ].connector_id
            for relationship
            in relationships
        } == connector_ids


def test_fixture_does_not_create_controller_resource_assignment() -> None:
    model, _, _ = get_fixture()

    assert (
        model.controller_resource_assignments
        == {}
    )

    assert len(
        model.controller_resources
    ) == 4


def test_removing_z_stepper_resource_removes_exposure_relationships() -> None:
    model, controller, _ = get_fixture()

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