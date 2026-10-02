"""Tests for semantic machine-component editing mutations."""

from machine_builder.editor_state import (
    EditorState,
)
from machine_builder.semantic_component_mutations import (
    SetMachineComponentProperty,
    UpdateMachineComponent,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
    Provenance,
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

    semantic_model.add_component(
        "machine-1",
        MachineComponent(
            id="component-1",
            role="motor",
            label="Original Motor",
        ),
    )

    visual_model = VisualModel()

    visual_model.add_node(
        VisualNode(
            id="node-1",
            node_type="motor",
            label="Original Motor",
            semantic_reference="component-1",
        )
    )

    return EditorState(
        visual_model=visual_model,
        semantic_model=semantic_model,
    )


def test_update_component_role() -> None:
    state = make_state()

    UpdateMachineComponent(
        component_id="component-1",
        role="drive motor",
    ).apply(state)

    component = (
        state.semantic_model.components[
            "component-1"
        ]
    )

    assert component.role == "drive motor"


def test_update_component_label_updates_visual_representation() -> None:
    state = make_state()

    UpdateMachineComponent(
        component_id="component-1",
        label="X Axis Motor",
    ).apply(state)

    component = (
        state.semantic_model.components[
            "component-1"
        ]
    )

    node = (
        state.visual_model.nodes[
            "node-1"
        ]
    )

    assert component.label == "X Axis Motor"
    assert node.label == "X Axis Motor"


def test_update_component_properties_replaces_properties() -> None:
    state = make_state()

    UpdateMachineComponent(
        component_id="component-1",
        properties={
            "axis": "X",
            "voltage": 24,
        },
    ).apply(state)

    component = (
        state.semantic_model.components[
            "component-1"
        ]
    )

    assert component.properties == {
        "axis": "X",
        "voltage": 24,
    }


def test_update_component_adds_provenance() -> None:
    state = make_state()

    provenance = Provenance(
        source="user",
        evidence_type="authored",
        method="visual editor authoring",
    )

    UpdateMachineComponent(
        component_id="component-1",
        label="Edited Motor",
        provenance=provenance,
    ).apply(state)

    component = (
        state.semantic_model.components[
            "component-1"
        ]
    )

    assert component.provenance == [
        provenance
    ]


def test_update_component_allows_label_and_role_together() -> None:
    state = make_state()

    UpdateMachineComponent(
        component_id="component-1",
        role="extruder drive motor",
        label="Extruder Motor",
    ).apply(state)

    component = (
        state.semantic_model.components[
            "component-1"
        ]
    )

    node = (
        state.visual_model.nodes[
            "node-1"
        ]
    )

    assert component.role == "extruder drive motor"
    assert component.label == "Extruder Motor"
    assert node.label == "Extruder Motor"


def test_set_component_property() -> None:
    state = make_state()

    SetMachineComponentProperty(
        component_id="component-1",
        property_name="axis",
        value="Z",
    ).apply(state)

    component = (
        state.semantic_model.components[
            "component-1"
        ]
    )

    assert component.properties["axis"] == "Z"


def test_set_component_property_can_store_unknown_information() -> None:
    state = make_state()

    SetMachineComponentProperty(
        component_id="component-1",
        property_name="manufacturer_model",
        value=None,
    ).apply(state)

    component = (
        state.semantic_model.components[
            "component-1"
        ]
    )

    assert (
        "manufacturer_model"
        in component.properties
    )

    assert (
        component.properties[
            "manufacturer_model"
        ]
        is None
    )


def test_update_component_rejects_unknown_component() -> None:
    state = make_state()

    try:
        UpdateMachineComponent(
            component_id="missing",
            label="Nope",
        ).apply(state)

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown machine component"
            in str(exc)
        )


def test_set_property_rejects_unknown_component() -> None:
    state = make_state()

    try:
        SetMachineComponentProperty(
            component_id="missing",
            property_name="axis",
            value="X",
        ).apply(state)

        raise AssertionError(
            "Expected KeyError"
        )
    except KeyError as exc:
        assert (
            "Unknown machine component"
            in str(exc)
        )


def test_update_component_rejects_empty_role() -> None:
    state = make_state()

    try:
        UpdateMachineComponent(
            component_id="component-1",
            role="   ",
        ).apply(state)

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert (
            "role"
            in str(exc)
        )


def test_set_property_rejects_empty_property_name() -> None:
    state = make_state()

    try:
        SetMachineComponentProperty(
            component_id="component-1",
            property_name="   ",
            value=10,
        ).apply(state)

        raise AssertionError(
            "Expected ValueError"
        )
    except ValueError as exc:
        assert (
            "property name"
            in str(exc)
        )