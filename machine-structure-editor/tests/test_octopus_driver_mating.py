"""Tests for the Octopus driver-module mating experiment."""

from machine_builder.controller_board_fixtures import (
    add_octopus_tmc5160t_mating_experiment,
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


def test_octopus_mating_uses_existing_semantic_port_endpoints() -> None:
    model = make_test_model()

    (
        controller,
        module,
        socket_port,
        module_port,
    ) = add_octopus_tmc5160t_mating_experiment(
        model,
        machine_id="machine-1",
    )

    assert socket_port.controller_id == controller.id
    assert socket_port.component_id is None

    assert module_port.component_id == module.id
    assert module_port.controller_id is None

    assert socket_port.pin_id is None
    assert module_port.pin_id is None


def test_octopus_mating_relationship_is_interface_level() -> None:
    model = make_test_model()

    (
        controller,
        module,
        socket_port,
        module_port,
    ) = add_octopus_tmc5160t_mating_experiment(
        model,
        machine_id="machine-1",
    )

    relationships = [
        relationship
        for relationship
        in model.relationships.values()
        if relationship.relationship_type
        == "mated_with"
    ]

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.source_id == socket_port.id
    assert relationship.target_id == module_port.id

    assert (
        relationship.is_type(
            "mated_with"
        )
    )

    assert (
        model.ports[
            relationship.source_id
        ].controller_id
        == controller.id
    )

    assert (
        model.ports[
            relationship.target_id
        ].component_id
        == module.id
    )


def test_octopus_mating_is_not_exposed_through() -> None:
    model = make_test_model()

    add_octopus_tmc5160t_mating_experiment(
        model,
        machine_id="machine-1",
    )

    mating_relationships = [
        relationship
        for relationship
        in model.relationships.values()
        if relationship.relationship_type
        == "mated_with"
    ]

    exposure_relationships = [
        relationship
        for relationship
        in model.relationships.values()
        if relationship.relationship_type
        == "exposed_through"
    ]

    assert len(
        mating_relationships
    ) == 1

    assert exposure_relationships == []


def test_removing_driver_module_removes_mating_relationship() -> None:
    model = make_test_model()

    (
        _,
        module,
        socket_port,
        module_port,
    ) = add_octopus_tmc5160t_mating_experiment(
        model,
        machine_id="machine-1",
    )

    relationship_id = (
        f"{socket_port.id}"
        "-mated-with-"
        f"{module_port.id}"
    )

    assert relationship_id in (
        model.relationships
    )

    model.remove_component(
        module.id
    )

    assert relationship_id not in (
        model.relationships
    )

    assert module_port.id not in (
        model.ports
    )

    assert socket_port.id in (
        model.ports
    )