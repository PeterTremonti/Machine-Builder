"""Tests for projecting multiple canonical ports with the same purpose."""

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


def build_duplicate_power_case() -> tuple[
    CanonicalMachineModel,
    MachineComponent,
    VisualNode,
]:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    component = MachineComponent(
        id="component-heater",
        role="Chamber Heater",
    )

    model.add_component(
        "machine-1",
        component,
    )

    model.add_port(
        SemanticPort(
            id="component-heater-terminal-a",
            component_id=component.id,
            purpose="Power",
            direction="input",
        )
    )

    model.add_port(
        SemanticPort(
            id="component-heater-terminal-b",
            component_id=component.id,
            purpose="Power",
            direction="input",
        )
    )

    node = VisualNode(
        id="heater-node",
        node_type="chamber_heater",
        label="Chamber Heater",
    )

    node.ports[
        "heater-node-terminal-a"
    ] = VisualPort(
        id="heater-node-terminal-a",
        node_id=node.id,
        label="Power",
        port_type="power",
        direction="input",
        side="left",
        order=0,
    )

    node.ports[
        "heater-node-terminal-b"
    ] = VisualPort(
        id="heater-node-terminal-b",
        node_id=node.id,
        label="Power",
        port_type="power",
        direction="input",
        side="left",
        order=1,
    )

    return (
        model,
        component,
        node,
    )


def test_duplicate_purposes_match_distinct_visual_ports() -> None:
    (
        model,
        component,
        node,
    ) = build_duplicate_power_case()

    project_component_ports(
        component,
        model,
        node,
    )

    assert (
        node.ports[
            "heater-node-terminal-a"
        ].semantic_reference
        == "component-heater-terminal-a"
    )

    assert (
        node.ports[
            "heater-node-terminal-b"
        ].semantic_reference
        == "component-heater-terminal-b"
    )


def test_duplicate_purposes_preserve_visual_port_count() -> None:
    (
        model,
        component,
        node,
    ) = build_duplicate_power_case()

    project_component_ports(
        component,
        model,
        node,
    )

    assert len(
        node.ports
    ) == 2


def test_duplicate_purposes_preserve_visual_order() -> None:
    (
        model,
        component,
        node,
    ) = build_duplicate_power_case()

    project_component_ports(
        component,
        model,
        node,
    )

    assert (
        node.ports[
            "heater-node-terminal-a"
        ].order
        == 0
    )

    assert (
        node.ports[
            "heater-node-terminal-b"
        ].order
        == 1
    )