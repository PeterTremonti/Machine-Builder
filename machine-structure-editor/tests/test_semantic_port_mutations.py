"""Tests for semantic port editing mutations."""

from machine_builder.editor_state import (
    EditorState,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
    SemanticPort,
)
from machine_builder.semantic_port_mutations import (
    SetSemanticPortProperty,
    UpdateSemanticPort,
)
from machine_builder.visual_model import (
    VisualModel,
    VisualNode,
    VisualPort,
)


def make_state() -> EditorState:
    semantic_model = CanonicalMachineModel()

    semantic_model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    semantic_model.add_component(
        "machine-1",
        MachineComponent(
            id="component-1",
            role="motor",
            label="X Motor",
        ),
    )

    semantic_model.add_port(
        SemanticPort(
            id="port-1",
            component_id="component-1",
            purpose="Signal",
            direction="input",
        )
    )

    visual_model = VisualModel()

    node = VisualNode(
        id="node-1",
        node_type="motor",
        label="X Motor",
        semantic_reference="component-1",
    )

    node.add_port(
        VisualPort(
            id="port-1",
            node_id="node-1",
            label="Signal",
            port_type="signal",
            direction="input",
            semantic_reference="port-1",
        )
    )

    visual_model.add_node(
        node
    )

    return EditorState(
        visual_model=visual_model,
        semantic_model=semantic_model,
    )


def test_update_port_purpose() -> None:
    state = make_state()

    UpdateSemanticPort(
        port_id="port-1",
        purpose="Motor Command",
    ).apply(state)

    port = (
        state.semantic_model.ports[
            "port-1"
        ]
    )

    visual_port = (
        state.visual_model.nodes[
            "node-1"
        ].ports["port-1"]
    )

    assert port.purpose == "Motor Command"
    assert visual_port.label == "Motor Command"


def test_update_port_direction() -> None:
    state = make_state()

    UpdateSemanticPort(
        port_id="port-1",
        direction="output",
    ).apply(state)

    port = (
        state.semantic_model.ports[
            "port-1"
        ]
    )

    visual_port = (
        state.visual_model.nodes[
            "node-1"
        ].ports["port-1"]
    )

    assert port.direction == "output"
    assert visual_port.direction == "output"


def test_update_port_connector() -> None:
    state = make_state()

    UpdateSemanticPort(
        port_id="port-1",
        connector_id="J4",
    ).apply(state)

    assert (
        state.semantic_model.ports[
            "port-1"
        ].connector_id
        == "J4"
    )


def test_update_port_pin() -> None:
    state = make_state()

    UpdateSemanticPort(
        port_id="port-1",
        pin_id="PA7",
    ).apply(state)

    assert (
        state.semantic_model.ports[
            "port-1"
        ].pin_id
        == "PA7"
    )


def test_update_port_properties() -> None:
    state = make_state()

    UpdateSemanticPort(
        port_id="port-1",
        properties={
            "voltage": 24,
            "protocol": "PWM",
        },
    ).apply(state)

    assert (
        state.semantic_model.ports[
            "port-1"
        ].properties
        == {
            "voltage": 24,
            "protocol": "PWM",
        }
    )


def test_set_port_property() -> None:
    state = make_state()

    SetSemanticPortProperty(
        port_id="port-1",
        property_name="current",
        value=2.0,
    ).apply(state)

    assert (
        state.semantic_model.ports[
            "port-1"
        ].properties["current"]
        == 2.0
    )


def test_update_port_rejects_unknown_port() -> None:
    state = make_state()

    try:
        UpdateSemanticPort(
            port_id="missing",
            purpose="Power",
        ).apply(state)

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown semantic port"
            in str(exc)
        )


def test_set_property_rejects_unknown_port() -> None:
    state = make_state()

    try:
        SetSemanticPortProperty(
            port_id="missing",
            property_name="voltage",
            value=24,
        ).apply(state)

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown semantic port"
            in str(exc)
        )


def test_update_port_rejects_blank_purpose() -> None:
    state = make_state()

    try:
        UpdateSemanticPort(
            port_id="port-1",
            purpose="   ",
        ).apply(state)

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert "purpose" in str(exc)


def test_update_port_rejects_blank_direction() -> None:
    state = make_state()

    try:
        UpdateSemanticPort(
            port_id="port-1",
            direction="   ",
        ).apply(state)

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert "direction" in str(exc)


def test_set_port_property_rejects_blank_name() -> None:
    state = make_state()

    try:
        SetSemanticPortProperty(
            port_id="port-1",
            property_name="   ",
            value=24,
        ).apply(state)

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert "property name" in str(exc)