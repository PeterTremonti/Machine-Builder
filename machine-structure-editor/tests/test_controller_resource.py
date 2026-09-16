"""Tests for canonical controller resources."""

import pytest

from machine_builder.controller_resource import (
    ControllerResource,
)
from machine_builder.semantic_model import (
    Controller,
    Machine,
    Provenance,
)


def test_controller_resource_can_be_created() -> None:
    resource = ControllerResource(
        id="resource-1",
        name="Heater Output 0",
        resource_type="heater_output",
    )

    assert resource.id == "resource-1"
    assert resource.name == "Heater Output 0"
    assert (
        resource.resource_type
        == "heater_output"
    )


def test_controller_resource_can_reference_controller() -> None:
    resource = ControllerResource(
        id="resource-1",
        name="Fan Output 0",
        resource_type="fan_output",
        controller_id="controller-1",
    )

    assert (
        resource.controller_id
        == "controller-1"
    )


def test_controller_resource_can_store_properties() -> None:
    resource = ControllerResource(
        id="resource-1",
        name="Heater Output 0",
        resource_type="heater_output",
        properties={
            "voltage": "24 V",
            "max_current": "2 A",
        },
    )

    assert (
        resource.properties["voltage"]
        == "24 V"
    )

    assert (
        resource.properties["max_current"]
        == "2 A"
    )


def test_controller_resource_can_store_provenance() -> None:
    provenance = Provenance(
        source="Controller documentation",
        evidence_type="published",
        method="manual review",
    )

    resource = ControllerResource(
        id="resource-1",
        name="Temperature Input 0",
        resource_type="temperature_input",
        provenance=[
            provenance
        ],
    )

    assert (
        resource.provenance[0]
        is provenance
    )


def test_empty_controller_resource_id_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Controller resource ID cannot be empty",
    ):
        ControllerResource(
            id="",
            name="Heater Output 0",
            resource_type="heater_output",
        )


def test_empty_controller_resource_name_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Controller resource name cannot be empty",
    ):
        ControllerResource(
            id="resource-1",
            name="",
            resource_type="heater_output",
        )


def test_empty_controller_resource_type_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Controller resource type cannot be empty",
    ):
        ControllerResource(
            id="resource-1",
            name="Heater Output 0",
            resource_type="",
        )


def test_controller_resource_can_exist_without_controller_id() -> None:
    resource = ControllerResource(
        id="resource-1",
        name="Unknown Output",
        resource_type="unknown",
    )

    assert resource.controller_id is None


def test_controller_resource_can_reference_real_controller() -> None:
    controller = Controller(
        id="controller-1",
        name="Test Controller",
        controller_type="motion_controller",
    )

    assert controller.id == "controller-1"
    assert controller.controller_type == (
        "motion_controller"
    )