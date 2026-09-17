from machine_builder.controller import Controller
from machine_builder.controller_resource import ControllerResource
from machine_builder.controller_resource_mutations import (
    SetControllerResourceProperty,
    UpdateControllerResource,
)
from machine_builder.editor_state import EditorState
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
)


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
            controller_type="test",
        ),
    )

    model.add_controller_resource(
        "machine-1",
        ControllerResource(
            id="resource-1",
            name="Heater Output",
            resource_type="heater",
            controller_id="controller-1",
        ),
    )

    return EditorState(
        visual_model=None,
        semantic_model=model,
    )


def test_update_resource_name():
    state = make_state()

    UpdateControllerResource(
        resource_id="resource-1",
        name="Bed Heater",
        resource_type="heater",
        controller_id="controller-1",
    ).apply(state)

    assert (
        state.semantic_model.controller_resources[
            "resource-1"
        ].name
        == "Bed Heater"
    )


def test_update_resource_type():
    state = make_state()

    UpdateControllerResource(
        resource_id="resource-1",
        name="Heater Output",
        resource_type="high_power_output",
        controller_id="controller-1",
    ).apply(state)

    assert (
        state.semantic_model.controller_resources[
            "resource-1"
        ].resource_type
        == "high_power_output"
    )


def test_update_resource_controller():
    state = make_state()

    state.semantic_model.add_controller(
        "machine-1",
        Controller(
            id="controller-2",
            name="Secondary Controller",
            controller_type="test",
        ),
    )

    UpdateControllerResource(
        resource_id="resource-1",
        name="Heater Output",
        resource_type="heater",
        controller_id="controller-2",
    ).apply(state)

    assert (
        state.semantic_model.controller_resources[
            "resource-1"
        ].controller_id
        == "controller-2"
    )


def test_clear_resource_controller():
    state = make_state()

    UpdateControllerResource(
        resource_id="resource-1",
        name="Heater Output",
        resource_type="heater",
        controller_id=None,
    ).apply(state)

    assert (
        state.semantic_model.controller_resources[
            "resource-1"
        ].controller_id
        is None
    )


def test_update_resource_properties():
    state = make_state()

    UpdateControllerResource(
        resource_id="resource-1",
        name="Heater Output",
        resource_type="heater",
        controller_id="controller-1",
        properties={"max_current": 5},
    ).apply(state)

    assert (
        state.semantic_model.controller_resources[
            "resource-1"
        ].properties
        == {"max_current": 5}
    )


def test_set_resource_property():
    state = make_state()

    SetControllerResourceProperty(
        resource_id="resource-1",
        name="max_current",
        value=5,
    ).apply(state)

    assert (
        state.semantic_model.controller_resources[
            "resource-1"
        ].properties["max_current"]
        == 5
    )


def test_set_resource_property_replaces_value():
    state = make_state()

    state.semantic_model.controller_resources[
        "resource-1"
    ].properties["max_current"] = 3

    SetControllerResourceProperty(
        resource_id="resource-1",
        name="max_current",
        value=5,
    ).apply(state)

    assert (
        state.semantic_model.controller_resources[
            "resource-1"
        ].properties["max_current"]
        == 5
    )


def test_update_rejects_blank_name():
    state = make_state()

    try:
        UpdateControllerResource(
            resource_id="resource-1",
            name=" ",
            resource_type="heater",
            controller_id="controller-1",
        ).apply(state)
    except ValueError:
        return

    raise AssertionError(
        "Expected blank resource name to be rejected."
    )


def test_update_rejects_blank_type():
    state = make_state()

    try:
        UpdateControllerResource(
            resource_id="resource-1",
            name="Heater Output",
            resource_type=" ",
            controller_id="controller-1",
        ).apply(state)
    except ValueError:
        return

    raise AssertionError(
        "Expected blank resource type to be rejected."
    )


def test_set_property_rejects_blank_name():
    state = make_state()

    try:
        SetControllerResourceProperty(
            resource_id="resource-1",
            name=" ",
            value=5,
        ).apply(state)
    except ValueError:
        return

    raise AssertionError(
        "Expected blank property name to be rejected."
    )