from machine_builder.controller_resource import (
    ControllerResource,
)
from machine_builder.controller_resource_details import (
    ControllerResourceDetailsResult,
)


def test_details_result_contains_resource_fields():
    result = ControllerResourceDetailsResult(
        name="Bed Heater",
        resource_type="heater",
        controller_id="controller-1",
    )

    assert result.name == "Bed Heater"
    assert result.resource_type == "heater"
    assert result.controller_id == (
        "controller-1"
    )


def test_details_result_can_represent_unassigned_resource():
    result = ControllerResourceDetailsResult(
        name="Unused Output",
        resource_type="output",
        controller_id=None,
    )

    assert result.controller_id is None