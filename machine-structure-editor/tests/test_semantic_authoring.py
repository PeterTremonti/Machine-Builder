"""Tests for semantic authoring of real machine components."""

from machine_builder.mutations import CreateNode
from machine_builder.store import ModelStore
from machine_builder.visual_model import (
    VisualNode,
    VisualPort,
)


def build_part_cooling_fan_node() -> VisualNode:
    """Build the visual representation used by the palette."""
    node = VisualNode(
        id="fan-node-1",
        node_type="part_cooling_fan",
        label="Part Cooling Fan",
    )
    node.ports[
        "fan-node-1-power"
    ] = VisualPort(
        id="fan-node-1-power",
        node_id=node.id,
        label="Power",
        port_type="power",
        direction="input",
        side="left",
        order=0,
    )

    node.ports[
        "fan-node-1-ground"
    ] = VisualPort(
        id="fan-node-1-ground",
        node_id=node.id,
        label="Ground",
        port_type="electrical",
        direction="input",
        side="left",
        order=1,
    )

    return node


def test_part_cooling_fan_creation_adds_hardware_definition() -> None:
    store = ModelStore()

    node = build_part_cooling_fan_node()

    store.commit(
        CreateNode(
            node
        )
    )

    assert (
        "generic-4010-fan-24v"
        in store.semantic_model.hardware_definitions
    )

    hardware = (
        store.semantic_model.hardware_definitions[
            "generic-4010-fan-24v"
        ]
    )
    assert hardware.family == "4010 axial fan"
    assert hardware.manufacturer == "Generic / Unbranded"
    assert hardware.variant == "24 V"


def test_part_cooling_fan_creation_adds_canonical_component() -> None:
    store = ModelStore()

    node = build_part_cooling_fan_node()

    store.commit(
        CreateNode(
            node
        )
    )

    assert (
        node.semantic_reference
        == "component-fan-node-1"
    )
    component = (
        store.semantic_model.components[
            "component-fan-node-1"
        ]
    )

    assert component.role == "Part Cooling Fan"
    assert component.label == "Part Cooling Fan"

    assert (
        component.hardware_definition_id
        == "generic-4010-fan-24v"
    )


def test_part_cooling_fan_creation_adds_canonical_ports() -> None:
    store = ModelStore()

    node = build_part_cooling_fan_node()

    store.commit(
        CreateNode(
            node
        )
    )
    component = (
        store.semantic_model.components[
            "component-fan-node-1"
        ]
    )

    assert set(
        component.port_ids
    ) == {
        "component-fan-node-1-power",
        "component-fan-node-1-ground",
    }

    power = (
        store.semantic_model.ports[
            "component-fan-node-1-power"
        ]
    )

    ground = (
        store.semantic_model.ports[
            "component-fan-node-1-ground"
        ]
    )

    assert power.component_id == component.id
    assert power.purpose == "Power"
    assert power.direction == "input"

    assert ground.component_id == component.id
    assert ground.purpose == "Ground"
    assert ground.direction == "unknown"


def test_visual_fan_ports_reference_canonical_ports() -> None:
    store = ModelStore()

    node = build_part_cooling_fan_node()

    store.commit(
        CreateNode(
            node
        )
    )

    power = node.ports[
        "fan-node-1-power"
    ]
    ground = node.ports[
        "fan-node-1-ground"
    ]

    assert (
        power.semantic_reference
        == "component-fan-node-1-power"
    )

    assert (
        ground.semantic_reference
        == "component-fan-node-1-ground"
    )


def test_visual_fan_port_directions_follow_canonical_ports() -> None:
    store = ModelStore()

    node = build_part_cooling_fan_node()

    store.commit(
        CreateNode(
            node
        )
    )

    assert (
        node.ports[
            "fan-node-1-power"
        ].direction
        == "input"
    )

    assert (
        node.ports[
            "fan-node-1-ground"
        ].direction
        == "unknown"
    )


def test_deleting_fan_removes_component_and_ports() -> None:
    store = ModelStore()

    node = build_part_cooling_fan_node()

    store.commit(
        CreateNode(
            node
        )
    )

    from machine_builder.mutations import DeleteNodes

    store.commit(
        DeleteNodes(
            node_ids=(node.id,)
        )
    )

    assert (
        "component-fan-node-1"
        not in store.semantic_model.components
    )

    assert (
        "component-fan-node-1-power"
        not in store.semantic_model.ports
    )

    assert (
        "component-fan-node-1-ground"
        not in store.semantic_model.ports
    )