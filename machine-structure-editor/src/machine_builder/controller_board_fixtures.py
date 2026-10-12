"""Concrete controller-board fixtures for Machine Builder."""

from __future__ import annotations

from .controller_resource import ControllerResource
from .hardware_catalog import (
    BTT_OCTOPUS_BOARD_REVISION_EVIDENCE,
    BTT_OCTOPUS_DOCUMENTATION_SOURCE,
    BTT_OCTOPUS_HARDWARE_SOURCE,
    BTT_OCTOPUS_MOTOR_DRIVER_RECEIVING_INTERFACE_SPEC,
    BTT_OCTOPUS_PINOUT_SOURCE,
    BTT_TMC5160T_HARDWARE_SOURCE,
    DUET2_MAESTRO_ENDSTOP_CONNECTOR_IDS,
    DUET2_MAESTRO_ENDSTOP_SIGNAL_LABELS,
    DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS,
    DUET2_MAESTRO_HEATER_RESOURCES,
    DUET2_MAESTRO_MOTOR_CONNECTOR_IDS,
    DUET2_MAESTRO_MOTOR_PIN_LABELS,
    build_btt_tmc5160t,
    build_duet_2_maestro,
)
from .semantic_model import (
    CanonicalMachineModel,
    Controller,
    MachineComponent,
    Provenance,
    SemanticPort,
)
from .semantic_relationship import SemanticRelationship


DUET_2_MAESTRO_CONNECTOR_LAYOUT = (
    ("x-motor", "X motor", 4),
    ("y-motor", "Y motor", 4),
    ("e0-motor", "E0 motor", 4),
    ("e1-motor", "E1 motor", 4),
    ("z-a-motor", "Z A motor", 4),
    ("z-b-motor", "Z B motor", 4),
    ("j4", "High Current Terminal", 4),
    ("temp-ob", "TEMP_DB", 10),
    ("e0-heat-molex", "E0 heat Molex", 2),
    ("e0-heat-screw", "E0 heat screw terminal", 2),
    ("e1-heat-molex", "E1 heat Molex", 2),
    ("e1-heat-screw", "E1 heat screw terminal", 2),
    ("bed-temp", "Bed temp", 2),
    ("e0-temp", "E0 temp", 2),
    ("e1-temp", "E1 temp", 2),
    ("c-temp", "C temp", 2),
    ("x-stop", "X stop", 3),
    ("y-stop", "Y stop", 3),
    ("z-stop", "Z stop", 3),
    ("e0-stop", "E0 stop", 3),
    ("e1-stop", "E1 stop", 3),
    ("z-probe", "Z probe", 5),
    ("fan0", "Fan 0", 2),
    ("fan1", "Fan 1", 2),
    ("fan2", "Fan 2", 2),
    ("always-on-fan", "Always-on fan", 2),
    ("j21", "Expansion", 13),
    ("e2-driver", "E2 external stepper driver", 8),
    ("e3-driver", "E3 external stepper driver", 8),
)


# Repository commit identity is distinct from PCB title-block revision/date.
DUET2_MAESTRO_PCB_SOURCE_COMMIT = (
    "56958640c73c7febf3bce6e1eefbbdffd5a2db1b"
)
# Compatibility alias: the legacy source_revision field contains this commit SHA.
DUET2_MAESTRO_PCB_SOURCE_REVISION = DUET2_MAESTRO_PCB_SOURCE_COMMIT
DUET2_MAESTRO_PCB_SOURCE_FILE = (
    "Duet2/Duet2Maestro_v1.0/Duet2Maestro.kicad_pcb"
)
DUET2_MAESTRO_PCB_BOARD_REVISION = "V1.0"
DUET2_MAESTRO_PCB_SOURCE_DATE = "2018-02-20"
DUET2_MAESTRO_PCB_SOURCE_URL = (
    "https://raw.githubusercontent.com/Duet3D/Duet-2-Hardware/"
    f"{DUET2_MAESTRO_PCB_SOURCE_COMMIT}/"
    f"{DUET2_MAESTRO_PCB_SOURCE_FILE}"
)
DUET2_MAESTRO_PCB_NET_STATUS_ASSIGNED = (
    "named_net_assigned_in_reference_pcb"
)
DUET2_MAESTRO_PCB_NET_STATUS_UNASSIGNED = (
    "unassigned_in_reference_pcb"
)
DUET2_MAESTRO_PCB_NET_STATUS_UNKNOWN = "unknown_or_uninspected"
# Each entry explicitly maps the existing fixture ordinal to a PCB pad.
# The ordinal and legacy pin_label do not independently establish pad identity.
DUET2_MAESTRO_PCB_PAD_MAP: dict[
    str, dict[int, tuple[str, int, str | None]]
] = {
    "x-motor": {
        1: ("J9", 3, "X_MOT_B1"),
        2: ("J9", 4, "X_MOT_B2"),
        3: ("J9", 1, "X_MOT_A1"),
        4: ("J9", 2, "X_MOT_A2"),
    },
    "y-motor": {
        1: ("J8", 3, "Y_MOT_B1"),
        2: ("J8", 4, "Y_MOT_B2"),
        3: ("J8", 1, "Y_MOT_A1"),
        4: ("J8", 2, "Y_MOT_A2"),
    },
    "z-a-motor": {
        1: ("J36", 3, "Z_MOT_B1"),
        2: ("J36", 4, "Net-(J36-Pad4)"),
        3: ("J36", 1, "Z_MOT_A1"),
        4: ("J36", 2, "Net-(J36-Pad2)"),
    },
    "z-b-motor": {
        1: ("J7", 3, "Net-(J36-Pad4)"),
        2: ("J7", 4, "Z_MOT_B2"),
        3: ("J7", 1, "Net-(J36-Pad2)"),
        4: ("J7", 2, "Z_MOT_A2"),
    },
    "x-stop": {
        1: ("J33", 3, "X_STOP_CONN"),
        2: ("J33", 2, "+3.3V"),
        3: ("J33", 1, "GND"),
    },
    "y-stop": {
        1: ("J32", 3, "Y_STOP_CONN"),
        2: ("J32", 2, "+3.3V"),
        3: ("J32", 1, "GND"),
    },
    "z-probe": {
        1: ("J28", 5, "Z_PROBE_IN"),
        2: ("J28", 4, "GND"),
        3: ("J28", 3, "Z_PROBE_MOD"),
        4: ("J28", 2, "+3.3V"),
        5: ("J28", 1, "+5V"),
    },
    "temp-ob": {
        1: ("J37", 1, "SPI0_CS2"),
        2: ("J37", 2, "GND"),
        3: ("J37", 3, "SPI0_CS1"),
        4: ("J37", 4, "SPI0_SCK"),
        5: ("J37", 5, "SPI0_MOSI"),
        6: ("J37", 6, "SPI0_MISO"),
        7: ("J37", 7, "TWCK0"),
        8: ("J37", 8, "+3.3V"),
        9: ("J37", 9, "TWD0"),
        10: ("J37", 10, None),
    },
}

DUET2_MAESTRO_PROMEGA_GUIDE_VIEW_SOURCE = (
    "https://promega.printm3d.com/documentation/electronics/"
    "duet-maestro-wiring"
)
DUET2_MAESTRO_PROMEGA_GUIDE_VIEW_POSITIONS = {
    "Z_PROBE_IN": 1,
    "GND": 2,
    "Z_PROBE_MOD": 3,
    "+3.3V": 4,
    "+5V": 5,
}


def add_duet_2_maestro_physical_interfaces(
    model: CanonicalMachineModel,
    machine_id: str,
    controller_id: str = "duet-2-maestro-v1-0-controller",
    label: str = "Duet 2 Maestro",
) -> tuple[Controller, tuple[SemanticPort, ...]]:
    """Add a representative installed Duet 2 Maestro and its physical interfaces."""
    hardware_definition = build_duet_2_maestro()

    if hardware_definition.id not in model.hardware_definitions:
        model.add_hardware_definition(
            hardware_definition
        )

    controller = Controller(
        id=controller_id,
        name=label,
        controller_type="motion_controller",
        version="v1.0",
        hardware_definition_id=hardware_definition.id,
    )

    model.add_controller(
        machine_id,
        controller,
    )

    ports: list[SemanticPort] = []

    for (
        connector_id,
        connector_name,
        position_count,
    ) in DUET_2_MAESTRO_CONNECTOR_LAYOUT:
        for position in range(
            1,
            position_count + 1,
        ):
            pin_label: str | None = None
            purpose = (
                f"{connector_name}"
                " connector contact"
            )

            port_properties: dict[str, object] = {
                "connector_position_count": (
                    position_count
                )
            }

            direction = "unknown"

            if (
                connector_id
                in DUET2_MAESTRO_MOTOR_CONNECTOR_IDS
            ):
                pin_label = (
                    DUET2_MAESTRO_MOTOR_PIN_LABELS[
                        position - 1
                    ]
                )

                purpose = (
                    f"Stepper motor coil "
                    f"{pin_label} terminal"
                )

                port_properties[
                    "pin_label"
                ] = pin_label

            elif (
                connector_id
                in DUET2_MAESTRO_ENDSTOP_CONNECTOR_IDS
            ):
                if position == 1:
                    pin_label = (
                        DUET2_MAESTRO_ENDSTOP_SIGNAL_LABELS[
                            connector_id
                        ]
                    )
                    purpose = (
                        f"{connector_name}"
                        " signal input"
                    )
                    direction = "input"
                    electrical_role = (
                        "endstop_input"
                    )
                elif position == 2:
                    pin_label = "+3.3V"
                    purpose = "+3.3 V supply"
                    electrical_role = (
                        "power_supply_3v3"
                    )
                else:
                    pin_label = "GND"
                    purpose = "Ground reference"
                    electrical_role = (
                        "ground_reference"
                    )

                port_properties[
                    "pin_label"
                ] = pin_label

                port_properties[
                    "electrical_role"
                ] = electrical_role

            elif (
                connector_id
                in DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS
            ):
                specification = (
                    DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS[
                        connector_id
                    ]
                )

                purpose = (
                    f"{connector_name}"
                    " output contact"
                )

                direction = "output"

                port_properties[
                    "interface_type"
                ] = specification[
                    "interface_type"
                ]

                port_properties[
                    "output_voltage"
                ] = specification[
                    "output_voltage"
                ]

                port_properties[
                    "maximum_current"
                ] = specification[
                    "maximum_current"
                ]

                port_properties[
                    "electrical_role"
                ] = "heater_output"

            elif connector_id == "bed-temp":
                direction = "input"
                port_properties["electrical_role"] = "temperature_sensor_input"

            elif connector_id == "e0-temp":
                direction = "input"
                port_properties["electrical_role"] = "temperature_sensor_input"

            elif connector_id == "e1-temp":
                direction = "input"
                port_properties["electrical_role"] = "temperature_sensor_input"

            elif connector_id == "c-temp":
                direction = "input"
                port_properties["electrical_role"] = "temperature_sensor_input"

            elif connector_id == "z-probe":
                if position == 1:
                    pin_label = "Z_PROBE_IN"
                    purpose = "Z probe signal input"
                    direction = "input"
                    electrical_role = "z_probe_signal_input"
                elif position == 2:
                    pin_label = "GND"
                    purpose = "Ground reference"
                    electrical_role = "ground_reference"
                elif position == 3:
                    pin_label = "Z_PROBE_MOD"
                    purpose = "Z probe MOD control output"
                    direction = "output"
                    electrical_role = "z_probe_mod_output"
                elif position == 4:
                    pin_label = "+3.3V"
                    purpose = "3.3 V supply"
                    electrical_role = "power_supply_3v3"
                else:
                    pin_label = "+5V"
                    purpose = "5 V supply"
                    electrical_role = "power_supply_5v"

                port_properties["pin_label"] = pin_label
                port_properties["electrical_role"] = electrical_role

            elif connector_id == "j21":
                j21_pins = {
                    1: ("+5V", "5 V supply", "unknown", "power_supply_5v"),
                    2: ("GND", "Ground reference", "unknown", "ground_reference"),
                    3: ("RESET", "Board reset signal", "unknown", None),
                    4: ("EXP_0", "Expansion general-purpose signal", "unknown", None),
                    5: ("EXP_1", "Expansion general-purpose signal", "unknown", None),
                    6: ("ADVREF", "Analog reference signal", "unknown", None),
                    7: ("VSSA", "Analog ground reference", "unknown", "analog_ground_reference"),
                    8: ("TWCK0", "I2C clock signal", "unknown", None),
                    9: ("TWD0", "I2C data signal", "unknown", None),
                    10: ("+3.3V", "3.3 V supply", "unknown", "power_supply_3v3"),
                    11: ("SERVO", "Servo control output", "output", "servo_control_output"),
                    12: ("+5V", "5 V supply", "unknown", "power_supply_5v"),
                    13: ("GND", "Ground reference", "unknown", "ground_reference"),
                }

                (
                    pin_label,
                    purpose,
                    direction,
                    electrical_role,
                ) = j21_pins[position]

                port_properties["pin_label"] = pin_label

                if electrical_role is not None:
                    port_properties["electrical_role"] = electrical_role

            elif connector_id == "temp-ob":
                temp_ob_pins = {
                    1: ("SPI0_CS2", "SPI chip-select signal", "unknown", None),
                    2: ("GND", "Ground reference", "unknown", "ground_reference"),
                    3: ("SPI0_CS1", "SPI chip-select signal", "unknown", None),
                    4: ("SPI0_SCK", "SPI clock signal", "unknown", None),
                    5: ("SPI0_MOSI", "SPI data output signal", "unknown", None),
                    6: ("SPI0_MISO", "SPI data input signal", "unknown", None),
                    7: ("TWCK0", "I2C clock signal", "unknown", None),
                    8: ("+3.3V", "3.3 V supply", "unknown", "power_supply_3v3"),
                    9: ("TWD0", "I2C data signal", "unknown", None),
                    10: ("NC", "No connect", "unknown", None),
                }

                (
                    pin_label,
                    purpose,
                    direction,
                    electrical_role,
                ) = temp_ob_pins[position]

                port_properties["pin_label"] = pin_label

                if electrical_role is not None:
                    port_properties["electrical_role"] = electrical_role

            elif connector_id == "j4":
                j4_pins = {
                    1: ("GND", "Ground reference", "unknown", "ground_reference"),
                    2: ("V_IN", "Board power input", "unknown", None),
                    3: ("V_IN", "Bed heater supply", "unknown", None),
                    4: ("BED-", "Bed heater output return", "output", "heater_output"),
                }

                (
                    pin_label,
                    purpose,
                    direction,
                    electrical_role,
                ) = j4_pins[position]

                port_properties["pin_label"] = pin_label

                if electrical_role is not None:
                    port_properties["electrical_role"] = electrical_role

            elif connector_id in {"e2-driver", "e3-driver"}:
                driver_name = (
                    "E2"
                    if connector_id == "e2-driver"
                    else "E3"
                )

                if position == 1:
                    pin_label = "V_IN"
                    purpose = "External driver input supply"
                elif position == 2:
                    pin_label = "GND"
                    purpose = "Ground reference"
                    port_properties["electrical_role"] = (
                        "ground_reference"
                    )
                elif position == 3:
                    pin_label = f"{driver_name}_UART"
                    purpose = (
                        f"{driver_name} driver UART "
                        "configuration/communication"
                    )
                elif position == 4:
                    pin_label = f"{driver_name}_EN"
                    purpose = f"{driver_name} driver enable signal"
                    direction = "output"
                elif position == 5:
                    pin_label = f"{driver_name}_STEP"
                    purpose = f"{driver_name} step signal output"
                    direction = "output"
                elif position == 6:
                    pin_label = f"{driver_name}_DIR"
                    purpose = f"{driver_name} direction signal output"
                    direction = "output"
                elif position == 7:
                    pin_label = "GND"
                    purpose = "Ground reference"
                    port_properties["electrical_role"] = (
                        "ground_reference"
                    )
                else:
                    pin_label = "+3.3V"
                    purpose = "3.3 V supply"
                    port_properties["electrical_role"] = (
                        "power_supply_3v3"
                    )

                port_properties["pin_label"] = pin_label
            elif connector_id == "always-on-fan":
                if position == 1:
                    pin_label = "GND"
                    purpose = "Ground reference"
                    direction = "unknown"
                    electrical_role = "ground_reference"
                else:
                    pin_label = "V_FAN_A"
                    purpose = "Always-on fan supply output"
                    direction = "output"
                    electrical_role = "always_on_fan_output"

                port_properties["pin_label"] = pin_label
                port_properties["electrical_role"] = electrical_role
            elif connector_id in {"fan0", "fan1", "fan2"}:
                direction = "output"
                port_properties["electrical_role"] = "controlled_fan_output"

            pcb_identity = DUET2_MAESTRO_PCB_PAD_MAP.get(
                connector_id, {}
            ).get(position)
            port_properties["pcb_identity_inventory_status"] = (
                "covered_by_reviewed_pcb_identity_inventory"
                if pcb_identity is not None
                else "outside_reviewed_pcb_identity_inventory"
            )
            pcb_provenance: list[Provenance] = []
            if pcb_identity is not None:
                (
                    pcb_reference_designator,
                    pcb_pad_number,
                    pcb_net_name,
                ) = pcb_identity
                pcb_net_status = (
                    DUET2_MAESTRO_PCB_NET_STATUS_ASSIGNED
                    if pcb_net_name is not None
                    else DUET2_MAESTRO_PCB_NET_STATUS_UNASSIGNED
                )
                port_properties.update({
                    "pcb_reference_designator": pcb_reference_designator,
                    "pcb_pad_number": pcb_pad_number,
                    "pcb_net_name": pcb_net_name,
                    "pcb_net_status": pcb_net_status,
                    "pcb_source_url": DUET2_MAESTRO_PCB_SOURCE_URL,
                    "pcb_source_commit": DUET2_MAESTRO_PCB_SOURCE_COMMIT,
                    "pcb_source_revision": DUET2_MAESTRO_PCB_SOURCE_REVISION,
                    "pcb_source_file": DUET2_MAESTRO_PCB_SOURCE_FILE,
                    "pcb_board_revision": DUET2_MAESTRO_PCB_BOARD_REVISION,
                    "pcb_source_date": DUET2_MAESTRO_PCB_SOURCE_DATE,
                })
                net_context = (
                    f"net {pcb_net_name!r}"
                    if pcb_net_name is not None
                    else "no net assigned in the reference PCB"
                )
                pcb_provenance.append(
                    Provenance(
                        source=DUET2_MAESTRO_PCB_SOURCE_URL,
                        evidence_type="published",
                        method=(
                            "manual crosswalk review against pinned "
                            "manufacturer KiCad PCB source"
                        ),
                        context=(
                            f"PCB title-block revision "
                            f"{DUET2_MAESTRO_PCB_BOARD_REVISION}, "
                            f"date {DUET2_MAESTRO_PCB_SOURCE_DATE}; "
                            f"repository commit "
                            f"{DUET2_MAESTRO_PCB_SOURCE_COMMIT}; "
                            f"PCB reference {pcb_reference_designator}, "
                            f"pad {pcb_pad_number}: {net_context}. "
                            "This is reference-PCB evidence only; installed "
                            "hardware and physical wiring are not thereby "
                            "verified."
                        ),
                        date="2026-10-11",
                        notes=(
                            f"Source file: {DUET2_MAESTRO_PCB_SOURCE_FILE}. "
                            "This is a manually reviewed expected crosswalk; "
                            "tests do not automatically parse the external "
                            "PCB source. Exact source net spelling is "
                            "preserved. An unassigned reference-PCB pad does "
                            "not prove real-world physical disconnection. "
                            "PCB-view coordinates and cable mating-face/"
                            "cavity positions are not inferred."
                        ),
                    )
                )

            if connector_id == "z-probe":
                guide_position = (
                    DUET2_MAESTRO_PROMEGA_GUIDE_VIEW_POSITIONS.get(
                        pin_label or ""
                    )
                )
                if guide_position is not None:
                    port_properties.update({
                        "promega_diagram_view_position": guide_position,
                        "promega_diagram_view_source": (
                            DUET2_MAESTRO_PROMEGA_GUIDE_VIEW_SOURCE
                        ),
                    })

            port = SemanticPort(
                id=(
                    f"{controller_id}"
                    f"-{connector_id}"
                    f"-pin-{position}"
                ),
                component_id=None,
                purpose=purpose,
                direction=direction,
                connector_id=connector_id,
                pin_id=str(position),
                properties=port_properties,
                provenance=pcb_provenance,
                controller_id=controller_id,
            )

            model.add_port(
                port
            )

            ports.append(port)

    for (
        resource_suffix,
        resource_name,
        molex_connector_id,
        screw_connector_id,
    ) in DUET2_MAESTRO_HEATER_RESOURCES:
        resource = ControllerResource(
            id=f"{controller_id}-{resource_suffix}",
            name=resource_name,
            resource_type="heater",
            controller_id=controller_id,
        )

        model.add_controller_resource(
            machine_id,
            resource,
        )

        for port in ports:
            if port.connector_id not in {
                molex_connector_id,
                screw_connector_id,
            }:
                continue

            relationship = SemanticRelationship(
                id=(
                    f"{resource.id}"
                    f"-exposed-through-{port.id}"
                ),
                source_id=resource.id,
                target_id=port.id,
                relationship_type="exposed_through",
            )

            model.add_relationship(
                relationship
            )

    bed_heater_resource = ControllerResource(
        id=f"{controller_id}-bed-heater",
        name="Bed heater",
        resource_type="heater",
        controller_id=controller_id,
    )
    model.add_controller_resource(
        machine_id,
        bed_heater_resource,
    )

    for position in ("3", "4"):
        j4_bed_relationship = SemanticRelationship(
            id=(
                f"{bed_heater_resource.id}"
                f"-exposed-through-{controller_id}-j4-pin-{position}"
            ),
            source_id=bed_heater_resource.id,
            target_id=f"{controller_id}-j4-pin-{position}",
            relationship_type="exposed_through",
        )
        model.add_relationship(
            j4_bed_relationship
        )

    z_stepper_resource = ControllerResource(
        id=f"{controller_id}-z-stepper",
        name="Z stepper driver",
        resource_type="stepper",
        controller_id=controller_id,
    )

    model.add_controller_resource(
        machine_id,
        z_stepper_resource,
    )

    for port in ports:
        if port.connector_id not in {
            "z-a-motor",
            "z-b-motor",
        }:
            continue

        relationship = SemanticRelationship(
            id=(
                f"{z_stepper_resource.id}"
                f"-exposed-through-{port.id}"
            ),
            source_id=z_stepper_resource.id,
            target_id=port.id,
            relationship_type="exposed_through",
        )

        model.add_relationship(
            relationship
        )

    for (
        resource_suffix,
        resource_name,
        connector_id,
    ) in (
        (
            "e2-stepper",
            "E2 stepper driver",
            "e2-driver",
        ),
        (
            "e3-stepper",
            "E3 stepper driver",
            "e3-driver",
        ),
    ):
        resource = ControllerResource(
            id=f"{controller_id}-{resource_suffix}",
            name=resource_name,
            resource_type="stepper",
            controller_id=controller_id,
        )

        model.add_controller_resource(
            machine_id,
            resource,
        )

        for port in ports:
            if port.connector_id != connector_id:
                continue

            relationship = SemanticRelationship(
                id=(
                    f"{resource.id}"
                    f"-exposed-through-{port.id}"
                ),
                source_id=resource.id,
                target_id=port.id,
                relationship_type="exposed_through",
            )

            model.add_relationship(
                relationship
            )

    return controller, tuple(ports)


def add_octopus_tmc5160t_mating_experiment(
    model: CanonicalMachineModel,
    machine_id: str,
) -> tuple[
    Controller,
    MachineComponent,
    SemanticPort,
    SemanticPort,
]:
    """Add a minimal Octopus driver-socket/TMC5160T experiment."""
    tmc5160t_hardware = build_btt_tmc5160t()

    if (
        tmc5160t_hardware.id
        not in model.hardware_definitions
    ):
        model.add_hardware_definition(
            tmc5160t_hardware
        )

    controller = Controller(
        id="btt-octopus-v1-1-controller",
        name="BTT Octopus V1.1",
        controller_type="motion_controller",
        version="V1.1",
        properties={
            "manufacturer": "BigTreeTech",
            "family": "Octopus",
            "board_revision_evidence": (
                BTT_OCTOPUS_BOARD_REVISION_EVIDENCE
            ),
            "silkscreen_inspection_status": "uninspected",
        },
        provenance=[
            Provenance(
                source=BTT_OCTOPUS_DOCUMENTATION_SOURCE,
                evidence_type="published",
                method="manufacturer technical documentation",
                context=(
                    "Documents early-production fan polarity, SPI3 supply "
                    "label, and Raspberry Pi UART silkscreen errors. The "
                    "documentation does not establish a reliable production "
                    "boundary for an individual board."
                ),
            ),
            Provenance(
                source=BTT_OCTOPUS_PINOUT_SOURCE,
                evidence_type="published",
                method="manufacturer board pinout",
                context=(
                    "Reference for corrected board signal assignments. "
                    "The pinout does not establish the inspected silkscreen "
                    "condition of a particular installed board."
                ),
            ),
            Provenance(
                source=BTT_OCTOPUS_HARDWARE_SOURCE,
                evidence_type="published",
                method="manufacturer hardware repository",
                context=(
                    "Repository reviewed for revision-specific schematic "
                    "evidence. A complete directly comparable non-Pro "
                    "V1.0/V1.1 schematic pair was not established."
                ),
            ),
        ],
    )

    model.add_controller(
        machine_id,
        controller,
    )

    socket_port = SemanticPort(
        id=(
            f"{controller.id}"
            "-z-driver-socket-interface"
        ),
        component_id=None,
        purpose=(
            "Z stepper driver receiving interface"
        ),
        direction="unknown",
        connector_id="z-driver-socket",
        pin_id=None,
        properties={
            "interface_role": (
                "driver_module_receiving_interface"
            ),
            "interface_spec": (
                BTT_OCTOPUS_MOTOR_DRIVER_RECEIVING_INTERFACE_SPEC
            ),
            "driver_position": {
                "driver_number": 2,
                "module_position": "M3",
                "motor_outputs": (
                    "MOTOR2_1",
                    "MOTOR2_2",
                ),
            },
            "contact_6_net": "DRIVER2_SLP",
        },
        provenance=[
            Provenance(
                source=BTT_OCTOPUS_HARDWARE_SOURCE,
                evidence_type="published",
                method="manufacturer hardware repository schematic",
                context=(
                    "The generic MOTOR_DRIVER receiving interface is "
                    "repeated across the Octopus driver positions. "
                    "Driver 2 is module position M3 with MOTOR2_1 and "
                    "MOTOR2_2 motor outputs."
                ),
            ),
            Provenance(
                source=BTT_OCTOPUS_DOCUMENTATION_SOURCE,
                evidence_type="published",
                method="manufacturer technical documentation",
                context=(
                    "The Octopus documentation identifies pluggable "
                    "motor-driver sockets and documents the driver-mode "
                    "jumper configurations."
                ),
            ),
            Provenance(
                source=BTT_TMC5160T_HARDWARE_SOURCE,
                evidence_type="published",
                method="manufacturer technical documentation",
                context=(
                    "The TMC5160T Pro V1.0 documentation identifies "
                    "J1-6 as CLK. The evidence does not establish "
                    "equivalence with Octopus contact 6 SLEEP."
                ),
            ),
        ],
        controller_id=controller.id,
    )

    model.add_port(
        socket_port
    )

    module = MachineComponent(
        id="btt-tmc5160t-1",
        role="stepper_driver_module",
        label="BTT TMC5160T",
        hardware_definition_id=(
            tmc5160t_hardware.id
        ),
    )

    model.add_component(
        machine_id,
        module,
    )

    module_port = SemanticPort(
        id=(
            f"{module.id}"
            "-mating-interface"
        ),
        component_id=module.id,
        purpose=(
            "TMC5160T driver module mating interface"
        ),
        direction="unknown",
        connector_id="tmc5160t-module-interface",
        pin_id=None,
        properties={
            "interface_role": (
                "driver_module_mating_interface"
            ),
            "contact_count": 16,
            "interface_source": (
                BTT_TMC5160T_HARDWARE_SOURCE
            ),
        },
        provenance=[
            Provenance(
                source=BTT_TMC5160T_HARDWARE_SOURCE,
                evidence_type="published",
                method="manufacturer technical documentation",
                context=(
                    "The TMC5160T module exposes its J1 and J2 "
                    "interfaces through the documented plug-in driver "
                    "module interface."
                ),
            )
        ],
    )

    model.add_port(
        module_port
    )

    relationship = SemanticRelationship(
        id=(
            f"{socket_port.id}"
            "-mated-with-"
            f"{module_port.id}"
        ),
        source_id=socket_port.id,
        target_id=module_port.id,
        relationship_type="mated_with",
    )

    model.add_relationship(
        relationship
    )

    return (
        controller,
        module,
        socket_port,
        module_port,
    )