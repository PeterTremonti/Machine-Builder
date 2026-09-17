"""Tests for machine-component semantic queries."""

from machine_builder.editor_state import (
    EditorState,
)
from machine_builder.semantic_component_queries import (
    component_for_visual_node,
    component_id_for_visual_node,
    get_component,
    machine_id_for_component,
    ports_for_component,
    visual_node_for_component,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
    SemanticPort,
)
from machine_builder.visual_model import (
    VisualModel,
    VisualNode,
)


def make_state() -> EditorState:
    semantic_model = CanonicalMachineModel()

    semantic_model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    component = MachineComponent(
        id="component-1",
        role="motor",
        label="Test Motor",
    )

    semantic_model.add_component(
        "machine-1",
        component,
    )

    port = SemanticPort(
        id="component-1-power",
        component_id="component-1",
        purpose="Power",
        direction="input",
    )

    semantic_model.add_port(
        port
    )

    visual_model = VisualModel()

    visual_model.add_node(
        VisualNode(
            id="node-1",
            node_type="motor",
            label="Test Motor",
            semantic_reference="component-1",
        )
    )

    visual_model.add_node(
        VisualNode(
            id="orphan-node",
            node_type="motor",
            label="Unlinked Motor",
        )
    )

    return EditorState(
        visual_model=visual_model,
        semantic_model=semantic_model,
    )


def test_get_component_returns_component() -> None:
    state = make_state()

    component = get_component(
        state,
        "component-1",
    )

    assert component.id == "component-1"
    assert component.role == "motor"


def test_get_component_rejects_unknown_id() -> None:
    state = make_state()

    try:
        get_component(
            state,
            "missing",
        )

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown machine component"
            in str(exc)
        )


def test_component_for_visual_node_resolves_reference() -> None:
    state = make_state()

    component = component_for_visual_node(
        state,
        "node-1",
    )

    assert component is not None
    assert component.id == "component-1"


def test_component_for_unlinked_visual_node_returns_none() -> None:
    state = make_state()

    assert (
        component_for_visual_node(
            state,
            "orphan-node",
        )
        is None
    )


def test_component_for_unknown_visual_node_rejects_id() -> None:
    state = make_state()

    try:
        component_for_visual_node(
            state,
            "missing",
        )

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown visual node"
            in str(exc)
        )


def test_visual_node_for_component_resolves_node() -> None:
    state = make_state()

    node = visual_node_for_component(
        state,
        "component-1",
    )

    assert node is not None
    assert node.id == "node-1"


def test_visual_node_for_component_can_be_absent() -> None:
    state = make_state()

    node = visual_node_for_component(
        state,
        "component-1",
    )

    assert node is not None

    del state.visual_model.nodes[
        "node-1"
    ]

    assert (
        visual_node_for_component(
            state,
            "component-1",
        )
        is None
    )


def test_ports_for_component_returns_component_ports() -> None:
    state = make_state()

    ports = ports_for_component(
        state,
        "component-1",
    )

    assert len(ports) == 1
    assert ports[0].id == (
        "component-1-power"
    )


def test_ports_for_component_returns_empty_tuple_when_no_ports() -> None:
    state = make_state()

    state.semantic_model.components[
        "component-1"
    ].port_ids.clear()

    ports = ports_for_component(
        state,
        "component-1",
    )

    assert ports == ()


def test_machine_id_for_component_returns_owner() -> None:
    state = make_state()

    assert (
        machine_id_for_component(
            state,
            "component-1",
        )
        == "machine-1"
    )


def test_machine_id_for_component_rejects_unattached_component() -> None:
    state = make_state()

    state.semantic_model.machines[
        "machine-1"
    ].component_ids.clear()

    try:
        machine_id_for_component(
            state,
            "component-1",
        )

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert (
            "not attached to a machine"
            in str(exc)
        )


def test_component_id_for_visual_node_returns_reference() -> None:
    state = make_state()

    assert (
        component_id_for_visual_node(
            state,
            "node-1",
        )
        == "component-1"
    )


def test_component_id_for_unlinked_visual_node_returns_none() -> None:
    state = make_state()

    assert (
        component_id_for_visual_node(
            state,
            "orphan-node",
        )
        is None
    )