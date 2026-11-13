from machine_builder.editor_state import EditorState
from machine_builder.semantic_component_mutations import (
    UpdateMachineComponentWithStepperTerminalProfile,
)
from machine_builder.semantic_model import (
    CanonicalMachineModel,
    Machine,
    MachineComponent,
    SemanticPort,
)
from machine_builder.visual_model import VisualModel, VisualNode, VisualPort


def _make_motor_state():
    state = EditorState(
        visual_model=VisualModel(),
        semantic_model=CanonicalMachineModel(),
    )
    state.semantic_model.add_machine(
        Machine(id="machine-1", name="Test machine")
    )
    component = MachineComponent(
        id="motor-1",
        role="X MOT",
        label="X MOT",
        properties={"visual_node_type": "motor"},
    )
    state.semantic_model.add_component("machine-1", component)

    interface = SemanticPort(
        id="motor-1-motor-electrical-interface",
        component_id=component.id,
        purpose="Motor electrical interface",
        properties={
            "interface_role": "motor_electrical_interface",
            "interface_granularity": "functional_interface",
            "visual_port_type": "motor",
            "visual_side": "left",
        },
    )
    state.semantic_model.add_port(interface)

    node = VisualNode(
        id="motor-node",
        node_type="motor",
        label="X MOT",
        semantic_reference=component.id,
    )
    visual_interface = VisualPort(
        id="motor-node-electrical-interface",
        node_id=node.id,
        label=interface.purpose,
        port_type="motor",
        semantic_reference=interface.id,
        side="left",
        order=0,
    )
    node.ports[visual_interface.id] = visual_interface
    for index, suffix in enumerate(("a", "b"), start=1):
        provisional_id = f"motor-node-provisional-{suffix}"
        node.ports[provisional_id] = VisualPort(
            id=provisional_id,
            node_id=node.id,
            label=f"Legacy motor port {suffix.upper()}",
            port_type="motor",
            direction="unknown",
            semantic_reference=None,
            side="left",
            order=index,
        )
    state.visual_model.add_node(node)
    return state, component, interface, node


def _apply_component_properties(state, component, properties):
    mutation = UpdateMachineComponentWithStepperTerminalProfile(
        component_id=component.id,
        role=component.role,
        label=component.label,
        properties=properties,
        provenance_entries=component.provenance.copy(),
    )
    mutation.apply(state)


def _terminal_ports(state, component):
    return [
        port
        for port in state.semantic_model.ports.values()
        if port.component_id == component.id
        and port.properties.get("interface_role") == "motor_conductor_terminal"
    ]


def test_explicit_stepper_profile_projects_four_unassigned_lead_endpoints():
    state, component, interface, node = _make_motor_state()

    _apply_component_properties(
        state,
        component,
        {
            "visual_node_type": "motor",
            "motor_terminal_profile": "stepper_four_lead",
        },
    )

    terminals = _terminal_ports(state, component)
    assert len(terminals) == 4
    assert {port.id for port in terminals} == {
        f"{component.id}-stepper-lead-{index}" for index in range(1, 5)
    }
    assert all(
        port.properties["terminal_identity_status"] == "unassigned"
        and port.properties["motor_coil_mapping_status"] == "not_established"
        and port.properties["controller_contact_mapping_status"] == "not_established"
        for port in terminals
    )
    assert interface.id in {port.semantic_reference for port in node.ports.values()}
    assert {port.semantic_reference for port in node.ports.values()} >= {
        interface.id, *(port.id for port in terminals)
    }
    assert not any(
        port.semantic_reference is None
        for port in node.ports.values()
    )


def test_generic_motor_does_not_gain_stepper_terminals_without_profile():
    state, component, _interface, _node = _make_motor_state()

    _apply_component_properties(
        state,
        component,
        {"visual_node_type": "motor"},
    )

    assert _terminal_ports(state, component) == []


def test_applying_stepper_profile_twice_does_not_duplicate_terminals():
    state, component, _interface, node = _make_motor_state()
    properties = {
        "visual_node_type": "motor",
        "motor_terminal_profile": "stepper_four_lead",
    }

    _apply_component_properties(state, component, properties)
    _apply_component_properties(state, component, properties)

    terminals = _terminal_ports(state, component)
    assert len(terminals) == 4
    assert len({port.id for port in terminals}) == 4
    projected_terminal_ids = {
        visual_port.semantic_reference
        for visual_port in node.ports.values()
        if (
            visual_port.semantic_reference is not None
            and visual_port.semantic_reference in state.semantic_model.ports
            and state.semantic_model.ports[
                visual_port.semantic_reference
            ].properties.get("interface_role") == "motor_conductor_terminal"
        )
    }
    assert projected_terminal_ids == {port.id for port in terminals}
def test_stepper_profile_removes_only_unused_provisional_ports():
    from machine_builder.visual_model import VisualConnection

    state, component, _interface, node = _make_motor_state()
    provisional_a = "motor-node-provisional-a"
    provisional_b = "motor-node-provisional-b"
    state.visual_model.connections["legacy-placeholder-connection"] = VisualConnection(
        id="legacy-placeholder-connection",
        endpoint_a_id=provisional_a,
        endpoint_b_id="external-existing-endpoint",
        connection_type="electrical",
    )

    _apply_component_properties(
        state,
        component,
        {
            "visual_node_type": "motor",
            "motor_terminal_profile": "stepper_four_lead",
        },
    )

    assert provisional_a in node.ports
    assert provisional_b not in node.ports
