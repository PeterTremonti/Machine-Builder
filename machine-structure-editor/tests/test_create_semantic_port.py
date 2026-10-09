"""Tests for creating canonical component-owned semantic ports."""

from __future__ import annotations

import pytest

from machine_builder.editor_state import EditorState
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    MachineComponent,
    SemanticPort,
)
from machine_builder.semantic_port_mutations import (
    CreateSemanticPort,
)
from machine_builder.visual_model import (
    VisualConnection,
    VisualModel,
    VisualNode,
    VisualPort,
)


def make_state():
    state = EditorState(
        visual_model=VisualModel(),
        semantic_model=CanonicalMachineModel(),
    )

    component = MachineComponent(
        id="component-1",
        role="motor",
        label="X Axis Motor",
    )
    state.semantic_model.components[component.id] = component

    node = VisualNode(
        id="visual-node-1",
        node_type="motor",
        label=component.label,
        x=0.0,
        y=0.0,
        semantic_reference=component.id,
    )
    state.visual_model.nodes[node.id] = node

    return state, component, node


def make_port(
    component_id: str | None = "component-1",
    controller_id: str | None = None,
) -> SemanticPort:
    return SemanticPort(
        id="component-1-port-1",
        component_id=component_id,
        controller_id=controller_id,
        purpose="Motor winding",
        direction="unknown",
        connector_id=None,
        pin_id=None,
        properties={},
        provenance=[],
    )


def test_create_semantic_port_registers_canonical_owner() -> None:
    state, component, _node = make_state()
    port = make_port()

    CreateSemanticPort(port).apply(state)

    assert state.semantic_model.ports[port.id] is port
    assert component.port_ids == [port.id]
    assert port.component_id == component.id
    assert port.controller_id is None


def test_create_semantic_port_projects_visual_reference() -> None:
    state, _component, node = make_state()
    port = make_port()

    CreateSemanticPort(port).apply(state)

    assert len(node.ports) == 1
    visual_port = next(iter(node.ports.values()))
    assert visual_port.semantic_reference == port.id
    assert visual_port.label == port.purpose
    assert visual_port.direction == port.direction


def test_create_semantic_port_rejects_non_component_ownership() -> None:
    state, _component, _node = make_state()
    port = make_port(
        component_id=None,
        controller_id="controller-1",
    )

    with pytest.raises(
        ValueError,
        match="MachineComponent owner",
    ):
        CreateSemanticPort(port).apply(state)



def test_create_semantic_port_preserves_unmatched_provisional_port_and_wire() -> None:
    state, _component, component_node = make_state()

    provisional_port = VisualPort(
        id="component-provisional-power",
        node_id=component_node.id,
        label="Power",
        port_type="power",
        direction="unknown",
        semantic_reference=None,
        side="left",
        order=0,
    )
    component_node.add_port(provisional_port)

    peer_node = VisualNode(
        id="peer-node",
        node_type="generic",
        label="Peer",
        x=180.0,
        y=0.0,
    )
    peer_port = VisualPort(
        id="peer-port",
        node_id=peer_node.id,
        label="Peer Connection",
        port_type="signal",
        direction="unknown",
        semantic_reference=None,
        side="left",
        order=0,
    )
    peer_node.add_port(peer_port)
    state.visual_model.nodes[peer_node.id] = peer_node

    connection = VisualConnection(
        id="provisional-wire",
        endpoint_a_id=provisional_port.id,
        endpoint_b_id=peer_port.id,
    )
    state.visual_model.add_connection(connection)

    CreateSemanticPort(
        make_port()
    ).apply(state)

    assert (
        state.visual_model.find_port(
            provisional_port.id
        )
        is provisional_port
    )
    assert (
        state.visual_model.connections[
            connection.id
        ].endpoint_a_id
        == provisional_port.id
    )
    assert (
        state.visual_model.find_port(peer_port.id)
        is peer_port
    )
