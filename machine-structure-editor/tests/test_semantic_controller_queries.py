"""Tests for controller semantic queries."""

from machine_builder.controller_fixtures import (
    add_generic_octopus_controller,
)
from machine_builder.editor_state import (
    EditorState,
)
from machine_builder.semantic_controller_queries import (
    controller_for_visual_node,
    controller_id_for_visual_node,
    get_controller,
    visual_node_for_controller,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
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

    add_generic_octopus_controller(
        semantic_model,
        "machine-1",
    )

    visual_model = VisualModel()

    visual_model.add_node(
        VisualNode(
            id="controller-node-1",
            node_type="controller",
            label="BTT Octopus V1.1",
            semantic_reference="octopus-v1-1",
        )
    )

    visual_model.add_node(
        VisualNode(
            id="orphan-node",
            node_type="controller",
            label="Unlinked Controller",
        )
    )

    return EditorState(
        visual_model=visual_model,
        semantic_model=semantic_model,
    )


def test_get_controller_returns_controller() -> None:
    state = make_state()

    controller = get_controller(
        state,
        "octopus-v1-1",
    )

    assert controller.id == "octopus-v1-1"
    assert controller.name == "BTT Octopus V1.1"


def test_controller_for_visual_node_resolves_reference() -> None:
    state = make_state()

    controller = controller_for_visual_node(
        state,
        "controller-node-1",
    )

    assert controller is not None
    assert controller.id == "octopus-v1-1"


def test_controller_for_unlinked_visual_node_returns_none() -> None:
    state = make_state()

    assert (
        controller_for_visual_node(
            state,
            "orphan-node",
        )
        is None
    )


def test_controller_for_unknown_visual_node_rejects_id() -> None:
    state = make_state()

    try:
        controller_for_visual_node(
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


def test_visual_node_for_controller_resolves_node() -> None:
    state = make_state()

    node = visual_node_for_controller(
        state,
        "octopus-v1-1",
    )

    assert node is not None
    assert node.id == "controller-node-1"


def test_visual_node_for_controller_can_be_absent() -> None:
    state = make_state()

    del state.visual_model.nodes[
        "controller-node-1"
    ]

    node = visual_node_for_controller(
        state,
        "octopus-v1-1",
    )

    assert node is None


def test_controller_id_for_visual_node_returns_reference() -> None:
    state = make_state()

    assert (
        controller_id_for_visual_node(
            state,
            "controller-node-1",
        )
        == "octopus-v1-1"
    )


def test_controller_id_for_unlinked_visual_node_returns_none() -> None:
    state = make_state()

    assert (
        controller_id_for_visual_node(
            state,
            "orphan-node",
        )
        is None
    )


def test_get_controller_rejects_unknown_id() -> None:
    state = make_state()

    try:
        get_controller(
            state,
            "missing",
        )

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown controller"
            in str(exc)
        )


def test_visual_controller_reference_points_to_canonical_controller() -> None:
    state = make_state()

    node = state.visual_model.nodes[
        "controller-node-1"
    ]

    controller = controller_for_visual_node(
        state,
        node.id,
    )

    assert controller is state.semantic_model.controllers[
        "octopus-v1-1"
    ]
    assert node.semantic_reference == controller.id