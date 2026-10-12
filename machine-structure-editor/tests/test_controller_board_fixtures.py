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

    assert len(ports) == 111

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
        "y-motor": 4,
        "e0-motor": 4,
        "e1-motor": 4,
        "z-a-motor": 4,
        "z-b-motor": 4,
        "j4": 4,
        "temp-ob": 10,
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
        "always-on-fan": 2,
        "j21": 13,
        "e2-driver": 8,
        "e3-driver": 8,
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
        "y-motor": 4,
        "e0-motor": 4,
        "e1-motor": 4,
        "z-a-motor": 4,
        "j4": 4,
        "temp-ob": 10,
        "z-b-motor": 4,
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
        "always-on-fan": 2,
        "j21": 13,
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


def test_y_motor_ports_have_maestro_motor_labels() -> None:
    _, _, ports = get_fixture()

    y_ports = {
        port.pin_id: port
        for port in ports
        if port.connector_id == "y-motor"
    }

    assert set(y_ports) == {"1", "2", "3", "4"}

    expected_labels = ["B1", "B2", "A1", "A2"]

    assert [
        y_ports[str(position)].properties["pin_label"]
        for position in range(1, 5)
    ] == expected_labels

    assert all(
        port.direction == "unknown"
        for port in y_ports.values()
    )

    for position, pin_label in zip(
        range(1, 5),
        expected_labels,
    ):
        assert (
            y_ports[str(position)].purpose
            == f"Stepper motor coil {pin_label} terminal"
        )


def test_e0_motor_ports_have_maestro_motor_labels() -> None:
    _, _, ports = get_fixture()

    e0_ports = {
        port.pin_id: port
        for port in ports
        if port.connector_id == "e0-motor"
    }

    assert set(e0_ports) == {"1", "2", "3", "4"}

    expected_labels = ["B1", "B2", "A1", "A2"]

    assert [
        e0_ports[str(position)].properties["pin_label"]
        for position in range(1, 5)
    ] == expected_labels

    assert all(
        port.direction == "unknown"
        for port in e0_ports.values()
    )

    for position, pin_label in zip(
        range(1, 5),
        expected_labels,
    ):
        assert (
            e0_ports[str(position)].purpose
            == f"Stepper motor coil {pin_label} terminal"
        )

def test_e1_motor_ports_have_maestro_motor_labels() -> None:
    _, _, ports = get_fixture()

    e1_ports = {
        port.pin_id: port
        for port in ports
        if port.connector_id == "e1-motor"
    }

    assert set(e1_ports) == {"1", "2", "3", "4"}

    expected_labels = ["B1", "B2", "A1", "A2"]

    assert [
        e1_ports[str(position)].properties["pin_label"]
        for position in range(1, 5)
    ] == expected_labels

    assert all(
        port.direction == "unknown"
        for port in e1_ports.values()
    )

    for position, pin_label in zip(
        range(1, 5),
        expected_labels,
    ):
        assert (
            e1_ports[str(position)].purpose
            == f"Stepper motor coil {pin_label} terminal"
        )


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


def test_maestro_z_probe_ports_have_position_specific_roles() -> None:
    _, _, ports = get_fixture()

    z_probe_ports = {
        port.pin_id: port
        for port in ports
        if port.connector_id == "z-probe"
    }

    assert set(z_probe_ports) == {"1", "2", "3", "4", "5"}

    expected = {
        "1": ("Z_PROBE_IN", "input", "z_probe_signal_input"),
        "2": ("GND", "unknown", "ground_reference"),
        "3": ("Z_PROBE_MOD", "output", "z_probe_mod_output"),
        "4": ("+3.3V", "unknown", "power_supply_3v3"),
        "5": ("+5V", "unknown", "power_supply_5v"),
    }

    for position, (pin_label, direction, electrical_role) in expected.items():
        port = z_probe_ports[position]
        assert port.properties["pin_label"] == pin_label
        assert port.direction == direction
        assert port.properties["electrical_role"] == electrical_role


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

def test_maestro_always_on_fan_ports_have_verified_pin_mappings() -> None:
    _, _, ports = get_fixture()

    always_on_fan_ports = [
        port
        for port in ports
        if port.connector_id == "always-on-fan"
    ]

    assert len(always_on_fan_ports) == 2

    expected = {
        "1": ("GND", "Ground reference", "unknown", "ground_reference"),
        "2": (
            "V_FAN_A",
            "Always-on fan supply output",
            "output",
            "always_on_fan_output",
        ),
    }

    assert {port.pin_id for port in always_on_fan_ports} == set(expected)

    for port in always_on_fan_ports:
        pin_label, purpose, direction, electrical_role = expected[port.pin_id]

        assert port.properties["pin_label"] == pin_label
        assert port.purpose == purpose
        assert port.direction == direction
        assert port.properties["electrical_role"] == electrical_role

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
    assert not {
        "bed-heat-molex",
        "bed-heat-screw",
    } & {port.connector_id for port in ports}


def test_heater_ports_have_verified_output_information() -> None:
    _, _, ports = get_fixture()

    heater_ports = [
        port
        for port in ports
        if port.connector_id
        in {
            "e0-heat-molex",
            "e0-heat-screw",
            "e1-heat-molex",
            "e1-heat-screw",
        }
    ]

    assert len(heater_ports) == 8

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


def test_maestro_j21_expansion_ports_have_verified_pin_mappings() -> None:
    _, _, ports = get_fixture()

    j21_ports = {
        port.pin_id: port
        for port in ports
        if port.connector_id == "j21"
    }

    expected = {
        "1": ("+5V", "5 V supply", "unknown", "power_supply_5v"),
        "2": ("GND", "Ground reference", "unknown", "ground_reference"),
        "3": ("RESET", "Board reset signal", "unknown", None),
        "4": ("EXP_0", "Expansion general-purpose signal", "unknown", None),
        "5": ("EXP_1", "Expansion general-purpose signal", "unknown", None),
        "6": ("ADVREF", "Analog reference signal", "unknown", None),
        "7": ("VSSA", "Analog ground reference", "unknown", "analog_ground_reference"),
        "8": ("TWCK0", "I2C clock signal", "unknown", None),
        "9": ("TWD0", "I2C data signal", "unknown", None),
        "10": ("+3.3V", "3.3 V supply", "unknown", "power_supply_3v3"),
        "11": ("SERVO", "Servo control output", "output", "servo_control_output"),
        "12": ("+5V", "5 V supply", "unknown", "power_supply_5v"),
        "13": ("GND", "Ground reference", "unknown", "ground_reference"),
    }

    assert set(j21_ports) == set(expected)

    for position, (pin_label, purpose, direction, electrical_role) in expected.items():
        port = j21_ports[position]
        assert port.properties["pin_label"] == pin_label
        assert port.purpose == purpose
        assert port.direction == direction
        assert port.properties.get("electrical_role") == electrical_role


def test_maestro_j37_temp_db_ports_have_verified_pin_mappings() -> None:
    _, _, ports = get_fixture()

    j37_ports = {
        port.pin_id: port
        for port in ports
        if port.connector_id == "temp-ob"
    }

    expected = {
        "1": ("SPI0_CS2", "SPI chip-select signal", "unknown", None),
        "2": ("GND", "Ground reference", "unknown", "ground_reference"),
        "3": ("SPI0_CS1", "SPI chip-select signal", "unknown", None),
        "4": ("SPI0_SCK", "SPI clock signal", "unknown", None),
        "5": ("SPI0_MOSI", "SPI data output signal", "unknown", None),
        "6": ("SPI0_MISO", "SPI data input signal", "unknown", None),
        "7": ("TWCK0", "I2C clock signal", "unknown", None),
        "8": ("+3.3V", "3.3 V supply", "unknown", "power_supply_3v3"),
        "9": ("TWD0", "I2C data signal", "unknown", None),
        "10": ("NC", "No connect", "unknown", None),
    }

    assert set(j37_ports) == set(expected)

    for position, (pin_label, purpose, direction, electrical_role) in expected.items():
        port = j37_ports[position]

        assert port.properties["pin_label"] == pin_label
        assert port.purpose == purpose
        assert port.direction == direction

        if electrical_role is None:
            assert "electrical_role" not in port.properties
        else:
            assert port.properties["electrical_role"] == electrical_role

def test_maestro_j4_high_current_ports_have_verified_pin_mappings() -> None:
    _, _, ports = get_fixture()

    j4_ports = {
        port.pin_id: port
        for port in ports
        if port.connector_id == "j4"
    }

    expected = {
        "1": ("GND", "Ground reference", "unknown", "ground_reference"),
        "2": ("V_IN", "Board power input", "unknown", None),
        "3": ("V_IN", "Bed heater supply", "unknown", None),
        "4": ("BED-", "Bed heater output return", "output", "heater_output"),
    }

    assert set(j4_ports) == set(expected)
    assert j4_ports["2"].id != j4_ports["3"].id

    for position, (pin_label, purpose, direction, electrical_role) in expected.items():
        port = j4_ports[position]
        assert port.properties["pin_label"] == pin_label
        assert port.purpose == purpose
        assert port.direction == direction

        if electrical_role is None:
            assert "electrical_role" not in port.properties
        else:
            assert port.properties["electrical_role"] == electrical_role


def test_j4_bed_heater_resource_is_exposed_through_bed_supply_and_return_only() -> None:
    model, controller, _ = get_fixture()

    resource_id = f"{controller.id}-bed-heater"
    relationships = [
        relationship
        for relationship in model.relationships.values()
        if (
            relationship.source_id == resource_id
            and relationship.relationship_type == "exposed_through"
        )
    ]

    targets = {relationship.target_id for relationship in relationships}
    assert len(relationships) == 2
    assert targets == {
        f"{controller.id}-j4-pin-3",
        f"{controller.id}-j4-pin-4",
    }
    assert not targets.intersection({
        f"{controller.id}-j4-pin-1",
        f"{controller.id}-j4-pin-2",
    })

def test_maestro_external_driver_ports_have_verified_pin_mappings() -> None:
    _, _, ports = get_fixture()

    expected = {
        "e2-driver": {
            "1": ("V_IN", "unknown", None),
            "2": ("GND", "unknown", "ground_reference"),
            "3": ("E2_UART", "unknown", None),
            "4": ("E2_EN", "output", None),
            "5": ("E2_STEP", "output", None),
            "6": ("E2_DIR", "output", None),
            "7": ("GND", "unknown", "ground_reference"),
            "8": ("+3.3V", "unknown", "power_supply_3v3"),
        },
        "e3-driver": {
            "1": ("V_IN", "unknown", None),
            "2": ("GND", "unknown", "ground_reference"),
            "3": ("E3_UART", "unknown", None),
            "4": ("E3_EN", "output", None),
            "5": ("E3_STEP", "output", None),
            "6": ("E3_DIR", "output", None),
            "7": ("GND", "unknown", "ground_reference"),
            "8": ("+3.3V", "unknown", "power_supply_3v3"),
        },
    }

    for connector_id, expected_pins in expected.items():
        driver_ports = {
            port.pin_id: port
            for port in ports
            if port.connector_id == connector_id
        }

        assert set(driver_ports) == set(expected_pins)
        assert driver_ports["2"].id != driver_ports["7"].id

        for position, (pin_label, direction, electrical_role) in expected_pins.items():
            port = driver_ports[position]
            assert port.properties["pin_label"] == pin_label
            assert port.direction == direction
            assert port.properties.get("electrical_role") == electrical_role

def test_external_stepper_resources_are_exposed_through_e2_and_e3() -> None:
    model, controller, ports = get_fixture()

    expected = {
        "e2-stepper": "e2-driver",
        "e3-stepper": "e3-driver",
    }

    for resource_suffix, connector_id in expected.items():
        resource_id = f"{controller.id}-{resource_suffix}"
        resource = model.controller_resources[resource_id]

        assert resource.resource_type == "stepper"

        relationships = [
            relationship
            for relationship in model.relationships.values()
            if relationship.source_id == resource_id
            and relationship.relationship_type == "exposed_through"
        ]

        expected_ports = {
            port.id
            for port in ports
            if port.connector_id == connector_id
        }

        assert len(relationships) == 8
        assert {relationship.target_id for relationship in relationships} == expected_ports

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


def test_heater_resources_are_exposed_through_j4_and_e0_e1_interfaces() -> None:
    model, controller, ports = get_fixture()

    expected = {
        "bed-heater": {"j4"},
        "e0-heater": {
            "e0-heat-molex",
            "e0-heat-screw",
        },
        "e1-heater": {
            "e1-heat-molex",
            "e1-heat-screw",
        },
    }

    expected_relationship_counts = {
        "bed-heater": 2,
        "e0-heater": 4,
        "e1-heater": 4,
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

        assert len(relationships) == (
            expected_relationship_counts[resource_suffix]
        )

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
    ) == 6


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


def test_maestro_pcb_pad_identity_metadata_matches_pinned_manual_crosswalk() -> None:
    """Compare against a manually reviewed expected crosswalk, not a parsed external PCB."""
    _, _, ports = get_fixture()
    ports_by_key = {(port.connector_id, port.pin_id): port for port in ports}

    source_commit = "56958640c73c7febf3bce6e1eefbbdffd5a2db1b"
    # Backward-compatible pcb_source_revision stores the repository commit.
    source_revision = source_commit
    source_file = "Duet2/Duet2Maestro_v1.0/Duet2Maestro.kicad_pcb"
    source_url = (
        "https://raw.githubusercontent.com/Duet3D/Duet-2-Hardware/"
        f"{source_commit}/{source_file}"
    )
    guide_url = (
        "https://promega.printm3d.com/documentation/electronics/"
        "duet-maestro-wiring"
    )

    # These expectations are manually reviewed against the pinned KiCad source.
    # The test validates fixture metadata and does not parse that external source.
    # Each sequence is in legacy fixture ordinal order, not PCB pad order.
    expected = {
        "x-motor": ("J9", [(3, "X_MOT_B1"), (4, "X_MOT_B2"), (1, "X_MOT_A1"), (2, "X_MOT_A2")]),
        "y-motor": ("J8", [(3, "Y_MOT_B1"), (4, "Y_MOT_B2"), (1, "Y_MOT_A1"), (2, "Y_MOT_A2")]),
        "z-a-motor": ("J36", [(3, "Z_MOT_B1"), (4, "Net-(J36-Pad4)"), (1, "Z_MOT_A1"), (2, "Net-(J36-Pad2)")]),
        "z-b-motor": ("J7", [(3, "Net-(J36-Pad4)"), (4, "Z_MOT_B2"), (1, "Net-(J36-Pad2)"), (2, "Z_MOT_A2")]),
        "x-stop": ("J33", [(3, "X_STOP_CONN"), (2, "+3.3V"), (1, "GND")]),
        "y-stop": ("J32", [(3, "Y_STOP_CONN"), (2, "+3.3V"), (1, "GND")]),
        "z-probe": ("J28", [(5, "Z_PROBE_IN"), (4, "GND"), (3, "Z_PROBE_MOD"), (2, "+3.3V"), (1, "+5V")]),
        "temp-ob": ("J37", [(1, "SPI0_CS2"), (2, "GND"), (3, "SPI0_CS1"), (4, "SPI0_SCK"), (5, "SPI0_MOSI"), (6, "SPI0_MISO"), (7, "TWCK0"), (8, "+3.3V"), (9, "TWD0"), (10, None)]),
    }

    for connector_id, (reference, contacts) in expected.items():
        for position, (pad_number, net_name) in enumerate(contacts, start=1):
            port = ports_by_key[(connector_id, str(position))]
            properties = port.properties

            assert port.pin_id == str(position)
            assert port.id.endswith(f"-pin-{position}")
            assert properties["pcb_identity_inventory_status"] == (
                "covered_by_reviewed_pcb_identity_inventory"
            )
            assert properties["pcb_reference_designator"] == reference
            assert properties["pcb_pad_number"] == pad_number
            assert properties["pcb_net_name"] == net_name
            assert properties["pcb_net_status"] == (
                "unassigned_in_reference_pcb"
                if net_name is None
                else "named_net_assigned_in_reference_pcb"
            )
            assert properties["pcb_source_url"] == source_url
            assert properties["pcb_source_commit"] == source_commit
            assert properties["pcb_source_revision"] == source_revision
            assert properties["pcb_source_file"] == source_file
            assert properties["pcb_board_revision"] == "V1.0"
            assert properties["pcb_source_date"] == "2018-02-20"
            assert len(port.provenance) == 1

            evidence = port.provenance[0]
            assert evidence.source == source_url
            assert evidence.evidence_type == "published"
            assert evidence.method == (
                "manual crosswalk review against pinned "
                "manufacturer KiCad PCB source"
            )
            assert reference in (evidence.context or "")
            assert f"pad {pad_number}" in (evidence.context or "")
            assert source_revision in (evidence.context or "")
            assert "V1.0" in (evidence.context or "")
            assert "2018-02-20" in (evidence.context or "")
            assert "not automatically parse" in (evidence.notes or "")
            assert "mating-face/cavity positions are not inferred" in (
                evidence.notes or ""
            )

            # Coordinate identities stay separate and explicitly source-qualified.
            assert "connector_position" not in properties
            assert "pcb_front_view_location" not in properties
            assert "cable_cavity_position" not in properties

            if connector_id == "z-probe":
                guide_positions = {
                    "Z_PROBE_IN": 1,
                    "GND": 2,
                    "Z_PROBE_MOD": 3,
                    "+3.3V": 4,
                    "+5V": 5,
                }
                assert properties["promega_diagram_view_position"] == (
                    guide_positions[properties["pin_label"]]
                )
                assert properties["promega_diagram_view_source"] == guide_url
            else:
                assert "promega_diagram_view_position" not in properties
                assert "promega_diagram_view_source" not in properties

    # E0/E1 motor pad identity is outside this authorized slice.
    for connector_id in ("e0-motor", "e1-motor"):
        excluded_ports = [
            port for port in ports
            if port.connector_id == connector_id
        ]
        assert len(excluded_ports) == 4
        assert all(
            "pcb_pad_number" not in port.properties
            for port in excluded_ports
        )
    # Every fixture port is explicitly classified for this bounded inventory.
    # Being outside the inventory does not establish its PCB net state.
    mapped_fixture_keys = {
        (connector_id, str(position))
        for connector_id, (_, contacts) in expected.items()
        for position, _ in enumerate(contacts, start=1)
    }
    outside_inventory = [
        port for port in ports
        if (port.connector_id, port.pin_id) not in mapped_fixture_keys
    ]
    assert outside_inventory
    assert len(mapped_fixture_keys) + len(outside_inventory) == len(ports)
    assert all(
        port.properties["pcb_identity_inventory_status"]
        == "outside_reviewed_pcb_identity_inventory"
        for port in outside_inventory
    )
    assert all(
        "pcb_source_url" not in port.properties
        and "pcb_net_status" not in port.properties
        for port in outside_inventory
    )

    expected_labels = {
        "x-motor": ("B1", "B2", "A1", "A2"),
        "y-motor": ("B1", "B2", "A1", "A2"),
        "z-a-motor": ("B1", "B2", "A1", "A2"),
        "z-b-motor": ("B1", "B2", "A1", "A2"),
        "x-stop": ("xstop", "+3.3V", "GND"),
        "y-stop": ("ystop", "+3.3V", "GND"),
        "z-probe": ("Z_PROBE_IN", "GND", "Z_PROBE_MOD", "+3.3V", "+5V"),
    }
    for connector_id, labels in expected_labels.items():
        for position, label in enumerate(labels, start=1):
            port = ports_by_key[(connector_id, str(position))]
            assert port.properties["pin_label"] == label
