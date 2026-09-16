from machine_builder.controller_assignment_fixtures import (
    add_generic_heater_controller_assignment,
    add_generic_heater_controller_assignment_to_model,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
)


def build_model() -> CanonicalMachineModel:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    return model


def test_heater_assignment_fixture_creates_controller() -> None:
    model = build_model()

    assignment = add_generic_heater_controller_assignment(
        model=model,
        machine_id="machine-1",
    )

    assert assignment.resource_id == (
        "octopus-v1-1-heater-0"
    )
    assert "octopus-v1-1" in model.controllers


def test_heater_assignment_fixture_creates_heater() -> None:
    model = build_model()

    assignment = add_generic_heater_controller_assignment(
        model=model,
        machine_id="machine-1",
    )

    assert assignment.source_id == (
        "chamber-heater-1"
    )
    assert "chamber-heater-1" in model.components


def test_heater_assignment_fixture_returns_expected_assignment() -> None:
    model = build_model()

    assignment = add_generic_heater_controller_assignment(
        model=model,
        machine_id="machine-1",
    )

    assert assignment.id == (
        "chamber-heater-1-controller-assignment"
    )
    assert assignment.assignment_type == "controls"
    assert assignment.properties[
        "semantic_role"
    ] == "heater"


def test_heater_assignment_fixture_does_not_store_assignment() -> None:
    model = build_model()

    assignment = add_generic_heater_controller_assignment(
        model=model,
        machine_id="machine-1",
    )

    assert assignment.id not in (
        model.controller_resource_assignments
    )


def test_stored_heater_assignment_fixture_adds_assignment() -> None:
    model = build_model()

    assignment = (
        add_generic_heater_controller_assignment_to_model(
            model=model,
            machine_id="machine-1",
        )
    )

    assert (
        model.controller_resource_assignments[
            assignment.id
        ]
        is assignment
    )


def test_stored_heater_assignment_fixture_attaches_to_machine() -> None:
    model = build_model()

    assignment = (
        add_generic_heater_controller_assignment_to_model(
            model=model,
            machine_id="machine-1",
        )
    )

    assert assignment.id in (
        model.machines[
            "machine-1"
        ].controller_resource_assignment_ids
    )


def test_stored_heater_assignment_fixture_is_idempotent() -> None:
    model = build_model()

    first = (
        add_generic_heater_controller_assignment_to_model(
            model=model,
            machine_id="machine-1",
        )
    )

    second = (
        add_generic_heater_controller_assignment_to_model(
            model=model,
            machine_id="machine-1",
        )
    )

    assert second is first
    assert list(
        model.controller_resource_assignments
    ) == [
        first.id,
    ]


def test_stored_heater_assignment_fixture_supports_custom_ids() -> None:
    model = build_model()

    assignment = (
        add_generic_heater_controller_assignment_to_model(
            model=model,
            machine_id="machine-1",
            component_id="heater-2",
            controller_id="controller-2",
        )
    )

    assert assignment.id == (
        "heater-2-controller-assignment"
    )
    assert assignment.source_id == "heater-2"
    assert assignment.resource_id == (
        "controller-2-heater-0"
    )
    assert assignment.id in (
        model.controller_resource_assignments
    )