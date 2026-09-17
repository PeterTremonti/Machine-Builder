"""Tests for semantic port queries."""

from machine_builder.editor_state import (
    EditorState,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
    SemanticPort,
)
from machine_builder.semantic_port_queries import (
    component_for_port,
    get_port,
    machine_id_for_port,
    port_id_for_visual_port,
    semantic_ports_for_component,
    visual_node_for_semantic_port,
    visual_port_for_semantic_port,
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

    component = MachineComponent(
        id="component-1",
        role="motor",
        label="X Axis Motor",
    )

    semantic_model.add_component(
        "machine-1",
        component,
    )

    port_a = SemanticPort(
        id="port-a",
        component_id="component-1",
        purpose="Motor Command",
        direction="output",
    )

    port_b = SemanticPort(
        id="port-b",
        component_id="component-1",
        purpose="Power",
        direction="input",
    )

    semantic_model.add_port(
        port_a
    )

    semantic_model.add_port(
        port_b
    )

    visual_model = VisualModel()

    node = VisualNode(
        id="node-1",
        node_type="motor",
        label="X Axis Motor",
        semantic_reference="component-1",
    )

    node.add_port(
        VisualPort(
            id="visual-port-a",
            node_id="node-1",
            label="Motor Command",
            port_type="signal",
            direction="output",
            semantic_reference="port-a",
            side="right",
            order=0,
        )
    )

    node.add_port(
        VisualPort(
            id="visual-port-b",
            node_id="node-1",
            label="Power",
            port_type="power",
            direction="input",
            semantic_reference="port-b",
            side="left",
            order=0,
        )
    )

    visual_model.add_node(
        node
    )

    return EditorState(
        visual_model=visual_model,
        semantic_model=semantic_model,
    )


def test_get_port_returns_semantic_port() -> None:
    state = make_state()

    port = get_port(
        state,
        "port-a",
    )

    assert port.id == "port-a"
    assert port.purpose == "Motor Command"


def test_get_port_rejects_unknown_port() -> None:
    state = make_state()

    try:
        get_port(
            state,
            "missing",
        )

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown semantic port"
            in str(exc)
        )


def test_component_for_port_returns_owner() -> None:
    state = make_state()

    component = component_for_port(
        state,
        "port-a",
    )

    assert component.id == (
        "component-1"
    )


def test_component_for_port_rejects_broken_reference() -> None:
    state = make_state()

    state.semantic_model.ports[
        "port-a"
    ].component_id = "missing-component"

    try:
        component_for_port(
            state,
            "port-a",
        )

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert (
            "unknown component"
            in str(exc)
        )


def test_visual_port_for_semantic_port_resolves_visual_port() -> None:
    state = make_state()

    visual_port = (
        visual_port_for_semantic_port(
            state,
            "port-a",
        )
    )

    assert visual_port is not None
    assert visual_port.id == (
        "visual-port-a"
    )


def test_visual_node_for_semantic_port_resolves_node() -> None:
    state = make_state()

    node = visual_node_for_semantic_port(
        state,
        "port-a",
    )

    assert node is not None
    assert node.id == "node-1"


def test_visual_port_resolution_can_be_absent() -> None:
    state = make_state()

    state.visual_model.nodes[
        "node-1"
    ].ports.pop(
        "visual-port-a"
    )

    assert (
        visual_port_for_semantic_port(
            state,
            "port-a",
        )
        is None
    )


def test_machine_id_for_port_returns_owner_machine() -> None:
    state = make_state()

    assert (
        machine_id_for_port(
            state,
            "port-a",
        )
        == "machine-1"
    )


def test_machine_id_for_port_rejects_unattached_component() -> None:
    state = make_state()

    state.semantic_model.machines[
        "machine-1"
    ].component_ids.clear()

    try:
        machine_id_for_port(
            state,
            "port-a",
        )

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert (
            "not attached to a machine"
            in str(exc)
        )


def test_port_id_for_visual_port_returns_reference() -> None:
    state = make_state()

    assert (
        port_id_for_visual_port(
            state,
            "node-1",
            "visual-port-a",
        )
        == "port-a"
    )


def test_port_id_for_visual_port_can_be_unlinked() -> None:
    state = make_state()

    state.visual_model.nodes[
        "node-1"
    ].ports[
        "visual-port-a"
    ].semantic_reference = None

    assert (
        port_id_for_visual_port(
            state,
            "node-1",
            "visual-port-a",
        )
        is None
    )


def test_port_id_for_visual_port_rejects_unknown_node() -> None:
    state = make_state()

    try:
        port_id_for_visual_port(
            state,
            "missing-node",
            "visual-port-a",
        )

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown visual node"
            in str(exc)
        )


def test_port_id_for_visual_port_rejects_unknown_visual_port() -> None:
    state = make_state()

    try:
        port_id_for_visual_port(
            state,
            "node-1",
            "missing-port",
        )

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown visual port"
            in str(exc)
        )


def test_semantic_ports_for_component_returns_all_ports() -> None:
    state = make_state()

    ports = semantic_ports_for_component(
        state,
        "component-1",
    )

    assert [port.id for port in ports] == [
        "port-a",
        "port-b",
    ]


def test_semantic_ports_for_unknown_component_rejects_id() -> None:
    state = make_state()

    try:
        semantic_ports_for_component(
            state,
            "missing-component",
        )

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown machine component"
            in str(exc)
        )


def test_semantic_ports_for_component_ignores_stale_port_id() -> None:
    state = make_state()

    state.semantic_model.components[
        "component-1"
    ].port_ids.append(
        "missing-port"
    )

    ports = semantic_ports_for_component(
        state,
        "component-1",
    )

    assert [port.id for port in ports] == [
        "port-a",
        "port-b",
    ]