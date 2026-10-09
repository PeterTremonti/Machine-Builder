from machine_builder.controller import Controller
from machine_builder.controller_resource import ControllerResource
from machine_builder.hardware_catalog import (
    BTT_OCTOPUS_BOARD_REVISION_EVIDENCE,
    BTT_OCTOPUS_DOCUMENTATION_SOURCE,
    BTT_OCTOPUS_HARDWARE_SOURCE,
    BTT_OCTOPUS_PINOUT_SOURCE,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Provenance,
)


def add_generic_octopus_controller(
    model: CanonicalMachineModel,
    machine_id: str,
    controller_id: str = "octopus-v1-1",
    label: str = "BTT Octopus V1.1",
) -> Controller:
    """Add a simplified BTT Octopus V1.1 controller and basic resources."""
    controller = Controller(
        id=controller_id,
        name=label,
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

    resources = [
        ControllerResource(
            id=f"{controller_id}-stepper-x",
            name="Stepper X",
            resource_type="stepper_output",
            controller_id=controller_id,
        ),
        ControllerResource(
            id=f"{controller_id}-stepper-y",
            name="Stepper Y",
            resource_type="stepper_output",
            controller_id=controller_id,
        ),
        ControllerResource(
            id=f"{controller_id}-stepper-z",
            name="Stepper Z",
            resource_type="stepper_output",
            controller_id=controller_id,
        ),
        ControllerResource(
            id=f"{controller_id}-stepper-e",
            name="Stepper E",
            resource_type="stepper_output",
            controller_id=controller_id,
        ),
        ControllerResource(
            id=f"{controller_id}-heater-0",
            name="Heater 0",
            resource_type="heater_output",
            controller_id=controller_id,
        ),
        ControllerResource(
            id=f"{controller_id}-thermistor-0",
            name="Thermistor 0",
            resource_type="temperature_input",
            controller_id=controller_id,
        ),
        ControllerResource(
            id=f"{controller_id}-fan-0",
            name="Fan 0",
            resource_type="fan_output",
            controller_id=controller_id,
        ),
    ]

    for resource in resources:
        model.add_controller_resource(
            machine_id,
            resource,
        )

    return controller