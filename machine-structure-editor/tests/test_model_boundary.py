"""Tests for the canonical/visual model boundary."""

from machine_builder.model_boundary import (
    SemanticModelBoundary,
)
from machine_builder.semantic_model import (
    Machine,
    MachineComponent,
)
from machine_builder.visual_model import (
    VisualModel,
    VisualNode,
)


def build_boundary() -> (
    tuple[
        SemanticModelBoundary,
        Machine,
        MachineComponent,
        VisualNode,
    ]
):
    canonical_model = (
        __import__(
            "machine_builder.semantic_model",
            fromlist=[
                "CanonicalMachineModel"
            ],
        ).CanonicalMachineModel()
    )

    visual_model = VisualModel()

    machine = Machine(
        id="machine-1",
        name="Test Printer",
    )

    canonical_model.add_machine(
        machine
    )

    component = MachineComponent(
        id="component-1",
        role="Part Cooling Fan",
        label="Part Cooling Fan",
    )

    canonical_model.add_component(
        machine.id,
        component,
    )

    node = VisualNode(
        id="node-1",
        node_type="fan",
        label="Part Cooling Fan",
    )

    visual_model.add_node(
        node
    )

    boundary = SemanticModelBoundary(
        canonical_model=canonical_model,
        visual_model=visual_model,
    )

    return (
        boundary,
        machine,
        component,
        node,
    )


def test_visual_node_can_be_bound_to_canonical_component() -> None:
    (
        boundary,
        _machine,
        component,
        node,
    ) = build_boundary()

    boundary.bind_node(
        node,
        component.id,
    )

    assert (
        node.semantic_reference
        == component.id
    )

    assert boundary.is_bound(
        node.id
    )


def test_boundary_resolves_component_from_visual_node() -> None:
    (
        boundary,
        _machine,
        component,
        node,
    ) = build_boundary()

    boundary.bind_node(
        node,
        component.id,
    )

    resolved = (
        boundary.get_component_for_node(
            node.id
        )
    )

    assert resolved is component


def test_boundary_resolves_visual_node_from_component() -> None:
    (
        boundary,
        _machine,
        component,
        node,
    ) = build_boundary()

    boundary.bind_node(
        node,
        component.id,
    )

    resolved = (
        boundary.get_node_for_component(
            component.id
        )
    )

    assert resolved is node


def test_unbound_visual_node_returns_no_component() -> None:
    (
        boundary,
        _machine,
        _component,
        node,
    ) = build_boundary()

    assert (
        boundary.get_component_for_node(
            node.id
        )
        is None
    )

    assert not boundary.is_bound(
        node.id
    )


def test_binding_unknown_component_is_rejected() -> None:
    (
        boundary,
        _machine,
        _component,
        node,
    ) = build_boundary()

    try:
        boundary.bind_node(
            node,
            "missing-component",
        )
    except ValueError as exc:
        assert (
            "Canonical component does not exist"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected unknown canonical component "
            "to be rejected"
        )


def test_binding_unknown_visual_node_is_rejected() -> None:
    (
        boundary,
        _machine,
        component,
        _node,
    ) = build_boundary()

    missing_node = VisualNode(
        id="missing-node",
        node_type="fan",
        label="Missing",
    )

    try:
        boundary.bind_node(
            missing_node,
            component.id,
        )
    except ValueError as exc:
        assert (
            "Visual node is not in the visual model"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected unknown visual node "
            "to be rejected"
        )


def test_visual_node_cannot_be_rebound_to_different_component() -> None:
    (
        boundary,
        machine,
        component,
        node,
    ) = build_boundary()

    second_component = MachineComponent(
        id="component-2",
        role="Heater",
        label="Heater",
    )

    boundary.create_component(
        machine.id,
        second_component,
    )

    boundary.bind_node(
        node,
        component.id,
    )

    try:
        boundary.bind_node(
            node,
            second_component.id,
        )
    except ValueError as exc:
        assert (
            "already bound"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected rebinding to be rejected"
        )


def test_create_component_uses_canonical_model() -> None:
    (
        boundary,
        machine,
        _component,
        _node,
    ) = build_boundary()

    new_component = MachineComponent(
        id="component-3",
        role="Temperature Sensor",
        label="Hotend Temperature",
    )

    result = boundary.create_component(
        machine.id,
        new_component,
    )

    assert result is new_component

    assert (
        boundary.canonical_model.components[
            "component-3"
        ]
        is new_component
    )

    assert (
        "component-3"
        in boundary.canonical_model.machines[
            machine.id
        ].component_ids
    )