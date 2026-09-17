"""Tests for controller editing mutations."""

from machine_builder.controller import Controller
from machine_builder.controller_mutations import (
    SetControllerProperty,
    UpdateController,
)
from machine_builder.editor_state import EditorState
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
)
from machine_builder.visual_model import VisualModel, VisualNode


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

    return EditorState(
        visual_model=VisualModel(),
        semantic_model=model,
    )


def test_update_controller_name() -> None:
    state = make_state()

    UpdateController(
        controller_id="controller-1",
        name="Main Motion Controller",
    ).apply(state)

    assert (
        state.semantic_model.controllers[
            "controller-1"
        ].name
        == "Main Motion Controller"
    )


def test_update_controller_name_updates_visual_node_label() -> None:
    state = make_state()

    state.visual_model.add_node(
        VisualNode(
            id="controller-node-1",
            node_type="controller",
            label="Main Controller",
            semantic_reference="controller-1",
        )
    )

    UpdateController(
        controller_id="controller-1",
        name="Main Motion Controller",
    ).apply(state)

    assert (
        state.semantic_model.controllers[
            "controller-1"
        ].name
        == "Main Motion Controller"
    )

    assert (
        state.visual_model.nodes[
            "controller-node-1"
        ].label
        == "Main Motion Controller"
    )


def test_update_controller_type() -> None:
    state = make_state()

    UpdateController(
        controller_id="controller-1",
        controller_type="RRF",
    ).apply(state)

    assert (
        state.semantic_model.controllers[
            "controller-1"
        ].controller_type
        == "RRF"
    )


def test_update_controller_version() -> None:
    state = make_state()

    UpdateController(
        controller_id="controller-1",
        version="3.5.4",
    ).apply(state)

    assert (
        state.semantic_model.controllers[
            "controller-1"
        ].version
        == "3.5.4"
    )


def test_blank_version_becomes_none() -> None:
    state = make_state()

    UpdateController(
        controller_id="controller-1",
        version="   ",
    ).apply(state)

    assert (
        state.semantic_model.controllers[
            "controller-1"
        ].version
        is None
    )


def test_update_controller_properties() -> None:
    state = make_state()

    UpdateController(
        controller_id="controller-1",
        properties={
            "board": "Duet 2 Maestro",
            "axes": 3,
        },
    ).apply(state)

    assert (
        state.semantic_model.controllers[
            "controller-1"
        ].properties
        == {
            "board": "Duet 2 Maestro",
            "axes": 3,
        }
    )


def test_set_controller_property() -> None:
    state = make_state()

    SetControllerProperty(
        controller_id="controller-1",
        property_name="firmware",
        value="RRF",
    ).apply(state)

    assert (
        state.semantic_model.controllers[
            "controller-1"
        ].properties["firmware"]
        == "RRF"
    )


def test_unknown_controller_rejected() -> None:
    state = make_state()

    try:
        UpdateController(
            controller_id="missing",
            name="Nope",
        ).apply(state)

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown controller"
            in str(exc)
        )


def test_blank_controller_name_rejected() -> None:
    state = make_state()

    try:
        UpdateController(
            controller_id="controller-1",
            name="   ",
        ).apply(state)

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert "name" in str(exc)


def test_blank_controller_type_rejected() -> None:
    state = make_state()

    try:
        UpdateController(
            controller_id="controller-1",
            controller_type="   ",
        ).apply(state)

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert "type" in str(exc)


def test_blank_property_name_rejected() -> None:
    state = make_state()

    try:
        SetControllerProperty(
            controller_id="controller-1",
            property_name="   ",
            value=10,
        ).apply(state)

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert "property name" in str(exc)