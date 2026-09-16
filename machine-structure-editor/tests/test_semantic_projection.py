"""Tests for canonical-to-visual semantic projection."""

from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
    SemanticPort,
)
from machine_builder.semantic_projection import (
    project_component_ports,
)
from machine_builder.visual_model import (
    VisualNode,
    VisualPort,
)


def build_component() -> tuple[
    CanonicalMachineModel,
    MachineComponent,
]:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
        label="Part Cooling Fan",
    )

    model.add_component(
        "machine-1",
        component,
    )

    model.add_port(
        SemanticPort(
            id="port-power",
            component_id=component.id,
            purpose="Power",
            direction="input",
        )
    )

    model.add_port(
        SemanticPort(
            id="port-ground",
            component_id=component.id,
            purpose="Ground",
            direction="unknown",
        )
    )

    return (
        model,
        component,
    )


def test_projection_creates_visual_ports_from_canonical_ports() -> None:
    (
        model,
        component,
    ) = build_component()

    node = VisualNode(
        id="node-1",
        node_type="part_cooling_fan",
        label="Part Cooling Fan",
    )

    project_component_ports(
        component,
        model,
        node,
    )

    assert len(
        node.ports
    ) == 2

    semantic_references = {
        port.semantic_reference
        for port in node.ports.values()
    }

    assert semantic_references == {
        "port-power",
        "port-ground",
    }


def test_projection_uses_canonical_purpose_as_visual_label() -> None:
    (
        model,
        component,
    ) = build_component()

    node = VisualNode(
        id="node-1",
        node_type="part_cooling_fan",
        label="Part Cooling Fan",
    )

    project_component_ports(
        component,
        model,
        node,
    )

    labels = {
        port.label
        for port in node.ports.values()
    }

    assert labels == {
        "Power",
        "Ground",
    }


def test_projection_uses_canonical_direction() -> None:
    (
        model,
        component,
    ) = build_component()

    node = VisualNode(
        id="node-1",
        node_type="part_cooling_fan",
        label="Part Cooling Fan",
    )

    project_component_ports(
        component,
        model,
        node,
    )

    by_reference = {
        port.semantic_reference: port
        for port in node.ports.values()
    }

    assert (
        by_reference["port-power"].direction
        == "input"
    )

    assert (
        by_reference["port-ground"].direction
        == "unknown"
    )


def test_projection_preserves_existing_visual_placement() -> None:
    (
        model,
        component,
    ) = build_component()

    node = VisualNode(
        id="node-1",
        node_type="part_cooling_fan",
        label="Part Cooling Fan",
    )

    existing = VisualPort(
        id="old-power-visual-id",
        node_id=node.id,
        label="Power",
        port_type="power",
        direction="input",
        semantic_reference=None,
        side="right",
        order=7,
    )

    node.ports[
        existing.id
    ] = existing

    project_component_ports(
        component,
        model,
        node,
    )

    projected = next(
        port
        for port in node.ports.values()
        if port.semantic_reference
        == "port-power"
    )

    assert projected.side == "right"
    assert projected.order == 7
    assert projected.id == "old-power-visual-id"


def test_projection_removes_visual_ports_without_canonical_counterpart() -> None:
    (
        model,
        component,
    ) = build_component()

    node = VisualNode(
        id="node-1",
        node_type="part_cooling_fan",
        label="Part Cooling Fan",
    )

    node.ports[
        "obsolete"
    ] = VisualPort(
        id="obsolete",
        node_id=node.id,
        label="Obsolete",
        port_type="unknown",
        direction="unknown",
        side="left",
        order=0,
    )

    project_component_ports(
        component,
        model,
        node,
    )

    assert "obsolete" not in node.ports

    assert {
        port.label
        for port in node.ports.values()
    } == {
        "Power",
        "Ground",
    }