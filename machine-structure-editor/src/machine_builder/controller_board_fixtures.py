"""Concrete controller-board fixtures for Machine Builder."""

from __future__ import annotations

from .controller_resource import ControllerResource
from .hardware_catalog import (
    DUET2_MAESTRO_ENDSTOP_CONNECTOR_IDS,
    DUET2_MAESTRO_ENDSTOP_SIGNAL_LABELS,
    DUET2_MAESTRO_HEATER_CONNECTOR_SPECIFICATIONS,
    DUET2_MAESTRO_HEATER_RESOURCES,
    DUET2_MAESTRO_MOTOR_CONNECTOR_IDS,
    DUET2_MAESTRO_MOTOR_PIN_LABELS,
    build_duet_2_maestro,
)
from .semantic_model import (
    CanonicalMachineModel,
    Controller,
    SemanticPort,
)
from .semantic_relationship import SemanticRelationship


DUET_2_MAESTRO_CONNECTOR_LAYOUT = (
    ("x-motor", "X motor", 4),
    ("z-a-motor", "Z A motor", 4),
    ("z-b-motor", "Z B motor", 4),
    ("bed-heat-molex", "Bed heat Molex", 2),
    ("bed-heat-screw", "Bed heat screw terminal", 2),
    ("e0-heat-molex", "E0 heat Molex", 2),
    ("e0-heat-screw", "E0 heat screw terminal", 2),
    ("e1-heat-molex", "E1 heat Molex", 2),
    ("e1-heat-screw", "E1 heat screw terminal", 2),
    ("thermistor", "Thermistor", 2),
    ("x-stop", "X stop", 3),
    ("y-stop", "Y stop", 3),
    ("z-stop", "Z stop", 3),
    ("e0-stop", "E0 stop", 3),
    ("e1-stop", "E1 stop", 3),
    ("z-probe", "Z probe", 5),
    ("fan", "Fan", 2),
)


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
                provenance=[],
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

    return controller, tuple(ports)