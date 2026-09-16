from machine_builder.controller import Controller
from machine_builder.controller_resource import ControllerResource
from machine_builder.semantic_model import CanonicalMachineModel


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
        },
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