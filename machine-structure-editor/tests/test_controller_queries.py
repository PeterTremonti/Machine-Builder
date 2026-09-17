"""Tests for canonical controller queries."""

from machine_builder.controller import Controller
from machine_builder.controller_queries import (
    controller_for_resource,
    controllers_for_machine,
    get_controller,
    machine_id_for_controller,
)
from machine_builder.controller_resource import (
    ControllerResource,
)
from machine_builder.editor_state import EditorState
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
)
from machine_builder.visual_model import VisualModel


def make_state() -> EditorState:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    model.add_controller(
        "machine-1",
        Controller(
            id="controller-1",
            name="Main Controller",
            controller_type="motion_controller",
            version="1.0",
        ),
    )

    model.add_controller_resource(
        "machine-1",
        ControllerResource(
            id="resource-1",
            name="Heater Output 0",
            resource_type="heater",
            controller_id="controller-1",
        ),
    )

    return EditorState(
        visual_model=VisualModel(),
        semantic_model=model,
    )


def test_get_controller_returns_controller() -> None:
    state = make_state()

    controller = get_controller(
        state,
        "controller-1",
    )

    assert controller.name == (
        "Main Controller"
    )


def test_get_controller_rejects_unknown_id() -> None:
    state = make_state()

    try:
        get_controller(
            state,
            "missing",
        )

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert "Unknown controller" in str(exc)


def test_machine_id_for_controller() -> None:
    state = make_state()

    assert (
        machine_id_for_controller(
            state,
            "controller-1",
        )
        == "machine-1"
    )


def test_machine_id_for_unattached_controller() -> None:
    state = make_state()

    state.semantic_model.machines[
        "machine-1"
    ].controller_ids.clear()

    try:
        machine_id_for_controller(
            state,
            "controller-1",
        )

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert (
            "not attached"
            in str(exc)
        )


def test_controllers_for_machine() -> None:
    state = make_state()

    controllers = controllers_for_machine(
        state,
        "machine-1",
    )

    assert len(controllers) == 1
    assert controllers[0].id == (
        "controller-1"
    )


def test_unknown_machine_rejected() -> None:
    state = make_state()

    try:
        controllers_for_machine(
            state,
            "missing",
        )

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert "Unknown machine" in str(exc)


def test_controller_for_resource() -> None:
    state = make_state()

    controller = controller_for_resource(
        state,
        "resource-1",
    )

    assert controller is not None
    assert controller.id == "controller-1"


def test_resource_without_controller_returns_none() -> None:
    state = make_state()

    state.semantic_model.controller_resources[
        "resource-1"
    ].controller_id = None

    assert (
        controller_for_resource(
            state,
            "resource-1",
        )
        is None
    )


def test_unknown_resource_rejected() -> None:
    state = make_state()

    try:
        controller_for_resource(
            state,
            "missing",
        )

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown controller resource"
            in str(exc)
        )