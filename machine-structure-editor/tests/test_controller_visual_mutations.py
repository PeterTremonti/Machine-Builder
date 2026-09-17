"""Tests for controller visual authoring."""

from machine_builder.canvas import MachineCanvas
from machine_builder.controller import Controller
from machine_builder.controller_visual_mutations import (
    CreateControllerNode,
    CreateControllerVisualNode,
)
from machine_builder.editor_state import EditorState
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
)
from machine_builder.store import ModelStore
from machine_builder.visual_model import (
    VisualModel,
    VisualNode,
)


def make_state() -> EditorState:
    model = CanonicalMachineModel()

    model.add_machine(
        Machine(
            id="machine-1",
            name="Test Machine",
        )
    )

    model.add_controller(
        "machine-1",
        Controller(
            id="controller-1",
            name="BTT Octopus V1.1",
            controller_type="motion_controller",
            version="V1.1",
        ),
    )

    return EditorState(
        visual_model=VisualModel(),
        semantic_model=model,
    )


def make_node() -> VisualNode:
    return VisualNode(
        id="controller-node-1",
        node_type="controller",
        label="Controller",
    )


def make_store() -> ModelStore:
    return ModelStore(
        semantic_model=make_state().semantic_model,
    )


def test_create_controller_node_creates_controller() -> None:
    state = EditorState(
        visual_model=VisualModel(),
        semantic_model=CanonicalMachineModel(),
    )

    node = make_node()

    controller = Controller(
        id="controller-1",
        name="BTT Octopus V1.1",
        controller_type="motion_controller",
        version="V1.1",
    )

    CreateControllerNode(
        controller=controller,
        node=node,
    ).apply(state)

    assert (
        state.semantic_model.controllers[
            "controller-1"
        ]
        is controller
    )

    assert (
        node.semantic_reference
        == "controller-1"
    )

    assert (
        state.visual_model.nodes[
            node.id
        ]
        is node
    )


def test_create_controller_node_attaches_controller_to_machine() -> None:
    state = EditorState(
        visual_model=VisualModel(),
        semantic_model=CanonicalMachineModel(),
    )

    node = make_node()

    controller = Controller(
        id="controller-1",
        name="BTT Octopus V1.1",
        controller_type="motion_controller",
    )

    CreateControllerNode(
        controller=controller,
        node=node,
    ).apply(state)

    assert (
        state.semantic_model.machines[
            "machine-1"
        ].controller_ids
        == ["controller-1"]
    )


def test_create_controller_node_rejects_non_controller_node() -> None:
    state = make_state()

    node = VisualNode(
        id="motor-node-1",
        node_type="motor",
        label="Motor",
    )

    controller = Controller(
        id="controller-2",
        name="Controller",
        controller_type="controller",
    )

    try:
        CreateControllerNode(
            controller=controller,
            node=node,
        ).apply(state)

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert (
            "node_type='controller'"
            in str(exc)
        )


def test_create_controller_node_is_undoable() -> None:
    store = make_store()

    node = make_node()

    controller = Controller(
        id="controller-2",
        name="New Controller",
        controller_type="controller",
    )

    store.commit(
        CreateControllerNode(
            controller=controller,
            node=node,
        )
    )

    assert (
        "controller-2"
        in store.semantic_model.controllers
    )

    assert store.undo()

    assert (
        "controller-2"
        not in store.semantic_model.controllers
    )

    assert (
        node.id
        not in store.model.nodes
    )


def test_create_controller_node_is_redoable() -> None:
    store = make_store()

    node = make_node()

    controller = Controller(
        id="controller-2",
        name="New Controller",
        controller_type="controller",
    )

    store.commit(
        CreateControllerNode(
            controller=controller,
            node=node,
        )
    )

    assert store.undo()
    assert store.redo()

    assert (
        store.semantic_model.controllers[
            "controller-2"
        ]
        is not None
    )

    assert (
        store.model.nodes[
            node.id
        ].semantic_reference
        == "controller-2"
    )


def test_controller_visual_node_has_no_ports() -> None:
    node = make_node()

    assert node.ports == {}


def test_create_controller_visual_node_links_existing_controller() -> None:
    state = make_state()
    node = make_node()

    CreateControllerVisualNode(
        controller_id="controller-1",
        node=node,
    ).apply(state)

    assert (
        node.semantic_reference
        == "controller-1"
    )

    assert (
        node.label
        == "BTT Octopus V1.1"
    )

    assert (
        state.visual_model.nodes[node.id]
        is node
    )


def test_create_controller_visual_node_does_not_create_controller() -> None:
    state = make_state()
    node = make_node()

    CreateControllerVisualNode(
        controller_id="controller-1",
        node=node,
    ).apply(state)

    assert list(
        state.semantic_model.controllers
    ) == ["controller-1"]


def test_create_controller_visual_node_rejects_unknown_controller() -> None:
    state = make_state()

    try:
        CreateControllerVisualNode(
            controller_id="missing",
            node=make_node(),
        ).apply(state)

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown controller"
            in str(exc)
        )


def test_create_controller_visual_node_rejects_existing_visual_node() -> None:
    state = make_state()
    node = make_node()

    state.visual_model.add_node(
        node
    )

    try:
        CreateControllerVisualNode(
            controller_id="controller-1",
            node=node,
        ).apply(state)

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert (
            "Visual node already exists"
            in str(exc)
        )