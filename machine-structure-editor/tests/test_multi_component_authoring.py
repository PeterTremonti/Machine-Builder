"""Tests for authoring multiple real hardware components together."""

from machine_builder.mutations import CreateNode
from machine_builder.store import ModelStore
from machine_builder.visual_model import (
    VisualNode,
    VisualPort,
)


def build_fan_node() -> VisualNode:
    node = VisualNode(
        id="fan-1",
        node_type="part_cooling_fan",
        label="Part Cooling Fan",
    )

    node.ports[
        "fan-1-power"
    ] = VisualPort(
        id="fan-1-power",
        node_id=node.id,
        label="Power",
        port_type="power",
        direction="input",
        side="left",
        order=0,
    )

    node.ports[
        "fan-1-ground"
    ] = VisualPort(
        id="fan-1-ground",
        node_id=node.id,
        label="Ground",
        port_type="electrical",
        direction="input",
        side="left",
        order=1,
    )

    return node


def build_heater_node() -> VisualNode:
    node = VisualNode(
        id="heater-1",
        node_type="chamber_heater",
        label="Chamber Heater",
    )

    node.ports[
        "heater-1-terminal-a"
    ] = VisualPort(
        id="heater-1-terminal-a",
        node_id=node.id,
        label="Power",
        port_type="power",
        direction="input",
        side="left",
        order=0,
    )

    node.ports[
        "heater-1-terminal-b"
    ] = VisualPort(
        id="heater-1-terminal-b",
        node_id=node.id,
        label="Power",
        port_type="power",
        direction="input",
        side="left",
        order=1,
    )

    return node


def create_fan_and_heater() -> ModelStore:
    store = ModelStore()

    store.commit(
        CreateNode(
            build_fan_node()
        )
    )

    store.commit(
        CreateNode(
            build_heater_node()
        )
    )

    return store


def test_machine_can_contain_fan_and_heater() -> None:
    store = create_fan_and_heater()

    machine = store.semantic_model.machines[
        "machine-1"
    ]

    assert set(
        machine.component_ids
    ) == {
        "component-fan-1",
        "component-heater-1",
    }


def test_fan_and_heater_use_different_hardware_definitions() -> None:
    store = create_fan_and_heater()

    fan = store.semantic_model.components[
        "component-fan-1"
    ]

    heater = store.semantic_model.components[
        "component-heater-1"
    ]

    assert (
        fan.hardware_definition_id
        == "generic-4010-fan-24v"
    )

    assert (
        heater.hardware_definition_id
        == "generic-120vac-400w-heater"
    )


def test_fan_and_heater_ports_are_independent() -> None:
    store = create_fan_and_heater()

    fan = store.semantic_model.components[
        "component-fan-1"
    ]

    heater = store.semantic_model.components[
        "component-heater-1"
    ]

    assert set(
        fan.port_ids
    ) == {
        "component-fan-1-power",
        "component-fan-1-ground",
    }

    assert set(
        heater.port_ids
    ) == {
        "component-heater-1-terminal-a",
        "component-heater-1-terminal-b",
    }


def test_visual_nodes_keep_separate_canonical_references() -> None:
    store = create_fan_and_heater()

    fan = store.model.nodes[
        "fan-1"
    ]

    heater = store.model.nodes[
        "heater-1"
    ]

    assert (
        fan.semantic_reference
        == "component-fan-1"
    )

    assert (
        heater.semantic_reference
        == "component-heater-1"
    )


def test_visual_fan_ports_and_heater_ports_keep_distinct_semantic_references() -> None:
    store = create_fan_and_heater()

    fan = store.model.nodes[
        "fan-1"
    ]

    heater = store.model.nodes[
        "heater-1"
    ]

    assert {
        port.semantic_reference
        for port in fan.ports.values()
    } == {
        "component-fan-1-power",
        "component-fan-1-ground",
    }

    assert {
        port.semantic_reference
        for port in heater.ports.values()
    } == {
        "component-heater-1-terminal-a",
        "component-heater-1-terminal-b",
    }


def test_shared_hardware_definitions_are_reusable_but_components_are_unique() -> None:
    store = create_fan_and_heater()

    assert len(
        store.semantic_model.components
    ) == 2

    assert len(
        store.semantic_model.hardware_definitions
    ) == 2

    assert (
        store.semantic_model.components[
            "component-fan-1"
        ].hardware_definition_id
        != store.semantic_model.components[
            "component-heater-1"
        ].hardware_definition_id
    )